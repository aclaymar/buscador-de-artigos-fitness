"""
Configurações centrais da coleta fitness/esportiva.

Estrutura:
    AREAS  -> para cada área, consultas e termos de categorização em cada idioma.
    QUERIES, DICIONARIO_AREAS -> derivados de AREAS (não editar à mão).

A OpenAlex indexa título e abstract no idioma original, então as consultas
são feitas em cada língua, e não só traduzidas no filtro. Sem filtro de
idioma: a coleta traz trabalhos em qualquer língua.

Para ajustar a estratégia, edite apenas AREAS (e os parâmetros abaixo).
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# =============================================================
# CAMINHOS
# =============================================================
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = ROOT_DIR / "data" / "raw"
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"

for _d in [DATA_RAW_DIR, DATA_PROCESSED_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

# =============================================================
# PARÂMETROS DA COLETA
# =============================================================
ANO_INICIO = int(os.getenv("ANO_INICIO", 2015))
ANO_FIM = int(os.getenv("ANO_FIM", 2025))
LIMITE_POR_QUERY = int(os.getenv("LIMITE_POR_QUERY", 200))
TIMEOUT_SEGUNDOS = int(os.getenv("TIMEOUT_SEGUNDOS", 30))

OPENALEX_MAILTO = os.getenv("OPENALEX_MAILTO", "")

# "review" inclui revisões sistemáticas e meta-análises.
TIPOS_DOCUMENTO = ["article", "review"]

# None = sem filtro de idioma (qualquer língua).
# Para restringir, use uma lista de códigos ISO, ex.: ["en", "pt", "es"].
IDIOMAS = None

# Idiomas em que as consultas são feitas.
# en tem duas consultas por área; os demais, uma.
IDIOMAS_CONSULTA = ["en", "pt", "es", "de", "fr", "it", "zh", "ja", "ko", "ru"]


# =============================================================
# ÁREAS: consultas (por idioma) e termos de categorização (por idioma)
# =============================================================
AREAS = {
    "Musculação": {
        "codigo": "MUS",
        "idiomas": {
            "en": {"consultas": ['"resistance training" hypertrophy',
                                 '"strength training" "muscle strength"'],
                   "termos": ["resistance training", "strength training", "weight training",
                              "hypertrophy", "muscle strength", "muscle mass", "powerlifting",
                              "bodybuilding"]},
            "pt": {"consultas": ['"treinamento de força" hipertrofia'],
                   "termos": ["treinamento de força", "treinamento resistido", "musculação",
                              "hipertrofia", "força muscular", "massa muscular"]},
            "es": {"consultas": ['"entrenamiento de fuerza" hipertrofia'],
                   "termos": ["entrenamiento de fuerza", "entrenamiento de resistencia",
                              "hipertrofia", "fuerza muscular", "masa muscular"]},
            "de": {"consultas": ['Krafttraining Hypertrophie'],
                   "termos": ["krafttraining", "widerstandstraining", "hypertrophie",
                              "muskelkraft", "muskelmasse"]},
            "fr": {"consultas": ['"entraînement en force" hypertrophie'],
                   "termos": ["entraînement en force", "entraînement de résistance",
                              "musculation", "hypertrophie", "force musculaire"]},
            "it": {"consultas": ['"allenamento di forza" ipertrofia'],
                   "termos": ["allenamento di forza", "allenamento con i pesi", "ipertrofia",
                              "forza muscolare"]},
            "zh": {"consultas": ['抗阻训练 肌肥大'],
                   "termos": ["抗阻训练", "力量训练", "肌肥大", "肌肉力量", "肌肉量"]},
            "ja": {"consultas": ['レジスタンストレーニング 筋肥大'],
                   "termos": ["レジスタンストレーニング", "筋力トレーニング", "筋肥大", "筋力", "筋肉量"]},
            "ko": {"consultas": ['저항성 운동 근비대'],
                   "termos": ["저항성 운동", "근력 운동", "근비대", "근력", "근육량"]},
            "ru": {"consultas": ['силовые тренировки гипертрофия'],
                   "termos": ["силовые тренировки", "силовая тренировка", "гипертрофия",
                              "мышечная сила", "мышечная масса"]},
        },
    },
    "Triathlon": {
        "codigo": "TRI",
        "idiomas": {
            "en": {"consultas": ['triathlon performance', 'triathlete training'],
                   "termos": ["triathlon", "triathlete", "ironman", "swim bike run"]},
            "pt": {"consultas": ['triatlo desempenho'],
                   "termos": ["triathlon", "triatlo", "triatleta", "triátlon"]},
            "es": {"consultas": ['triatlón rendimiento'],
                   "termos": ["triatlón", "triatleta", "triathlon"]},
            "de": {"consultas": ['Triathlon Leistung'],
                   "termos": ["triathlon", "triathlet"]},
            "fr": {"consultas": ['triathlon performance'],
                   "termos": ["triathlon", "triathlète"]},
            "it": {"consultas": ['triathlon prestazione'],
                   "termos": ["triathlon", "triatleta"]},
            "zh": {"consultas": ['铁人三项 运动员'],
                   "termos": ["铁人三项", "三项全能", "三项铁人"]},
            "ja": {"consultas": ['トライアスロン 競技'],
                   "termos": ["トライアスロン", "トライアスリート"]},
            "ko": {"consultas": ['트라이애슬론 선수'],
                   "termos": ["트라이애슬론", "철인3종"]},
            "ru": {"consultas": ['триатлон спортсмены'],
                   "termos": ["триатлон", "триатлет"]},
        },
    },
    "Hyrox": {
        "codigo": "HYX",
        "idiomas": {
            "en": {"consultas": ['Hyrox', '"hybrid training" "functional fitness"'],
                   "termos": ["hyrox", "hybrid training", "functional fitness", "crossfit",
                              "hybrid athlete"]},
            "pt": {"consultas": ['"treino híbrido" "fitness funcional"'],
                   "termos": ["hyrox", "treino híbrido", "fitness funcional", "crossfit"]},
            "es": {"consultas": ['"entrenamiento híbrido" "fitness funcional"'],
                   "termos": ["hyrox", "entrenamiento híbrido", "fitness funcional", "crossfit"]},
            "de": {"consultas": ['Hybridtraining funktionelles Training'],
                   "termos": ["hyrox", "hybridtraining", "funktionelles training", "crossfit"]},
            "fr": {"consultas": ['"entraînement hybride" "fitness fonctionnel"'],
                   "termos": ["hyrox", "entraînement hybride", "fitness fonctionnel", "crossfit"]},
            "it": {"consultas": ['"allenamento ibrido" "fitness funzionale"'],
                   "termos": ["hyrox", "allenamento ibrido", "fitness funzionale", "crossfit"]},
            "zh": {"consultas": ['混合训练 功能性训练'],
                   "termos": ["混合训练", "功能性健身", "功能性训练"]},
            "ja": {"consultas": ['ハイブリッドトレーニング ファンクショナル'],
                   "termos": ["ハイブリッドトレーニング", "ファンクショナルフィットネス", "クロスフィット"]},
            "ko": {"consultas": ['하이브리드 훈련 기능적 피트니스'],
                   "termos": ["하이브리드 훈련", "기능적 피트니스", "크로스핏"]},
            "ru": {"consultas": ['гибридные тренировки функциональный фитнес'],
                   "termos": ["гибридные тренировки", "функциональный фитнес", "кроссфит"]},
        },
    },
    "Corrida de rua": {
        "codigo": "COR",
        "idiomas": {
            "en": {"consultas": ['"distance running" performance', 'marathon runners injury'],
                   "termos": ["running", "runner", "runners", "marathon", "half marathon",
                              "distance running"]},
            "pt": {"consultas": ['corrida de rua maratona'],
                   "termos": ["corrida", "corredor", "corredores", "maratona", "meia maratona"]},
            "es": {"consultas": ['"carrera a pie" maratón'],
                   "termos": ["carrera a pie", "corredor", "corredores", "maratón"]},
            "de": {"consultas": ['Laufen Marathon Läufer'],
                   "termos": ["laufen", "läufer", "marathon", "straßenlauf"]},
            "fr": {"consultas": ['course à pied marathon'],
                   "termos": ["course à pied", "coureur", "coureurs", "marathon"]},
            "it": {"consultas": ['corsa maratona corridori'],
                   "termos": ["corsa", "corridore", "corridori", "maratona"]},
            "zh": {"consultas": ['跑步 马拉松 跑者'],
                   "termos": ["跑步", "长跑", "马拉松", "跑者"]},
            "ja": {"consultas": ['ランニング マラソン ランナー'],
                   "termos": ["ランニング", "ランナー", "マラソン"]},
            "ko": {"consultas": ['달리기 마라톤 러너'],
                   "termos": ["달리기", "러너", "마라톤"]},
            "ru": {"consultas": ['бег марафон бегуны'],
                   "termos": ["бег", "бегуны", "марафон"]},
        },
    },
    "Nutrição esportiva": {
        "codigo": "NUT",
        "idiomas": {
            "en": {"consultas": ['"sports nutrition" athletes', '"protein intake" "exercise performance"'],
                   "termos": ["sports nutrition", "protein intake", "carbohydrate", "energy intake",
                              "hydration", "recovery nutrition"]},
            "pt": {"consultas": ['"nutrição esportiva" atletas'],
                   "termos": ["nutrição esportiva", "ingestão de proteína", "carboidrato",
                              "hidratação"]},
            "es": {"consultas": ['"nutrición deportiva" atletas'],
                   "termos": ["nutrición deportiva", "ingesta de proteína", "carbohidrato",
                              "hidratación"]},
            "de": {"consultas": ['Sporternährung Athleten'],
                   "termos": ["sporternährung", "proteinzufuhr", "kohlenhydrate", "hydratation"]},
            "fr": {"consultas": ['"nutrition sportive" athlètes'],
                   "termos": ["nutrition sportive", "apport en protéines", "glucides", "hydratation"]},
            "it": {"consultas": ['"nutrizione sportiva" atleti'],
                   "termos": ["nutrizione sportiva", "apporto proteico", "carboidrati", "idratazione"]},
            "zh": {"consultas": ['运动营养 运动员'],
                   "termos": ["运动营养", "蛋白质摄入", "碳水化合物", "补水"]},
            "ja": {"consultas": ['スポーツ栄養 アスリート'],
                   "termos": ["スポーツ栄養", "たんぱく質摂取", "炭水化物", "水分補給"]},
            "ko": {"consultas": ['스포츠 영양 선수'],
                   "termos": ["스포츠 영양", "단백질 섭취", "탄수화물", "수분 보충"]},
            "ru": {"consultas": ['спортивное питание спортсмены'],
                   "termos": ["спортивное питание", "потребление белка", "углеводы", "гидратация"]},
        },
    },
    "Medicina esportiva": {
        "codigo": "MED",
        "idiomas": {
            "en": {"consultas": ['"sports medicine" athletes', '"sports injury" athletes'],
                   "termos": ["sports medicine", "sports injury", "injuries", "return to play",
                              "athletic"]},
            "pt": {"consultas": ['"medicina esportiva" atletas'],
                   "termos": ["medicina esportiva", "medicina do esporte", "lesão esportiva",
                              "lesões", "atletas"]},
            "es": {"consultas": ['"medicina deportiva" atletas'],
                   "termos": ["medicina deportiva", "lesión deportiva", "lesiones", "atletas"]},
            "de": {"consultas": ['Sportmedizin Sportverletzung'],
                   "termos": ["sportmedizin", "sportverletzung", "verletzungen", "sportler"]},
            "fr": {"consultas": ['"médecine du sport" blessures'],
                   "termos": ["médecine du sport", "blessure sportive", "blessures", "sportifs"]},
            "it": {"consultas": ['"medicina dello sport" infortuni'],
                   "termos": ["medicina dello sport", "infortunio sportivo", "infortuni", "atleti"]},
            "zh": {"consultas": ['运动医学 运动损伤'],
                   "termos": ["运动医学", "运动损伤", "运动员"]},
            "ja": {"consultas": ['スポーツ医学 スポーツ外傷'],
                   "termos": ["スポーツ医学", "スポーツ外傷", "アスリート"]},
            "ko": {"consultas": ['스포츠 의학 스포츠 손상'],
                   "termos": ["스포츠 의학", "스포츠 손상", "선수"]},
            "ru": {"consultas": ['спортивная медицина спортивная травма'],
                   "termos": ["спортивная медицина", "спортивная травма", "травмы", "спортсмены"]},
        },
    },
    "Fisioterapia esportiva": {
        "codigo": "FIS",
        "idiomas": {
            "en": {"consultas": ['"sports physiotherapy" OR "sports physical therapy"',
                                 '"sports rehabilitation" athletes'],
                   "termos": ["physiotherapy", "physical therapy", "rehabilitation",
                              "physiotherapist", "tendinopathy", "return to sport"]},
            "pt": {"consultas": ['"fisioterapia esportiva" reabilitação'],
                   "termos": ["fisioterapia", "reabilitação", "tendinopatia", "retorno ao esporte"]},
            "es": {"consultas": ['"fisioterapia deportiva" rehabilitación'],
                   "termos": ["fisioterapia", "rehabilitación", "tendinopatía", "retorno al deporte"]},
            "de": {"consultas": ['Sportphysiotherapie Rehabilitation'],
                   "termos": ["physiotherapie", "rehabilitation", "tendinopathie", "rückkehr zum sport"]},
            "fr": {"consultas": ['"kinésithérapie du sport" rééducation'],
                   "termos": ["kinésithérapie", "physiothérapie", "rééducation", "tendinopathie",
                              "retour au sport"]},
            "it": {"consultas": ['fisioterapia sportiva riabilitazione'],
                   "termos": ["fisioterapia", "riabilitazione", "tendinopatia", "ritorno allo sport"]},
            "zh": {"consultas": ['运动康复 物理治疗'],
                   "termos": ["物理治疗", "康复", "肌腱病", "重返运动"]},
            "ja": {"consultas": ['スポーツ理学療法 リハビリテーション'],
                   "termos": ["理学療法", "リハビリテーション", "腱症", "スポーツ復帰"]},
            "ko": {"consultas": ['스포츠 물리치료 재활'],
                   "termos": ["물리치료", "재활", "건병증", "스포츠 복귀"]},
            "ru": {"consultas": ['спортивная физиотерапия реабилитация спортсменов'],
                   "termos": ["физиотерапия", "реабилитация", "тендинопатия", "возвращение к спорту"]},
        },
    },
    "Ortomolecular esportivo": {
        "codigo": "ORT",
        "idiomas": {
            "en": {"consultas": ['micronutrient athletes', '"dietary supplements" athletes performance'],
                   "termos": ["micronutrient", "vitamin", "vitamin d", "omega-3", "creatine",
                              "dietary supplement", "supplementation", "magnesium", "ergogenic"]},
            "pt": {"consultas": ['micronutrientes atletas suplementação'],
                   "termos": ["micronutriente", "vitamina", "vitamina d", "ômega-3", "creatina",
                              "suplemento alimentar", "suplementação", "magnésio"]},
            "es": {"consultas": ['micronutrientes deportistas suplementación'],
                   "termos": ["micronutriente", "vitamina", "omega-3", "creatina",
                              "suplemento dietético", "suplementación", "magnesio"]},
            "de": {"consultas": ['Mikronährstoffe Athleten Supplementierung'],
                   "termos": ["mikronährstoff", "vitamin", "omega-3", "kreatin",
                              "nahrungsergänzungsmittel", "supplementierung", "magnesium"]},
            "fr": {"consultas": ['micronutriments athlètes supplémentation'],
                   "termos": ["micronutriment", "vitamine", "oméga-3", "créatine",
                              "complément alimentaire", "supplémentation", "magnésium"]},
            "it": {"consultas": ['micronutrienti atleti integrazione'],
                   "termos": ["micronutriente", "vitamina", "omega-3", "creatina",
                              "integratore alimentare", "supplementazione", "magnesio"]},
            "zh": {"consultas": ['微量营养素 运动员 补充剂'],
                   "termos": ["微量营养素", "维生素", "欧米伽3", "肌酸", "膳食补充剂", "补充剂", "镁"]},
            "ja": {"consultas": ['微量栄養素 アスリート サプリメント'],
                   "termos": ["微量栄養素", "ビタミン", "オメガ3", "クレアチン", "サプリメント",
                              "栄養補助食品", "マグネシウム"]},
            "ko": {"consultas": ['미량영양소 선수 보충제'],
                   "termos": ["미량영양소", "비타민", "오메가3", "크레아틴", "영양보충제", "마그네슘"]},
            "ru": {"consultas": ['микронутриенты спортсмены добавки'],
                   "termos": ["микронутриент", "витамин", "омега-3", "креатин",
                              "пищевая добавка", "магний"]},
        },
    },
    "Endocrinologia esportiva": {
        "codigo": "END",
        "idiomas": {
            "en": {"consultas": ['"sports endocrinology" athletes',
                                 '"relative energy deficiency" athletes'],
                   "termos": ["sports endocrinology", "endocrine", "testosterone", "cortisol",
                              "relative energy deficiency", "red-s", "thyroid", "hormone"]},
            "pt": {"consultas": ['"endocrinologia esportiva" atletas'],
                   "termos": ["endocrinologia esportiva", "endocrinologia", "testosterona",
                              "cortisol", "tireoide", "hormônio", "déficit energético relativo"]},
            "es": {"consultas": ['"endocrinología deportiva" atletas'],
                   "termos": ["endocrinología deportiva", "endocrino", "testosterona", "cortisol",
                              "tiroides", "hormona", "déficit energético relativo"]},
            "de": {"consultas": ['Sportendokrinologie Athleten'],
                   "termos": ["sportendokrinologie", "endokrin", "testosteron", "kortisol",
                              "schilddrüse", "hormon", "relatives energiedefizit"]},
            "fr": {"consultas": ['"endocrinologie du sport" athlètes'],
                   "termos": ["endocrinologie du sport", "endocrinien", "testostérone", "cortisol",
                              "thyroïde", "hormone", "déficit énergétique relatif"]},
            "it": {"consultas": ['"endocrinologia dello sport" atleti'],
                   "termos": ["endocrinologia dello sport", "endocrino", "testosterone", "cortisolo",
                              "tiroide", "ormone", "deficit energetico relativo"]},
            "zh": {"consultas": ['运动 内分泌 运动员'],
                   "termos": ["运动内分泌", "内分泌", "睾酮", "皮质醇", "甲状腺", "激素", "相对能量缺乏"]},
            "ja": {"consultas": ['運動 内分泌 アスリート'],
                   "termos": ["運動内分泌", "内分泌", "テストステロン", "コルチゾール", "甲状腺",
                              "ホルモン", "相対的エネルギー不足"]},
            "ko": {"consultas": ['운동 내분비 선수'],
                   "termos": ["운동 내분비", "내분비", "테스토스테론", "코르티솔", "갑상선", "호르몬"]},
            "ru": {"consultas": ['спортивная эндокринология спортсмены'],
                   "termos": ["спортивная эндокринология", "эндокринный", "тестостерон", "кортизол",
                              "щитовидная железа", "гормон", "относительный дефицит энергии"]},
        },
    },
}


# =============================================================
# DERIVADOS (gerados a partir de AREAS)
# =============================================================
# QUERIES: código -> {area, idioma_consulta, expressao}
QUERIES = {}
for _area, _info in AREAS.items():
    for _lang in IDIOMAS_CONSULTA:
        _bloco = _info["idiomas"].get(_lang)
        if not _bloco:
            continue
        for _i, _expr in enumerate(_bloco["consultas"], 1):
            QUERIES[f"{_info['codigo']}_{_lang}{_i}"] = {
                "area": _area,
                "idioma_consulta": _lang,
                "expressao": _expr,
            }

# DICIONARIO_AREAS: área -> lista de termos de todas as línguas
DICIONARIO_AREAS = {
    _area: [t for _bloco in _info["idiomas"].values() for t in _bloco["termos"]]
    for _area, _info in AREAS.items()
}


# =============================================================
# DESENHO DO ESTUDO (nível de evidência, multilíngue)
# =============================================================
# Ordem importa: o primeiro padrão que bate define o desenho.
# nivel_evidencia: 1 = mais forte ... 5 = mais fraco / sem desenho identificado.
DESENHOS_ESTUDO = [
    ("Meta-análise", 1, [
        "meta-analysis", "meta-analyses", "metanalysis", "pooled analysis",
        "meta-análise", "metanálise", "meta-análisis", "metaanálisis", "metaanalyse",
        "méta-analyse", "meta-analisi", "荟萃分析", "メタアナリシス", "메타분석", "метаанализ",
    ]),
    ("Revisão sistemática", 1, [
        "systematic review", "systematic literature review", "scoping review",
        "revisão sistemática", "revisión sistemática", "systematische übersicht",
        "systematische review", "revue systématique", "revisione sistematica",
        "系统综述", "系统评价", "システマティックレビュー", "체계적 문헌고찰",
        "систематический обзор",
    ]),
    ("Ensaio clínico randomizado", 2, [
        "randomized controlled trial", "randomised controlled trial", "randomized clinical trial",
        "randomized trial", "randomised trial", "rct",
        "ensaio clínico randomizado", "ensayo clínico aleatorizado",
        "randomisierte kontrollierte studie", "essai contrôlé randomisé",
        "studio randomizzato controllato", "随机对照试验", "ランダム化比較試験",
        "무작위 대조 시험", "рандомизированное контролируемое исследование",
    ]),
    ("Coorte", 3, [
        "cohort study", "prospective cohort", "retrospective cohort", "longitudinal cohort",
        "estudo de coorte", "estudio de cohorte", "kohortenstudie", "étude de cohorte",
        "studio di coorte", "队列研究", "コホート研究", "코호트 연구",
        "когортное исследование",
    ]),
    ("Caso-controle", 3, [
        "case-control", "case control", "caso-controle", "caso-control",
        "fall-kontroll", "cas-témoins", "caso-controllo", "病例对照", "症例対照研究",
        "환자-대조군", "исследование случай-контроль",
    ]),
    ("Transversal", 4, [
        "cross-sectional", "cross sectional", "survey study",
        "transversal", "querschnittsstudie", "étude transversale", "studio trasversale",
        "横断研究", "横断研究", "단면 연구", "поперечное исследование",
    ]),
    ("Revisão narrativa", 5, [
        "narrative review", "literature review", "review of",
        "revisão narrativa", "revisión narrativa", "narrative übersicht",
        "revue narrative", "revisione narrativa", "综述", "総説", "종설", "обзор литературы",
    ]),
]
DESENHO_NAO_IDENTIFICADO = ("Não identificado", 5)


# =============================================================
# CRITÉRIOS DE FILTRAGEM
# =============================================================
# Filtro de foco técnico (opcional, desligado por padrão).
FILTRO_TECNICO = False
TERMOS_TECNICOS = [
    "finite element", "computational fluid", "neural network architecture",
    "machine learning model", "sensor calibration", "signal processing",
]
MIN_CARACTERES_ABSTRACT = 50


# =============================================================
# CONFIGURAÇÃO DOS GRÁFICOS (mesma paleta do TCC)
# =============================================================
PLOT_CONFIG = {
    "dpi": 300,
    "figsize_default": (9, 5.5),
    "font_family": "DejaVu Sans",
    "color_primary": "#2C5F9B",
    "color_secondary": "#B85C38",
    "color_tertiary": "#6B4E9E",
    "palette": "viridis",
}
