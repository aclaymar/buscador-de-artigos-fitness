"""
Processamento dos trabalhos coletados.

Etapas:
    1. Deduplicação por OpenAlex ID (guarda quais queries e áreas encontraram cada trabalho)
    2. Filtragem: abstract mínimo, exclusão de retratados (e foco técnico, se ativado)
    3. Classificação por área temática (palavras-chave, com limites de palavra)
    4. Classificação do desenho do estudo e nível de evidência
"""
import re
import logging
from collections import Counter

import pandas as pd

from .config import (
    DICIONARIO_AREAS,
    DESENHOS_ESTUDO,
    DESENHO_NAO_IDENTIFICADO,
    TERMOS_TECNICOS,
    FILTRO_TECNICO,
    MIN_CARACTERES_ABSTRACT,
)

logger = logging.getLogger(__name__)


# =============================================================
# DEDUPLICAÇÃO
# =============================================================
def deduplicar(artigos_por_query: dict, areas_por_query: dict) -> list:
    """
    Remove duplicatas mantendo as queries e as áreas que recuperaram cada trabalho.

    Args:
        artigos_por_query: {codigo_query: [OpenAlexArticle, ...]}
        areas_por_query:   {codigo_query: "nome da área"}
    """
    unicos = {}
    for codigo, lista in artigos_por_query.items():
        area = areas_por_query.get(codigo, "")
        for artigo in lista:
            if artigo.id not in unicos:
                artigo.queries_origem = [codigo]
                artigo.areas_origem = [area]
                unicos[artigo.id] = artigo
            else:
                existente = unicos[artigo.id]
                if codigo not in existente.queries_origem:
                    existente.queries_origem.append(codigo)
                if area not in existente.areas_origem:
                    existente.areas_origem.append(area)

    total = sum(len(v) for v in artigos_por_query.values())
    logger.info(f"Deduplicação: {total} → {len(unicos)} trabalhos únicos")
    return list(unicos.values())


# =============================================================
# FILTRAGEM
# =============================================================
_CJK = re.compile(r"[぀-ヿ㐀-鿿가-힯]")


def _contem_termo(texto_lower: str, termo: str) -> bool:
    """
    Busca o termo no texto.

    Para termos em alfabeto latino/cirílico usa limite de palavra (evita
    falsos positivos, ex.: 'run' em 'brunch'). Para chinês, japonês e coreano,
    que não separam palavras por espaço, usa busca por substring.
    """
    if _CJK.search(termo):
        return termo in texto_lower
    return re.search(rf"\b{re.escape(termo)}\b", texto_lower) is not None


def tem_foco_tecnico(texto: str) -> bool:
    t = texto.lower()
    return any(_contem_termo(t, termo) for termo in TERMOS_TECNICOS)


def filtrar_artigos(artigos: list) -> tuple:
    """
    Critérios de inclusão/exclusão:
      - abstract com pelo menos MIN_CARACTERES_ABSTRACT caracteres
      - não retratado
      - (opcional) sem foco puramente técnico

    Returns:
        (incluidos, contagem_de_exclusoes)
    """
    incluidos = []
    excl = Counter()

    for artigo in artigos:
        if not artigo.abstract or len(artigo.abstract) < MIN_CARACTERES_ABSTRACT:
            excl["sem abstract válido"] += 1
            continue
        if artigo.retratado:
            excl["retratado"] += 1
            continue
        if FILTRO_TECNICO and tem_foco_tecnico(f"{artigo.titulo} {artigo.abstract}"):
            excl["foco técnico"] += 1
            continue
        incluidos.append(artigo)

    logger.info(f"Filtragem: {len(artigos)} → {len(incluidos)} incluídos ({dict(excl)})")
    return incluidos, dict(excl)


# =============================================================
# CLASSIFICAÇÃO POR ÁREA
# =============================================================
def classificar_area(texto: str) -> tuple:
    """
    Retorna (área principal, áreas secundárias, contagens).
    A área principal é a de maior número de termos encontrados.
    """
    t = texto.lower()
    contagens = {}
    for area, termos in DICIONARIO_AREAS.items():
        n = sum(1 for termo in termos if _contem_termo(t, termo))
        if n > 0:
            contagens[area] = n

    if not contagens:
        return "Outros", [], {}

    ordenadas = sorted(contagens.items(), key=lambda x: x[1], reverse=True)
    principal = ordenadas[0][0]
    secundarias = [a for a, _ in ordenadas[1:]]
    return principal, secundarias, contagens


# =============================================================
# CLASSIFICAÇÃO DO DESENHO DO ESTUDO
# =============================================================
def classificar_desenho(texto: str) -> tuple:
    """Retorna (desenho, nivel_evidencia) pelo primeiro padrão que bate."""
    t = texto.lower()
    for nome, nivel, padroes in DESENHOS_ESTUDO:
        if any(_contem_termo(t, p) for p in padroes):
            return nome, nivel
    return DESENHO_NAO_IDENTIFICADO


# =============================================================
# DATAFRAME FINAL
# =============================================================
def aplicar_classificacoes(artigos: list) -> pd.DataFrame:
    registros = []
    for artigo in artigos:
        texto = f"{artigo.titulo} {artigo.abstract}"
        area, secundarias, _ = classificar_area(texto)
        desenho, nivel = classificar_desenho(texto)

        registro = artigo.to_dict()
        registro["area_principal"] = area
        registro["areas_secundarias"] = "; ".join(secundarias)
        registro["desenho_estudo"] = desenho
        registro["nivel_evidencia"] = nivel
        registros.append(registro)

    df = pd.DataFrame(registros)
    if not df.empty:
        logger.info("Distribuição por área:\n" + df["area_principal"].value_counts().to_string())
    return df


# =============================================================
# PIPELINE COMPLETO
# =============================================================
def processar_pipeline(artigos_por_query: dict, areas_por_query: dict) -> tuple:
    """
    Executa deduplicar → filtrar → classificar.

    Returns:
        (DataFrame final, dict com contagem de exclusões)
    """
    print("\n" + "=" * 60)
    print("PIPELINE DE PROCESSAMENTO")
    print("=" * 60)

    print("\n[1/3] Deduplicação...")
    unicos = deduplicar(artigos_por_query, areas_por_query)

    print("\n[2/3] Filtragem...")
    incluidos, exclusoes = filtrar_artigos(unicos)

    print("\n[3/3] Classificação por área e desenho do estudo...")
    df = aplicar_classificacoes(incluidos)

    print(f"\n✓ Pipeline concluído: {len(df)} trabalhos finais")
    return df, exclusoes
