"""
fetch_attrition.py
==================
Descarga el dataset IBM HR Analytics Employee Attrition (o genera datos sintéticos).

Uso:
    python src/fetch_attrition.py

Dataset: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
Si no tienes el CSV, el script genera un dataset sintético realista.
"""

import numpy as np
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)

KAGGLE_FILE = RAW_DIR / "attrition.csv"


def generate_synthetic_attrition(n: int = 1470, seed: int = 42) -> pd.DataFrame:
    """
    Genera un dataset sintético que imita IBM HR Analytics.
    Calibrado para ~16% attrition rate (como el real).
    """
    rng = np.random.default_rng(seed)

    departments = ["Sales", "Research & Development", "Human Resources"]
    dept_weights = [0.30, 0.60, 0.10]

    job_roles = {
        "Sales": ["Sales Executive", "Sales Representative"],
        "Research & Development": ["Research Scientist", "Laboratory Technician",
                                    "Manufacturing Director", "Research Director"],
        "Human Resources": ["Human Resources", "Manager"],
    }

    education_fields = ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Other", "Human Resources"]

    df = pd.DataFrame()
    df["Age"] = rng.integers(18, 60, size=n)
    df["Department"] = rng.choice(departments, size=n, p=dept_weights)
    df["JobRole"] = [rng.choice(job_roles[d]) for d in df["Department"]]
    df["EducationField"] = rng.choice(education_fields, size=n)
    df["Gender"] = rng.choice(["Male", "Female"], size=n)
    df["MaritalStatus"] = rng.choice(["Single", "Married", "Divorced"], size=n, p=[0.32, 0.46, 0.22])

    # Numeric features
    df["DistanceFromHome"] = rng.integers(1, 30, size=n)
    df["Education"] = rng.integers(1, 5, size=n)  # 1-5 scale
    df["MonthlyIncome"] = (rng.lognormal(8.5, 0.6, size=n)).clip(1000, 20000).astype(int)
    df["NumCompaniesWorked"] = rng.integers(0, 10, size=n)
    df["TotalWorkingYears"] = (df["Age"] - 18 - rng.integers(0, 5, size=n)).clip(0, 40)
    df["YearsAtCompany"] = (df["TotalWorkingYears"] * rng.uniform(0.1, 0.8, size=n)).astype(int).clip(0, 40)
    df["YearsInCurrentRole"] = (df["YearsAtCompany"] * rng.uniform(0.2, 0.9, size=n)).astype(int).clip(0, 18)
    df["YearsSinceLastPromotion"] = rng.integers(0, 15, size=n).clip(0, df["YearsAtCompany"])
    df["TrainingTimesLastYear"] = rng.integers(0, 7, size=n)
    df["OverTime"] = rng.choice(["Yes", "No"], size=n, p=[0.28, 0.72])

    # Satisfaction scores (1-4)
    df["JobSatisfaction"] = rng.integers(1, 5, size=n)
    df["EnvironmentSatisfaction"] = rng.integers(1, 5, size=n)
    df["WorkLifeBalance"] = rng.integers(1, 5, size=n)
    df["JobInvolvement"] = rng.integers(1, 5, size=n)
    df["RelationshipSatisfaction"] = rng.integers(1, 5, size=n)
    df["PerformanceRating"] = rng.choice([3, 4], size=n, p=[0.85, 0.15])

    # Attrition: función de features (simula relación real)
    prob = (
        -0.02 * df["Age"]
        + 0.03 * df["DistanceFromHome"]
        - 0.00005 * df["MonthlyIncome"]
        + 0.15 * (df["OverTime"] == "Yes").astype(int)
        - 0.08 * df["JobSatisfaction"]
        - 0.06 * df["WorkLifeBalance"]
        - 0.04 * df["YearsAtCompany"]
        + 0.05 * df["NumCompaniesWorked"]
        + 0.12 * (df["MaritalStatus"] == "Single").astype(int)
        + rng.normal(0, 0.3, size=n)
    )
    # Sigmoid + threshold para ~16% attrition
    prob_sigmoid = 1 / (1 + np.exp(-prob))
    threshold = np.percentile(prob_sigmoid, 84)
    df["Attrition"] = (prob_sigmoid >= threshold).astype(int)
    df["Attrition"] = df["Attrition"].map({1: "Yes", 0: "No"})

    return df


def load_or_generate() -> pd.DataFrame:
    """Carga el CSV real si existe, si no genera datos sintéticos."""
    if KAGGLE_FILE.exists():
        print(f"[OK] Cargando dataset real: {KAGGLE_FILE}")
        df = pd.read_csv(KAGGLE_FILE)
    else:
        print(f"[INFO] No se encontró {KAGGLE_FILE}")
        print("[INFO] Generando dataset sintético (1470 empleados)...")
        print("[TIP]  Descarga el real desde:")
        print("       https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset")
        print(f"       y guárdalo en {KAGGLE_FILE}")
        df = generate_synthetic_attrition()

    out_path = PROC_DIR / "attrition_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"[OK] Dataset guardado: {out_path} ({len(df)} empleados, {df.shape[1]} columnas)")
    attrition_rate = (df["Attrition"] == "Yes").mean() * 100
    print(f"     Attrition rate: {attrition_rate:.1f}%")
    return df


if __name__ == "__main__":
    df = load_or_generate()
    print("\nPrimeras filas:")
    print(df.head())
