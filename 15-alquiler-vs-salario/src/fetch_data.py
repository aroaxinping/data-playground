"""
fetch_data.py — Descarga datos INE de salarios por CCAA y genera datos sintéticos de alquiler.

Uso:
    python src/fetch_data.py

Descarga:
    - INE Encuesta Estructura Salarial (tabla 10882) → data/ine_salarios.json
    - Precios alquiler conocidos 2024 → data/alquiler_ciudades.json
"""

import requests
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

INE_URL = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/10882?nult=5"


def fetch_ine_salarios():
    """Descarga salarios medianos por CCAA desde la API JSON del INE."""
    print("Descargando datos INE tabla 10882...")
    try:
        resp = requests.get(INE_URL, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        out_path = os.path.join(DATA_DIR, 'ine_salarios.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Guardado en: {}".format(out_path))
        return True
    except Exception as e:
        print("No se pudo descargar datos INE: {}".format(e))
        print("El notebook usará salarios hardcodeados de informes INE 2024.")
        return False


def generate_alquiler_data():
    """
    Genera datos de alquiler por ciudad (2024).
    Fuentes: Idealista, Fotocasa, datos de prensa especializada.
    No existe API pública de Idealista, se usan valores de referencia documentados.
    """
    alquiler_2024 = {
        "ciudades": [
            {"ciudad": "Madrid", "ccaa": "Comunidad de Madrid", "alquiler_medio_mes": 1800},
            {"ciudad": "Barcelona", "ccaa": "Cataluña", "alquiler_medio_mes": 1700},
            {"ciudad": "Palma", "ccaa": "Islas Baleares", "alquiler_medio_mes": 1300},
            {"ciudad": "Bilbao", "ccaa": "País Vasco", "alquiler_medio_mes": 1200},
            {"ciudad": "Málaga", "ccaa": "Andalucía", "alquiler_medio_mes": 1100},
            {"ciudad": "Valencia", "ccaa": "Comunitat Valenciana", "alquiler_medio_mes": 1000},
            {"ciudad": "Donostia-San Sebastián", "ccaa": "País Vasco", "alquiler_medio_mes": 1350},
            {"ciudad": "Sevilla", "ccaa": "Andalucía", "alquiler_medio_mes": 900},
            {"ciudad": "Vitoria-Gasteiz", "ccaa": "País Vasco", "alquiler_medio_mes": 1050},
            {"ciudad": "Pamplona", "ccaa": "Comunidad Foral de Navarra", "alquiler_medio_mes": 980},
            {"ciudad": "Zaragoza", "ccaa": "Aragón", "alquiler_medio_mes": 750},
            {"ciudad": "Valladolid", "ccaa": "Castilla y León", "alquiler_medio_mes": 700},
            {"ciudad": "Santander", "ccaa": "Cantabria", "alquiler_medio_mes": 750},
            {"ciudad": "Murcia", "ccaa": "Región de Murcia", "alquiler_medio_mes": 650},
            {"ciudad": "Córdoba", "ccaa": "Andalucía", "alquiler_medio_mes": 700},
            {"ciudad": "Alicante", "ccaa": "Comunitat Valenciana", "alquiler_medio_mes": 850},
            {"ciudad": "Granada", "ccaa": "Andalucía", "alquiler_medio_mes": 780},
            {"ciudad": "Las Palmas de Gran Canaria", "ccaa": "Canarias", "alquiler_medio_mes": 950},
            {"ciudad": "Santa Cruz de Tenerife", "ccaa": "Canarias", "alquiler_medio_mes": 900},
            {"ciudad": "Logroño", "ccaa": "La Rioja", "alquiler_medio_mes": 680}
        ],
        "fuente": "Datos conocidos 2024 — Idealista, Fotocasa, prensa especializada",
        "nota": "Alquiler piso 2 habitaciones, zona no céntrica. Precios aproximados de referencia.",
        "anno": 2024
    }

    out_path = os.path.join(DATA_DIR, 'alquiler_ciudades.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(alquiler_2024, f, ensure_ascii=False, indent=2)
    print("Datos de alquiler guardados en: {}".format(out_path))


if __name__ == '__main__':
    fetch_ine_salarios()
    generate_alquiler_data()
    print("\nDatos listos. Ejecuta el notebook para el análisis completo.")
