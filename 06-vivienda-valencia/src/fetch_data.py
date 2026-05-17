"""
Descarga datos de precios de vivienda en Valencia desde fuentes oficiales.

Fuentes:
  1. MITMA — precios de venta por municipio (CSV descargable)
     https://www.mitma.gob.es/vivienda-y-suelo/informacion-estadistica/estadisticas-de-precios-de-suelo-urbano

  2. INE — Índice de Precios del Alquiler Residencial
     https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177105

  3. GVA datos abiertos — Generalitat Valenciana
     https://dadesobertes.gva.es/
"""

import requests
import pandas as pd
from pathlib import Path
import io

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Municipios de interés (Valencia y zona DANA)
MUNICIPIOS_DANA = [
    "Valencia",       # capital, receptor de desplazados
    "Paiporta",       # municipio más afectado
    "Alfafar",
    "Massanassa",
    "Catarroja",
    "Aldaia",
    "Alaquàs",
    "Picanya",
    "Torrent",        # ciudad grande cercana
]


def fetch_ine_alquiler():
    """
    Descarga el índice de precios del alquiler del INE.
    El INE publica un JSON vía su API estadística.
    """
    print("Descargando Índice de Precios del Alquiler (INE)...")
    # Endpoint API INE — operación IPV (índice precios vivienda en alquiler)
    url = "https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/IPC251?nult=40"
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
        rows = []
        for item in data.get("Data", []):
            rows.append({"fecha": item["Fecha"], "valor": item["Valor"]})
        df = pd.DataFrame(rows)
        if not df.empty:
            df["fecha"] = pd.to_datetime(df["fecha"], unit="ms")
            df = df.sort_values("fecha").reset_index(drop=True)
            out = DATA_DIR / "ine_alquiler.csv"
            df.to_csv(out, index=False)
            print(f"Guardado: {out} ({len(df)} periodos)")
            return df
    except Exception as e:
        print(f"Error INE: {e}")
    return None


def fetch_mitma_precios():
    """
    Descarga precios de suelo urbano del MITMA.
    El ministerio publica CSVs por municipio y año.
    """
    print("Descargando precios MITMA (intentando)...")
    # URL directa al CSV publicado por MITMA (puede cambiar)
    url = "https://www.mitma.gob.es/recursos_mfom/listado/recursos/estadisticas/vivienda/suelo/estadisticas_precios_suelo_urbano_4t2024.csv"
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.content.decode("latin-1")), sep=";", decimal=",")
        out = DATA_DIR / "mitma_precios.csv"
        df.to_csv(out, index=False)
        print(f"Guardado: {out} ({len(df)} filas)")
        return df
    except Exception as e:
        print(f"Error MITMA: {e}")
    return None


if __name__ == "__main__":
    ine = fetch_ine_alquiler()
    mitma = fetch_mitma_precios()

    if ine is None and mitma is None:
        print("\nNo se pudieron descargar datos reales.")
        print("El notebook generará datos sintéticos con estructura de precios valenciana.")
    else:
        if ine is not None:
            print(ine.tail())
