"""
fetch_ts_data.py
================
Descarga el dataset de airline passengers (statsmodels) y genera un dataset
sintético de ventas diarias con trend, estacionalidad y anomalías.

Uso:
    python src/fetch_ts_data.py

Datasets:
- Airline Passengers: clásico Box-Jenkins (1949-1960), 144 observaciones mensuales.
- Ventas diarias sintéticas: ~3 años con trend + estacionalidad semanal + mensual + ruido + anomalías.
"""

import numpy as np
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Airline Passengers
# ---------------------------------------------------------------------------

def load_airline_passengers() -> pd.DataFrame:
    """
    Carga el dataset clásico de airline passengers desde statsmodels.
    Si statsmodels no está disponible, genera una versión sintética.
    """
    try:
        import statsmodels.api as sm
        data = sm.datasets.get_rdataset("AirPassengers", "datasets").data
        data.columns = ["month_index", "passengers"]
        # Crear fechas reales (1949-01 a 1960-12)
        data["date"] = pd.date_range(start="1949-01-01", periods=len(data), freq="MS")
        data = data[["date", "passengers"]].copy()
        print(f"[OK] Airline passengers cargado desde statsmodels: {len(data)} meses")
    except Exception:
        print("[INFO] statsmodels no disponible. Generando airline passengers sintético...")
        data = generate_synthetic_airline()
    return data


def generate_synthetic_airline(seed: int = 42) -> pd.DataFrame:
    """Genera un dataset sintético que imita airline passengers (1949-1960)."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start="1949-01-01", periods=144, freq="MS")
    t = np.arange(144)

    # Trend creciente + estacionalidad multiplicativa
    trend = 110 + 2.5 * t
    seasonal = 1 + 0.12 * np.sin(2 * np.pi * t / 12) + 0.05 * np.cos(4 * np.pi * t / 12)
    noise = rng.normal(0, 8, size=144)
    passengers = (trend * seasonal + noise).clip(80, 700).round().astype(int)

    return pd.DataFrame({"date": dates, "passengers": passengers})


# ---------------------------------------------------------------------------
# 2. Ventas diarias sintéticas
# ---------------------------------------------------------------------------

def generate_synthetic_daily_sales(n_days: int = 1095, seed: int = 42) -> pd.DataFrame:
    """
    Genera ~3 años de ventas diarias con:
    - Trend lineal creciente
    - Estacionalidad semanal (más ventas viernes-sábado)
    - Estacionalidad mensual (pico en diciembre, valle en enero)
    - Ruido gaussiano
    - ~10 anomalías (picos/caídas puntuales)
    """
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start="2022-01-01", periods=n_days, freq="D")
    t = np.arange(n_days)

    # Trend
    trend = 200 + 0.15 * t

    # Estacionalidad semanal (0=lunes, 6=domingo)
    day_of_week = np.array([d.weekday() for d in dates])
    weekly_effect = np.where(day_of_week == 4, 30,    # viernes
                   np.where(day_of_week == 5, 50,     # sábado
                   np.where(day_of_week == 6, -20,    # domingo
                   0)))

    # Estacionalidad mensual
    month = np.array([d.month for d in dates])
    monthly_effect = 40 * np.sin(2 * np.pi * (month - 4) / 12)  # pico ~julio
    # Boost diciembre (compras navideñas)
    december_boost = np.where(month == 12, 80, 0)

    # Ruido
    noise = rng.normal(0, 25, size=n_days)

    sales = trend + weekly_effect + monthly_effect + december_boost + noise
    sales = sales.clip(50, None).round(2)

    # Anomalías: ~10 días con picos o caídas extremas
    anomaly_idx = rng.choice(n_days, size=10, replace=False)
    anomaly_type = rng.choice([-1, 1], size=10)
    sales[anomaly_idx] += anomaly_type * rng.uniform(150, 300, size=10)
    sales = sales.clip(0, None).round(2)

    df = pd.DataFrame({"date": dates, "sales": sales})
    # Marcar anomalías para referencia
    df["is_anomaly"] = False
    df.loc[anomaly_idx, "is_anomaly"] = True

    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Airline passengers
    airline = load_airline_passengers()
    out_airline = PROC_DIR / "airline_passengers.csv"
    airline.to_csv(out_airline, index=False)
    print(f"[OK] Guardado: {out_airline} ({len(airline)} filas)")

    # Ventas diarias
    sales = generate_synthetic_daily_sales()
    out_sales = PROC_DIR / "daily_sales.csv"
    sales.to_csv(out_sales, index=False)
    print(f"[OK] Guardado: {out_sales} ({len(sales)} filas, {sales['is_anomaly'].sum()} anomalías)")

    return airline, sales


if __name__ == "__main__":
    airline, sales = main()
    print("\n--- Airline Passengers ---")
    print(airline.head())
    print(f"\n--- Ventas Diarias ---")
    print(sales.head(10))
    print(f"\nEstadísticas ventas:")
    print(sales["sales"].describe())
