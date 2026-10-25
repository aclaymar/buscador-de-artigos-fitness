"""
Script principal da coleta fitness/esportiva via OpenAlex.

Pipeline:
    1. Itera sobre as queries definidas em config.py
    2. Coleta via API OpenAlex (cursor, retry, polite pool)
    3. Salva bruto por query em data/raw/
    4. Deduplica, filtra e classifica (área + desenho do estudo)
    5. Salva dataset final e resumo em data/processed/

Uso:
    python -m src.coleta_fitness
"""
import json
import logging
from datetime import datetime

from .config import (
    QUERIES, ANO_INICIO, ANO_FIM, LIMITE_POR_QUERY,
    OPENALEX_MAILTO, IDIOMAS, IDIOMAS_CONSULTA, TIPOS_DOCUMENTO,
    DATA_RAW_DIR, DATA_PROCESSED_DIR,
)
from .openalex_client import OpenAlexClient
from .processamento import processar_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    print("\n" + "=" * 60)
    print("COLETA OPENALEX — FITNESS E ESPORTE")
    print("=" * 60)
    print(f"Período: {ANO_INICIO} a {ANO_FIM}")
    print(f"Limite por query: {LIMITE_POR_QUERY}")
    print(f"Queries: {len(QUERIES)}")
    idiomas_txt = ", ".join(IDIOMAS) if IDIOMAS else "todos (sem filtro)"
    print(f"Tipos: {', '.join(TIPOS_DOCUMENTO)} | Idiomas: {idiomas_txt}")
    print(f"Idiomas de consulta: {', '.join(IDIOMAS_CONSULTA)}")
    print(f"E-mail (polite pool): {OPENALEX_MAILTO or '(não configurado)'}")
    if not OPENALEX_MAILTO:
        print("\n⚠ AVISO: configure OPENALEX_MAILTO no .env para o polite pool")

    client = OpenAlexClient(mailto=OPENALEX_MAILTO)
    artigos_por_query = {}
    areas_por_query = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for codigo, info in QUERIES.items():
        print(f"\n→ {codigo} [{info['area']} | consulta em {info['idioma_consulta']}]")
        print(f"  Expressão: {info['expressao']}")

        artigos = client.search(
            query=info["expressao"],
            ano_inicio=ANO_INICIO,
            ano_fim=ANO_FIM,
            max_results=LIMITE_POR_QUERY,
            idiomas=IDIOMAS,
            tipos=TIPOS_DOCUMENTO,
        )
        artigos_por_query[codigo] = artigos
        areas_por_query[codigo] = info["area"]

        path_raw = DATA_RAW_DIR / f"{codigo}_{timestamp}.json"
        with open(path_raw, "w", encoding="utf-8") as f:
            json.dump([a.to_dict() for a in artigos], f, ensure_ascii=False, indent=2)
        print(f"  ✓ Salvo: {path_raw.name} ({len(artigos)} trabalhos)")

    df, exclusoes = processar_pipeline(artigos_por_query, areas_por_query)

    csv_path = DATA_PROCESSED_DIR / "fitness_dataset_final.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"\n✓ Dataset final: {csv_path} ({len(df)} trabalhos)")

    resumo = {
        "data_coleta": timestamp,
        "total_final": len(df),
        "exclusoes": exclusoes,
        "periodo": f"{ANO_INICIO}-{ANO_FIM}",
        "queries": {k: {"area": v["area"], "expressao": v["expressao"]}
                    for k, v in QUERIES.items()},
        "distribuicao_area": df["area_principal"].value_counts().to_dict() if len(df) else {},
        "distribuicao_desenho": df["desenho_estudo"].value_counts().to_dict() if len(df) else {},
        "distribuicao_nivel_evidencia": (
            df["nivel_evidencia"].value_counts().sort_index().to_dict() if len(df) else {}
        ),
        "acesso_aberto_pct": float(df["acesso_aberto"].mean() * 100) if len(df) else None,
    }
    json_path = DATA_PROCESSED_DIR / "fitness_resumo.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(resumo, f, ensure_ascii=False, indent=2)
    print(f"✓ Resumo: {json_path}")

    print("\n" + "=" * 60)
    print("COLETA CONCLUÍDA")
    print("=" * 60)


if __name__ == "__main__":
    main()
