"""
Cliente da API OpenAlex (genérico: não depende do tema).

Coleta paginada via cursor, com retry exponencial e polite pool via mailto.
Documentação: https://docs.openalex.org/
"""
import time
import logging
from typing import Optional
from dataclasses import dataclass, field

import requests
import backoff
from tqdm import tqdm

logger = logging.getLogger(__name__)

OPENALEX_BASE_URL = "https://api.openalex.org/works"
OPENALEX_PER_PAGE_MAX = 200
DEFAULT_PER_PAGE = 50
DEFAULT_TIMEOUT = 30

DEFAULT_SELECT_FIELDS = [
    "id", "doi", "title", "publication_year", "publication_date",
    "type", "language", "open_access",
    "authorships", "primary_location",
    "cited_by_count", "concepts", "topics",
    "abstract_inverted_index", "is_retracted",
]


@dataclass
class OpenAlexArticle:
    """Registro simplificado de um trabalho retornado pela OpenAlex."""
    id: str
    doi: Optional[str]
    titulo: str
    ano: Optional[int]
    data_publicacao: Optional[str]
    idioma: Optional[str]
    tipo: Optional[str]
    acesso_aberto: bool
    retratado: bool
    primeiro_autor: Optional[str]
    autores: list = field(default_factory=list)
    n_autores: int = 0
    instituicoes: list = field(default_factory=list)
    paises: list = field(default_factory=list)
    pais_principal: Optional[str] = None
    periodico: Optional[str] = None
    citacoes: int = 0
    conceitos: list = field(default_factory=list)
    topicos: list = field(default_factory=list)
    abstract: str = ""
    queries_origem: list = field(default_factory=list)
    areas_origem: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "doi": self.doi,
            "titulo": self.titulo,
            "ano": self.ano,
            "data_publicacao": self.data_publicacao,
            "idioma": self.idioma,
            "tipo": self.tipo,
            "acesso_aberto": self.acesso_aberto,
            "retratado": self.retratado,
            "primeiro_autor": self.primeiro_autor,
            "autores": "; ".join(self.autores),
            "n_autores": self.n_autores,
            "instituicoes": "; ".join(self.instituicoes),
            "paises": "; ".join(self.paises),
            "pais_principal": self.pais_principal,
            "periodico": self.periodico,
            "citacoes": self.citacoes,
            "conceitos": "; ".join(self.conceitos),
            "topicos": "; ".join(self.topicos),
            "abstract": self.abstract,
            "queries_origem": "; ".join(self.queries_origem),
            "areas_origem": "; ".join(self.areas_origem),
        }


class OpenAlexClient:
    """Cliente para a API REST de works da OpenAlex."""

    def __init__(self, mailto: str = "", timeout: int = DEFAULT_TIMEOUT):
        self.mailto = mailto
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": f"Fitness-OpenAlex (mailto:{mailto})" if mailto
                          else "Fitness-OpenAlex",
        })

    @staticmethod
    def reconstruir_abstract(inverted_index: Optional[dict]) -> str:
        """Reconstrói o texto a partir do inverted index {palavra: [posições]}."""
        if not inverted_index:
            return ""
        try:
            posicoes = []
            for palavra, lista_pos in inverted_index.items():
                for p in lista_pos:
                    posicoes.append((p, palavra))
            posicoes.sort(key=lambda x: x[0])
            return " ".join(palavra for _, palavra in posicoes)
        except Exception as e:
            logger.warning(f"Falha ao reconstruir abstract: {e}")
            return ""

    def _parse_artigo(self, registro: dict) -> OpenAlexArticle:
        autorias = registro.get("authorships", []) or []
        autores = [a["author"]["display_name"] for a in autorias
                   if a.get("author") and a["author"].get("display_name")]
        primeiro_autor = autores[0] if autores else None

        instituicoes, paises, pais_principal = [], [], None
        if autorias:
            for inst in autorias[0].get("institutions", []) or []:
                if inst.get("display_name"):
                    instituicoes.append(inst["display_name"])
                if inst.get("country_code"):
                    paises.append(inst["country_code"])
            pais_principal = paises[0] if paises else None

        primary_location = registro.get("primary_location") or {}
        source = primary_location.get("source") or {}
        periodico = source.get("display_name")

        oa = registro.get("open_access") or {}
        acesso_aberto = bool(oa.get("is_oa", False))

        conceitos = [c["display_name"]
                     for c in (registro.get("concepts", []) or [])[:5]
                     if c.get("display_name")]
        topicos = [t["display_name"]
                   for t in (registro.get("topics", []) or [])[:5]
                   if t.get("display_name")]

        return OpenAlexArticle(
            id=registro.get("id", ""),
            doi=registro.get("doi"),
            titulo=registro.get("title", "") or "",
            ano=registro.get("publication_year"),
            data_publicacao=registro.get("publication_date"),
            idioma=registro.get("language"),
            tipo=registro.get("type"),
            acesso_aberto=acesso_aberto,
            retratado=bool(registro.get("is_retracted", False)),
            primeiro_autor=primeiro_autor,
            autores=autores,
            n_autores=len(autores),
            instituicoes=instituicoes,
            paises=paises,
            pais_principal=pais_principal,
            periodico=periodico,
            citacoes=registro.get("cited_by_count", 0) or 0,
            conceitos=conceitos,
            topicos=topicos,
            abstract=self.reconstruir_abstract(
                registro.get("abstract_inverted_index")
            ),
        )

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.RequestException,),
        max_tries=5,
        max_time=120,
    )
    def _fetch_pagina(self, params: dict) -> dict:
        response = self.session.get(
            OPENALEX_BASE_URL, params=params, timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def search(
        self,
        query: str,
        ano_inicio: int = 2015,
        ano_fim: int = 2025,
        max_results: int = 200,
        idiomas: Optional[list] = None,
        tipos: Optional[list] = None,
        per_page: int = DEFAULT_PER_PAGE,
        progress: bool = True,
    ) -> list:
        """
        Busca paginada por cursor. Retorna lista de OpenAlexArticle.

        idiomas=None significa sem filtro de idioma (qualquer língua).
        """
        if tipos is None:
            tipos = ["article", "review"]

        filters = [
            f"from_publication_date:{ano_inicio}-01-01",
            f"to_publication_date:{ano_fim}-12-31",
            f"type:{'|'.join(tipos)}",
            "has_abstract:true",
        ]
        if idiomas:
            filters.append(f"language:{'|'.join(idiomas)}")
        params = {
            "search": query,
            "filter": ",".join(filters),
            "per-page": min(per_page, OPENALEX_PER_PAGE_MAX),
            "select": ",".join(DEFAULT_SELECT_FIELDS),
            "cursor": "*",
        }
        if self.mailto:
            params["mailto"] = self.mailto

        artigos = []
        pbar = tqdm(total=max_results, desc="OpenAlex", disable=not progress)

        while len(artigos) < max_results:
            data = self._fetch_pagina(params)
            results = data.get("results", []) or []
            if not results:
                break
            for registro in results:
                if len(artigos) >= max_results:
                    break
                try:
                    artigos.append(self._parse_artigo(registro))
                    pbar.update(1)
                except Exception as e:
                    logger.warning(f"Falha ao processar registro: {e}")

            next_cursor = data.get("meta", {}).get("next_cursor")
            if not next_cursor:
                break
            params["cursor"] = next_cursor
            time.sleep(0.1)

        pbar.close()
        logger.info(f"Coletados {len(artigos)} trabalhos para: '{query[:50]}'")
        return artigos
