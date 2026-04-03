"""
fetch_ab_data.py
================
Genera datos sinteticos de un experimento A/B en e-commerce.

Escenario: un sitio de e-commerce prueba dos disenos de boton de checkout.
- Control: boton original (gris, "Finalizar compra")
- Treatment: boton nuevo (naranja, "Comprar ahora")

~10,000 usuarios por grupo, conversion ~3.2% control vs ~3.8% treatment.

Uso:
    python src/fetch_ab_data.py
"""

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# CONFIGURACION DEL EXPERIMENTO
# ---------------------------------------------------------------------------

CONTROL_CONVERSION_RATE = 0.032      # 3.2% (same for both devices)
TREATMENT_CONVERSION_RATE = 0.038    # 3.8% (base, overridden per device below)
USERS_PER_GROUP = 10_000

COUNTRIES = ['ES', 'MX', 'AR', 'CO', 'CL', 'PE', 'US']
COUNTRY_WEIGHTS = [0.30, 0.25, 0.15, 0.10, 0.08, 0.05, 0.07]

# Simpson's paradox setup:
# Control gets a balanced device split (65% mobile / 35% desktop).
# Treatment gets an UNBALANCED split skewed towards desktop (40% mobile / 60% desktop).
# Combined with device-specific rates below, this creates a paradox where:
#   - Desktop: treatment WORSE than control (3.0% vs 3.2%)
#   - Mobile:  treatment BETTER than control (4.5% vs 3.2%)
#   - Overall: treatment wins (because mobile lift is large enough)
DEVICE_SPLIT_CONTROL   = {'mobile': 0.65, 'desktop': 0.35}
DEVICE_SPLIT_TREATMENT = {'mobile': 0.40, 'desktop': 0.60}

# Per-device conversion rates for Simpson's paradox
TREATMENT_RATE_DESKTOP = 0.030   # 3.0% — worse than control's 3.2%
TREATMENT_RATE_MOBILE  = 0.045   # 4.5% — better than control's 3.2%

# Sesion media en segundos (mobile tiende a ser mas corta)
SESSION_DURATION_PARAMS = {
    'mobile':  {'mean': 180, 'std': 90},
    'desktop': {'mean': 260, 'std': 120},
}


# ---------------------------------------------------------------------------
# GENERADOR
# ---------------------------------------------------------------------------

def generate_ab_data(
    n_per_group: int = USERS_PER_GROUP,
    control_rate: float = CONTROL_CONVERSION_RATE,
    treatment_rate: float = TREATMENT_CONVERSION_RATE,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Genera un dataset sintetico de A/B test con ~n_per_group usuarios por grupo.

    La diferencia es sutil pero estadisticamente significativa con n=10k.
    Incluye heterogeneidad por device y country para analisis de segmentacion.
    """
    rng = np.random.default_rng(seed)
    random.seed(seed)

    total = n_per_group * 2
    records = []

    # Asignar grupos (primera mitad control, segunda treatment, luego shuffle)
    groups = ['control'] * n_per_group + ['treatment'] * n_per_group

    # Fecha base del experimento: 2 semanas
    experiment_start = datetime(2026, 3, 1)
    experiment_days = 14

    for i in range(total):
        group = groups[i]

        # Device — different split per group to create Simpson's paradox
        if group == 'control':
            device_split = DEVICE_SPLIT_CONTROL
        else:
            device_split = DEVICE_SPLIT_TREATMENT

        device = rng.choice(
            list(device_split.keys()),
            p=list(device_split.values()),
        )

        # Country
        country = rng.choice(COUNTRIES, p=COUNTRY_WEIGHTS)

        # Conversion rate per group x device (Simpson's paradox)
        if group == 'control':
            # Control: same base rate regardless of device
            effective_rate = control_rate
        else:
            # Treatment: different rate per device
            if device == 'desktop':
                effective_rate = TREATMENT_RATE_DESKTOP   # 3.0% — worse than control
            else:
                effective_rate = TREATMENT_RATE_MOBILE    # 4.5% — better than control

        # Ligera variacion por pais (ES y MX convierten mas)
        if country in ('ES', 'MX'):
            effective_rate *= 1.05
        elif country in ('US',):
            effective_rate *= 0.90

        converted = int(rng.random() < effective_rate)

        # Session duration
        params = SESSION_DURATION_PARAMS[device]
        duration = max(10, rng.normal(params['mean'], params['std']))

        # Los convertidos tienden a tener sesiones ligeramente mas largas
        if converted:
            duration *= rng.uniform(1.1, 1.4)

        # Timestamp aleatorio dentro del periodo del experimento
        ts = experiment_start + timedelta(
            days=rng.uniform(0, experiment_days),
            hours=rng.integers(0, 24),
            minutes=rng.integers(0, 60),
        )

        records.append({
            'user_id': f'u_{i+1:06d}',
            'group': group,
            'converted': converted,
            'session_duration_sec': round(duration, 1),
            'device': device,
            'country': country,
            'timestamp': ts,
        })

    df = pd.DataFrame(records)

    # Shuffle para que no esten ordenados por grupo
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    print(f"[OK] A/B data generada: {len(df)} usuarios ({n_per_group} por grupo)")
    print(f"     Control:   {df[df['group']=='control']['converted'].mean()*100:.2f}% conversion")
    print(f"     Treatment: {df[df['group']=='treatment']['converted'].mean()*100:.2f}% conversion")

    return df


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def build_dataset(n_per_group: int = USERS_PER_GROUP, seed: int = 42) -> pd.DataFrame:
    """Genera el dataset y lo guarda en data/processed/."""
    df = generate_ab_data(n_per_group=n_per_group, seed=seed)

    out_path = PROC_DIR / "ab_test_data.csv"
    df.to_csv(out_path, index=False)
    print(f"\n[OK] Dataset guardado: {out_path} ({len(df)} filas)")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera datos sinteticos de A/B test")
    parser.add_argument("--n", type=int, default=USERS_PER_GROUP,
                        help="Usuarios por grupo (default: 10000)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Seed para reproducibilidad")
    args = parser.parse_args()

    df = build_dataset(n_per_group=args.n, seed=args.seed)
    print("\nPrimeras filas:")
    print(df.head(10))
