# Coleta Bibliométrica Fitness e Esporte (OpenAlex)

Versão da lógica do TCC (`tcc-univesp`) voltada a artigos científicos de:

- Musculação
- Triathlon
- Hyrox
- Corrida de rua
- Nutrição esportiva
- Medicina esportiva
- Fisioterapia esportiva
- Ortomolecular esportivo

## O que muda em relação ao TCC

| Aspecto | TCC (usuários de IA) | Fitness |
|---|---|---|
| Tipos de documento | só `article` | `article` + `review` (inclui meta-análises e revisões sistemáticas) |
| Período | 2020–2025 | 2015–2025 (amostra mais longa para evidência consolidada) |
| Eixo de categorização | 9 contextos de uso | 8 áreas esportivas |
| Qualidade da evidência | não havia | **desenho do estudo + nível de evidência** (1 a 5) |
| Retratados | ignorados | **excluídos** (`is_retracted`) |
| Tópicos OpenAlex | não | campo `topicos` incluído |
| Casamento de termos | substring | **limite de palavra** (evita falsos positivos) |

## Estrutura

Repositório: https://github.com/aclaymar/buscador-de-artigos-fitness

```
.
├── README.md
├── requirements.txt
├── .env.example
├── notebooks/
│   └── 01_coleta_fitness_openalex.ipynb   # versão Colab (autocontida)
└── src/
    ├── config.py              # queries por área, dicionários, desenho do estudo
    ├── openalex_client.py     # cliente genérico da API (cursor + retry)
    ├── processamento.py       # deduplicação, filtro, área, desenho do estudo
    └── coleta_fitness.py      # script principal
```

## Como rodar

### Colab (recomendado)
Abra `notebooks/01_coleta_fitness_openalex.ipynb`, troque o e-mail em `OPENALEX_MAILTO` e execute as células.

### Local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # preencha OPENALEX_MAILTO
python -m src.coleta_fitness
```

Saídas em `data/processed/`:
- `fitness_dataset_final.csv`
- `fitness_resumo.json`

Bruto por query em `data/raw/`.

## Como adaptar

- **Consultas:** edite `QUERIES` em `src/config.py`. Cada área tem duas consultas.
- **Área:** ajuste `DICIONARIO_AREAS`.
- **Evidência:** ajuste `DESENHOS_ESTUDO`, se quiser outra hierarquia.
- **Filtro técnico:** ative `FILTRO_TECNICO = True` e ajuste `TERMOS_TECNICOS`.

## Limitações conhecidas

- Classificação por palavras-chave: é transparente e reproduzível, mas sensível a variação léxica. Recomenda-se revisar uma amostra manual.
- Consultas em inglês concentram a amostra; termos em português quase não aparecem na OpenAlex.
- O nível de evidência é inferido do título e abstract, não de leitura do texto completo.
- Esta coleta gera dados para pesquisa. Ela não substitui avaliação clínica, e os resultados devem ser validados antes de virar recomendação ao atleta.

## Licença

Dados da OpenAlex: CC0. Código: escolha a licença que preferir.
