"""
fetch_comments.py
=================
Carga y limpia comentarios de TikTok/Instagram para analisis NLP.

Fuentes soportadas:
  - TikTok data export (JSON)
  - Instagram data export (JSON)
  - Generador sintetico (~500 comentarios realistas)

Uso:
    # Desde export de TikTok
    python src/fetch_comments.py --source tiktok --file data/raw/user_data.json

    # Desde export de Instagram
    python src/fetch_comments.py --source instagram --file data/raw/comments.json

    # Generar datos sinteticos
    python src/fetch_comments.py --synthetic
"""

import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. TIKTOK DATA EXPORT
# ---------------------------------------------------------------------------

def load_tiktok_export(filepath: str) -> pd.DataFrame:
    """
    Parsea el export JSON de TikTok (Settings > Privacy > Download your data).
    TikTok exporta los comentarios recibidos en Activity > Comments.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Navegar estructura del export de TikTok
    comments_raw = []
    try:
        # Estructura tipica: Comment > Comments > CommentsList
        comment_section = data.get("Comment", data.get("comment", {}))
        comments_list = comment_section.get("Comments", comment_section.get("comments", {}))
        items = comments_list.get("CommentsList", comments_list.get("commentsList", []))

        for item in items:
            comments_raw.append({
                "texto": item.get("Comment", item.get("comment", "")),
                "fecha": item.get("Date", item.get("date", "")),
                "fuente": "tiktok",
            })
    except (KeyError, AttributeError) as e:
        print(f"[WARN] Estructura de TikTok no reconocida: {e}")
        print("[INFO] Intenta colocar solo la seccion de comentarios en el JSON.")
        return pd.DataFrame()

    df = pd.DataFrame(comments_raw)
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    print(f"[OK] TikTok: {len(df)} comentarios cargados")
    return df


# ---------------------------------------------------------------------------
# 2. INSTAGRAM DATA EXPORT
# ---------------------------------------------------------------------------

def load_instagram_export(filepath: str) -> pd.DataFrame:
    """
    Parsea el export JSON de Instagram (Comments on your posts).
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    comments_raw = []
    # Instagram exporta como lista de posts, cada uno con sus comentarios
    items = data if isinstance(data, list) else data.get("comments_media_comments", [])

    for post in items:
        post_comments = post.get("string_list_data", [])
        for c in post_comments:
            comments_raw.append({
                "texto": c.get("value", ""),
                "fecha": datetime.fromtimestamp(c.get("timestamp", 0)),
                "fuente": "instagram",
            })

    df = pd.DataFrame(comments_raw)
    print(f"[OK] Instagram: {len(df)} comentarios cargados")
    return df


# ---------------------------------------------------------------------------
# 3. GENERADOR SINTETICO
# ---------------------------------------------------------------------------

# Categorias de comentarios tipicos de una creadora tech en espanol
COMMENT_TEMPLATES = {
    "setup": [
        "me encanta tu setup",
        "que teclado es?",
        "que monitor usas?",
        "tu setup es increible",
        "donde compraste ese teclado?",
        "setup goals",
        "el mejor setup que he visto",
        "quiero un setup asi",
        "que mouse es ese?",
        "pasa el link del teclado porfa",
        "de donde es la silla?",
        "setup review completa pls",
        "cuanto te costo todo el setup?",
        "ese escritorio es de ikea?",
        "las luces led de donde son?",
    ],
    "programacion": [
        "code review pls",
        "que lenguaje recomiendas para empezar?",
        "python es lo mejor",
        "en que IDE programas?",
        "como aprendiste a programar?",
        "yo tambien estoy aprendiendo python",
        "ese codigo esta muy limpio",
        "puedes hacer un tutorial de git?",
        "javascript o python?",
        "vscode o neovim?",
        "que extensiones usas en vscode?",
        "haz un video de tu workflow",
        "se nota que sabes lo que haces",
        "me inspiras a aprender a programar",
        "cuanto tiempo llevas programando?",
        "eres mi inspiracion para estudiar programacion",
        "como haces para no desesperarte con los bugs?",
        "full stack o data science?",
        "puedes explicar que es una API?",
        "quiero aprender data science, por donde empiezo?",
    ],
    "data_science": [
        "que es machine learning?",
        "pandas o sql?",
        "ese grafico esta brutal",
        "como limpias los datos?",
        "puedes hacer un video de analisis de datos?",
        "que curso recomiendas de data science?",
        "jupyter notebook ftw",
        "matplotlib o seaborn?",
        "haz mas videos de python para datos",
        "la visualizacion quedo increible",
        "me encanta como explicas los datos",
        "quiero ser data scientist, algun consejo?",
        "con que libreria hiciste ese grafico?",
        "sql es imprescindible",
        "numpy o pandas?",
    ],
    "motivacion": [
        "eres mi inspiracion",
        "sigue asi reina",
        "me motivas a estudiar",
        "gracias por el contenido",
        "nunca pares",
        "el mejor contenido tech en espanol",
        "me encanta tu energia",
        "grande!",
        "increible como siempre",
        "cada video mejor que el anterior",
        "mucho animo con todo",
        "eres un ejemplo a seguir",
        "ojala hubiera encontrado tu cuenta antes",
        "me alegra el dia ver tus videos",
        "lo mejor de mi feed",
        "contenido de calidad",
        "aprendo un monton contigo",
        "no cambies nunca",
    ],
    "preguntas_generales": [
        "de donde eres?",
        "que estudias?",
        "cuantos anos tienes?",
        "haces directos?",
        "cuando subes video nuevo?",
        "tienes twitter?",
        "haces tutoriales?",
        "puedes hacer un video sobre IA?",
        "aceptas colaboraciones?",
        "que portatil usas?",
        "mac o windows?",
        "linux?",
        "cuanto cobras por una collab?",
        "tienes newsletter?",
        "en que universidad estudias?",
    ],
    "criticas_neutras": [
        "el audio se escucha bajo",
        "podrias hablar mas lento?",
        "no se ve bien la pantalla",
        "el video es muy corto",
        "falto explicar mejor esa parte",
        "se corto el video al final",
        "la musica esta muy alta",
        "puedes poner subtitulos?",
        "no entendi la parte del medio",
    ],
    "spam_ruido": [
        "sigueme",
        "follow for follow",
        "like si ves esto en 2026",
        "primero!",
        "...",
        "jajajaja",
        "xd",
        "jajaja",
        "wtf",
    ],
    "emojis_cortos": [
        "fire",
        "top",
        "genial",
        "brutal",
        "wow",
        "dios",
        "guau",
        "crack",
    ],
}

# Emojis frecuentes en comentarios tech
EMOJIS = [
    "\U0001f525", "\u2764\ufe0f", "\U0001f4bb", "\U0001f680",
    "\U0001f60d", "\U0001f44f", "\U0001f64f", "\U0001f4af",
    "\u2728", "\U0001f4a1", "\U0001f389", "\U0001f60e",
    "\U0001f4aa", "\U0001f49c", "\U0001f331", "\U0001f3af",
    "\U0001f916", "\U0001f4c8", "\U0001f4a9", "\U0001f602",
]

# Temas de video simulados
VIDEO_TOPICS = [
    "setup tour", "tutorial python", "mi dia como estudiante",
    "data science 101", "review teclado mecanico", "como aprendi a programar",
    "sql en 60 segundos", "vscode tips", "mi rutina de estudio",
    "analisis de datos con pandas", "github para principiantes",
    "mi experiencia en la UOC", "IA explicada facil",
]


def _add_noise(text: str) -> str:
    """Anade ruido realista a un comentario: emojis, mayusculas, typos."""
    modifications = []

    # 40% probabilidad de anadir emoji(s)
    if random.random() < 0.4:
        n_emojis = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
        emojis = "".join(random.choices(EMOJIS, k=n_emojis))
        if random.random() < 0.5:
            text = emojis + " " + text
        else:
            text = text + " " + emojis

    # 15% todo mayusculas
    if random.random() < 0.15:
        text = text.upper()

    # 20% sin puntuacion final / con puntos suspensivos
    if random.random() < 0.1:
        text = text + "..."
    elif random.random() < 0.1:
        text = text + "!!!"

    # 10% repetir letras (muuuuy bien, increibleee)
    if random.random() < 0.1:
        idx = random.randint(0, max(0, len(text) - 2))
        char = text[idx]
        text = text[:idx] + char * random.randint(2, 5) + text[idx + 1:]

    return text


def generate_synthetic_comments(n: int = 500) -> pd.DataFrame:
    """
    Genera ~n comentarios sinteticos realistas en espanol,
    simulando la audiencia de una creadora tech (@aroaxinping).
    """
    random.seed(42)

    # Distribucion de categorias (ponderada)
    category_weights = {
        "setup": 0.15,
        "programacion": 0.25,
        "data_science": 0.15,
        "motivacion": 0.20,
        "preguntas_generales": 0.10,
        "criticas_neutras": 0.05,
        "spam_ruido": 0.05,
        "emojis_cortos": 0.05,
    }

    categories = list(category_weights.keys())
    weights = list(category_weights.values())

    comments = []
    base_date = datetime(2025, 6, 1)

    for i in range(n):
        cat = random.choices(categories, weights=weights, k=1)[0]
        texto = random.choice(COMMENT_TEMPLATES[cat])
        texto = _add_noise(texto)

        # Fecha aleatoria en los ultimos 10 meses
        days_offset = random.randint(0, 300)
        fecha = base_date + timedelta(days=days_offset, hours=random.randint(0, 23),
                                       minutes=random.randint(0, 59))

        # Asignar video topic aleatorio
        topic = random.choice(VIDEO_TOPICS)

        comments.append({
            "texto": texto,
            "fecha": fecha,
            "fuente": random.choice(["tiktok", "instagram"]),
            "video_topic": topic,
            "categoria_real": cat,  # ground truth para validar
        })

    df = pd.DataFrame(comments)
    print(f"[OK] Sintetico: {n} comentarios generados")
    return df


# ---------------------------------------------------------------------------
# 4. Pipeline principal
# ---------------------------------------------------------------------------

def build_dataset(source: str = None, filepath: str = None, synthetic: bool = False) -> pd.DataFrame:
    """Carga o genera comentarios y guarda en data/processed/."""

    if synthetic or (source is None and filepath is None):
        df = generate_synthetic_comments(500)
    elif source == "tiktok":
        df = load_tiktok_export(filepath)
    elif source == "instagram":
        df = load_instagram_export(filepath)
    else:
        print(f"[ERROR] Fuente no soportada: {source}")
        return pd.DataFrame()

    if df.empty:
        return df

    out_path = PROC_DIR / "comentarios.csv"
    df.to_csv(out_path, index=False)
    print(f"\n[OK] Dataset guardado: {out_path} ({len(df)} filas)")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Carga comentarios para analisis NLP")
    parser.add_argument("--source", choices=["tiktok", "instagram"], default=None,
                        help="Fuente de datos: tiktok o instagram")
    parser.add_argument("--file", default=None, help="Ruta al archivo JSON exportado")
    parser.add_argument("--synthetic", action="store_true",
                        help="Generar dataset sintetico (~500 comentarios)")
    args = parser.parse_args()

    df = build_dataset(source=args.source, filepath=args.file, synthetic=args.synthetic)
    if not df.empty:
        print("\nPrimeras filas:")
        print(df.head())
