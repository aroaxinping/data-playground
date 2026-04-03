"""
prepare_social_data.py
======================
Unifica datos de TikTok e Instagram en un dataset común para el predictor viral.

Uso:
    python src/prepare_social_data.py

Lee:
  - TikTok:    ~/Desktop/tiktok-analytics-aroaxinping/data/processed/videos_engagement.csv
  - Instagram: ~/Desktop/instagram-analytics-aroaxinping/data/processed/reels_metricas.csv

Genera:
  - data/processed/social_unified.csv (dataset unificado con target is_viral)
"""

import numpy as np
import pandas as pd
from pathlib import Path

PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
PROC_DIR.mkdir(parents=True, exist_ok=True)

# Rutas de datos fuente
TIKTOK_PATH = Path.home() / "Desktop" / "tiktok-analytics-aroaxinping" / "data" / "processed" / "videos_engagement.csv"
INSTAGRAM_PATH = Path.home() / "Desktop" / "instagram-analytics-aroaxinping" / "data" / "processed" / "reels_metricas.csv"


def load_tiktok() -> pd.DataFrame:
    """Carga y normaliza datos de TikTok."""
    if not TIKTOK_PATH.exists():
        print(f"[WARN] TikTok data no encontrada: {TIKTOK_PATH}")
        return pd.DataFrame()

    df = pd.read_csv(TIKTOK_PATH)
    print(f"[OK] TikTok: {len(df)} videos cargados")

    # Normalizar columnas
    out = pd.DataFrame({
        "platform": "tiktok",
        "date": pd.to_datetime(df["published_date"], errors="coerce"),
        "title": df["title"],
        "duration_sec": pd.to_numeric(df["duration_sec"], errors="coerce"),
        "views": pd.to_numeric(df["views"], errors="coerce"),
        "likes": pd.to_numeric(df["likes"], errors="coerce"),
        "comments": pd.to_numeric(df["comments"], errors="coerce"),
        "shares": pd.to_numeric(df["shares"], errors="coerce"),
        "saves": pd.to_numeric(df["saves"], errors="coerce"),
        "engagement_rate": pd.to_numeric(df["engagement_rate_pct"], errors="coerce"),
        "topic": df["topic"],
    })

    return out


def load_instagram() -> pd.DataFrame:
    """Carga y normaliza datos de Instagram."""
    if not INSTAGRAM_PATH.exists():
        print(f"[WARN] Instagram data no encontrada: {INSTAGRAM_PATH}")
        return pd.DataFrame()

    df = pd.read_csv(INSTAGRAM_PATH)
    print(f"[OK] Instagram: {len(df)} reels cargados")

    out = pd.DataFrame({
        "platform": "instagram",
        "date": pd.to_datetime(df["fecha"], errors="coerce"),
        "title": df["descripcion_corta"],
        "duration_sec": pd.to_numeric(df["duracion_seg"], errors="coerce"),
        "views": pd.to_numeric(df["visualizaciones"], errors="coerce"),
        "likes": pd.to_numeric(df["me_gustas"], errors="coerce"),
        "comments": pd.to_numeric(df["comentarios"], errors="coerce"),
        "shares": pd.to_numeric(df["compartidos"], errors="coerce"),
        "saves": pd.to_numeric(df["guardados"], errors="coerce"),
        "engagement_rate": pd.to_numeric(df["engagement_rate"], errors="coerce"),
        "topic": df["tema"],
    })

    return out


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Genera features para el modelo a partir de los datos unificados."""
    df = df.copy()

    # Temporal
    df["day_of_week"] = df["date"].dt.dayofweek  # 0=lunes
    df["hour"] = df["date"].dt.hour if df["date"].dt.hour.notna().any() else np.nan
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    # Texto
    df["title_length"] = df["title"].fillna("").str.len()
    df["num_hashtags"] = df["title"].fillna("").str.count("#")
    df["num_emojis"] = df["title"].fillna("").apply(
        lambda t: sum(1 for c in t if ord(c) > 0x1F600)
    )

    # Topic simplificado
    topic_map = {
        "Tech humor": "tech_humor",
        "Humor personal / relatable": "humor_relatable",
        "Hardware / PC": "hardware",
        "Programación": "programacion",
        "Setup / Accesorios": "setup",
        "Data / Analytics": "data",
        "Women in Tech": "women_in_tech",
    }
    df["topic_clean"] = df["topic"].map(topic_map).fillna("otro")

    return df


def define_viral(df: pd.DataFrame) -> pd.DataFrame:
    """
    Define el target is_viral por plataforma.
    Criterio: views > mediana * 3 para esa plataforma.
    """
    df = df.copy()
    df["is_viral"] = 0

    for platform in df["platform"].unique():
        mask = df["platform"] == platform
        median_views = df.loc[mask, "views"].median()
        threshold = median_views * 3
        df.loc[mask & (df["views"] > threshold), "is_viral"] = 1
        viral_count = df.loc[mask, "is_viral"].sum()
        total = mask.sum()
        print(f"  {platform}: mediana={median_views:.0f}, threshold={threshold:.0f}, "
              f"virales={viral_count}/{total} ({viral_count/max(total,1)*100:.0f}%)")

    return df


def generate_synthetic_social(n_tiktok: int = 15, n_instagram: int = 68, seed: int = 42) -> pd.DataFrame:
    """
    Genera datos sintéticos que imitan la estructura real.
    Para testing cuando no se tienen los datos originales.
    """
    rng = np.random.default_rng(seed)

    topics = ["tech_humor", "humor_relatable", "hardware", "programacion", "setup", "data", "women_in_tech"]
    records = []

    for platform, n, base_views in [("tiktok", n_tiktok, 200_000), ("instagram", n_instagram, 3_000)]:
        for i in range(n):
            views = int(rng.lognormal(np.log(base_views), 1.2))
            records.append({
                "platform": platform,
                "date": pd.Timestamp("2026-02-27") + pd.Timedelta(days=rng.integers(0, 35)),
                "title": f"video_{platform}_{i:02d} #tech #humor",
                "duration_sec": rng.integers(8, 60),
                "views": views,
                "likes": int(views * rng.uniform(0.03, 0.15)),
                "comments": int(views * rng.uniform(0.001, 0.01)),
                "shares": int(views * rng.uniform(0.005, 0.05)),
                "saves": int(views * rng.uniform(0.002, 0.02)),
                "engagement_rate": round(rng.uniform(2, 25), 2),
                "topic": rng.choice(topics),
                "topic_clean": rng.choice(topics),
                "day_of_week": rng.integers(0, 7),
                "hour": rng.integers(8, 22),
                "is_weekend": rng.choice([0, 1], p=[0.7, 0.3]),
                "title_length": rng.integers(20, 200),
                "num_hashtags": rng.integers(1, 8),
                "num_emojis": rng.integers(0, 4),
            })

    return pd.DataFrame(records)


def build_dataset() -> pd.DataFrame:
    """Pipeline completo: cargar → unificar → features → target."""
    tiktok = load_tiktok()
    instagram = load_instagram()

    if tiktok.empty and instagram.empty:
        print("[INFO] Datos reales no encontrados. Generando dataset sintético...")
        df = generate_synthetic_social()
        df = define_viral(df)
        out_path = PROC_DIR / "social_unified.csv"
        df.to_csv(out_path, index=False)
        print(f"\n[OK] Dataset sintético guardado: {out_path} ({len(df)} posts)")
        return df

    # Concatenar
    df = pd.concat([tiktok, instagram], ignore_index=True)
    print(f"\n[OK] Dataset unificado: {len(df)} posts ({tiktok.shape[0]} TikTok + {instagram.shape[0]} Instagram)")

    # Features
    df = engineer_features(df)

    # Target
    print("\nDefiniendo target is_viral (views > mediana * 3):")
    df = define_viral(df)

    # Guardar
    out_path = PROC_DIR / "social_unified.csv"
    df.to_csv(out_path, index=False)
    print(f"\n[OK] Dataset guardado: {out_path}")
    print(f"     Columnas: {df.columns.tolist()}")
    return df


if __name__ == "__main__":
    df = build_dataset()
    print("\nPrimeras filas:")
    print(df.head())
    print(f"\nDistribución is_viral:")
    print(df.groupby("platform")["is_viral"].value_counts())
