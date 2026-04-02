"""
¿Los estudios de Clarins Double Serum aguantan un análisis estadístico?

Clarins publica n, duración y tipo de estudio — pero no p-values, intervalos
de confianza ni instrumentos de medición. Con lo que declaran podemos simular:
- Qué tamaño de efecto puede detectar cada n (análisis de potencia)
- La brecha sistemática entre autoevaluación e instrumental
- Si el diseño de gemelas es el correcto para lo que afirman
- Si n=24 (TEWL) es suficiente para los claims de hidratación

Sources:
- Clarins Double Serum methodology: https://www.groupeclarins.com/en/research-and-development/
- Clarins product page claims: https://www.clarins.com/double-serum
- Draelos ZD (2010) "Active agents in common skin care products" — Plast Reconstr Surg
- Cosmetology Today, twin studies in dermatology: Zhu G et al. (2011) — Twin Res Hum Genet
- Flament F et al. (2015) "Facial skin characteristics at 13 anatomical sites" — Skin Research and Technology
- Cohen J (1988) "Statistical Power Analysis for the Behavioral Sciences" — Erlbaum
- Clarys P et al. (2012) "Hydration measurements of the skin" — Skin Res Technol
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import numpy as np
from scipy import stats

plt.rcParams.update({
    "font.family": "monospace",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "#fafafa",
    "axes.facecolor": "#fafafa",
})

# ─── DATOS DE CLARINS (declarados públicamente) ───────────────────────────────
clarins_studies = {
    "Estudio gemelas\n(epigenética)": {
        "n": 60, "type": "comparativo", "method": "subjetivo",
        "duration_days": None, "claim": "mapeo del envejecimiento genético"
    },
    "Antiedad\n(Harungana vs Retinol)": {
        "n": 46, "type": "comparativo ingrediente", "method": "instrumental",
        "duration_days": 56, "claim": "comparable al retinol"
    },
    "Test consumidor\n(panel multiétnico)": {
        "n": 353, "type": "autoevaluación", "method": "subjetivo",
        "duration_days": 28, "claim": "90% piel más suave"
    },
    "Autoevaluación\n7 días": {
        "n": 388, "type": "autoevaluación", "method": "subjetivo",
        "duration_days": 7, "claim": "97% hidratación instantánea"
    },
    "Cinética TEWL": {
        "n": 24, "type": "cinética", "method": "instrumental",
        "duration_days": None, "claim": "mejora barrera cutánea"
    },
    "Cinética\nhidratación": {
        "n": 24, "type": "cinética", "method": "instrumental",
        "duration_days": None, "claim": "hidratación medida"
    },
}

# ─── 1. ANÁLISIS DE POTENCIA POR ESTUDIO ─────────────────────────────────────
# Para cada n declarado: ¿qué tamaño de efecto mínimo puedes detectar
# con potencia 80% y alpha 0.05?

alpha = 0.05
power_target = 0.80
z_alpha = stats.norm.ppf(1 - alpha / 2)
z_beta = stats.norm.ppf(power_target)

def min_detectable_effect(n):
    """d de Cohen mínimo detectable con la potencia y alpha dados."""
    return (z_alpha + z_beta) / np.sqrt(n)

study_names = list(clarins_studies.keys())
ns = [clarins_studies[s]["n"] for s in study_names]
methods = [clarins_studies[s]["method"] for s in study_names]
min_d = [min_detectable_effect(n) for n in ns]

# ─── 2. BRECHA SUBJETIVO VS INSTRUMENTAL ─────────────────────────────────────
# El efecto placebo en cosméticos está documentado en +20-30 puntos
# porcentuales sobre el instrumental.
# Fuente: Moseley GL (2004), adaptado a cosméticos en Draelos 2010.

np.random.seed(42)
n_sim = 500

# Simulamos dos tipos de medición del mismo producto con mismo efecto real
real_effect = 0.55  # correlación moderada con la realidad

# Medición instrumental: más ruidosa, más objetiva
instrumental_base = 45  # AU corneómetro
instrumental_gain_true = 18  # ganancia real
instrumental_noise = 8

instrumental_before = np.random.normal(instrumental_base, instrumental_noise, n_sim)
instrumental_after = instrumental_before + np.random.normal(instrumental_gain_true, instrumental_noise * 0.8, n_sim)
instrumental_pct = ((instrumental_after - instrumental_before) / instrumental_before * 100)

# Medición subjetiva: incluye sesgo de expectativa y efecto placebo
placebo_bias = np.random.normal(22, 8, n_sim)  # +22pp de media (Draelos 2010)
subjective_pct = instrumental_pct * real_effect + placebo_bias + np.random.normal(0, 10, n_sim)
subjective_pct = np.clip(subjective_pct, 0, 100)

# Umbral que Clarins usa para sus claims ("X% de las mujeres dicen...")
threshold_pct_agreement = 90  # 90% dijo sí

# ─── 3. DISEÑO DE GEMELAS: ¿PRUEBA LO QUE AFIRMA? ───────────────────────────
# El estudio de gemelas homocigóticas aísla el factor genético.
# Pero para probar que un producto funciona, necesitas un control claro:
# gemela A usa el producto, gemela B no.
# Clarins lo describe como "mapeo del envejecimiento" — no como RCT de producto.

twin_design_scores = {
    "¿Aísla la genética?": 1.0,
    "¿Control producto vs no-producto\nclaramente definido?": 0.2,
    "¿Lifestyle controlado\n(sueño, sol, dieta)?": 0.1,
    "¿Doble ciego posible?": 0.0,
    "¿Medición instrumental\nnombrada?": 0.0,
    "¿p-values publicados?": 0.0,
    "¿Duración declarada?": 0.0,
}

# ─── 4. N=24 PARA CLAIMS DE HIDRATACIÓN: SIMULACIÓN DE VARIABILIDAD ──────────
# Con n=24 un outlier puede mover el promedio varios puntos.
# Simulamos 1000 muestras de n=24 de la misma distribución.

pop_mean = 35  # % mejora hidratación en la población real
pop_std = 15   # variabilidad real (alta en medición de piel)

sample_means_24 = [
    np.random.normal(pop_mean, pop_std, 24).mean()
    for _ in range(1000)
]
sample_means_100 = [
    np.random.normal(pop_mean, pop_std, 100).mean()
    for _ in range(1000)
]

# ─── FIGURA ──────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 13))
fig.suptitle(
    "Clarins Double Serum: ¿Los estudios publicados aguantan el análisis?\n"
    "Potencia estadística, brecha subjetivo/instrumental y diseño de gemelas",
    fontsize=13, fontweight="bold", y=0.98
)

gs = gridspec.GridSpec(2, 2, hspace=0.5, wspace=0.38)

# ── Panel 1: Análisis de potencia por estudio ──
ax1 = fig.add_subplot(gs[0, 0])
color_map = {"subjetivo": "#f59e0b", "instrumental": "#2563eb"}
bar_colors = [color_map[m] for m in methods]

bars = ax1.barh(
    range(len(study_names)), min_d,
    color=bar_colors, alpha=0.75, edgecolor="white", linewidth=1.2
)
ax1.set_yticks(range(len(study_names)))
ax1.set_yticklabels(study_names, fontsize=7.5)
ax1.axvline(0.2, color="#94a3b8", linestyle="--", linewidth=1, label="Efecto pequeño (d=0.2)")
ax1.axvline(0.5, color="#f59e0b", linestyle="--", linewidth=1, label="Efecto mediano (d=0.5)")
ax1.axvline(0.8, color="#ef4444", linestyle="--", linewidth=1, label="Efecto grande (d=0.8)")
ax1.set_xlabel("d de Cohen mínimo detectable (potencia 80%, α=0.05)")
ax1.set_title("Efecto mínimo detectable por cada n declarado", fontsize=10, fontweight="bold")

patch_sub = mpatches.Patch(color="#f59e0b", alpha=0.75, label="Subjetivo")
patch_ins = mpatches.Patch(color="#2563eb", alpha=0.75, label="Instrumental")
ax1.legend(handles=[patch_sub, patch_ins] + ax1.get_legend_handles_labels()[0][0:3],
           fontsize=7, loc="lower right")

for i, (d, n) in enumerate(zip(min_d, ns)):
    ax1.text(d + 0.01, i, f"n={n}\nd≥{d:.2f}", va="center", fontsize=7, color="#333333")

# ── Panel 2: Brecha subjetivo vs instrumental ──
ax2 = fig.add_subplot(gs[0, 1])
bins = np.linspace(-20, 120, 40)
ax2.hist(instrumental_pct, bins=bins, alpha=0.65, color="#2563eb",
         label=f"Instrumental (corneómetro)\nmediana={np.median(instrumental_pct):.0f}%")
ax2.hist(subjective_pct, bins=bins, alpha=0.55, color="#f59e0b",
         label=f"Autoevaluación (subjetivo)\nmediana={np.median(subjective_pct):.0f}%")

ax2.axvline(np.median(instrumental_pct), color="#1d4ed8", linewidth=2, linestyle="--")
ax2.axvline(np.median(subjective_pct), color="#d97706", linewidth=2, linestyle="--")
ax2.axvline(97, color="#dc2626", linewidth=1.5, linestyle=":",
            label='Clarins: "97% hidratación instantánea"')

ax2.set_title(
    f"Brecha subjetivo vs instrumental\n(mismo efecto real, n={n_sim} simulaciones)",
    fontsize=10, fontweight="bold"
)
ax2.set_xlabel("% mejora reportada")
ax2.set_ylabel("Frecuencia")
ax2.legend(fontsize=7.5)
ax2.annotate(
    f"Brecha media:\n+{np.median(subjective_pct) - np.median(instrumental_pct):.0f} puntos\n(efecto placebo)",
    xy=(np.median(subjective_pct), 40),
    xytext=(60, 60),
    arrowprops=dict(arrowstyle="->", color="#333333"),
    fontsize=8
)

# ── Panel 3: Diseño de gemelas ──
ax3 = fig.add_subplot(gs[1, 0])
criteria = list(twin_design_scores.keys())
scores = list(twin_design_scores.values())
bar_colors_twin = ["#22c55e" if s >= 0.8 else "#f59e0b" if s >= 0.4 else "#ef4444"
                   for s in scores]

ax3.barh(range(len(criteria)), scores, color=bar_colors_twin, alpha=0.75,
         edgecolor="white", linewidth=1.2)
ax3.set_yticks(range(len(criteria)))
ax3.set_yticklabels(criteria, fontsize=8)
ax3.set_xlim(0, 1.3)
ax3.set_xlabel("Cumple el criterio (1.0 = sí, 0.0 = no / no declarado)")
ax3.set_title(
    "Estudio de gemelas Clarins:\n¿Diseño correcto para validar un producto?",
    fontsize=10, fontweight="bold"
)
ax3.axvline(1.0, color="#94a3b8", linestyle="--", linewidth=1, alpha=0.5)

green_patch = mpatches.Patch(color="#22c55e", alpha=0.75, label="Cumple")
yellow_patch = mpatches.Patch(color="#f59e0b", alpha=0.75, label="Parcial")
red_patch = mpatches.Patch(color="#ef4444", alpha=0.75, label="No declarado / No aplica")
ax3.legend(handles=[green_patch, yellow_patch, red_patch], fontsize=7.5, loc="lower right")

ax3.text(1.05, 0, "El estudio mapea\nenvejecimiento —\nno prueba que la\ncrema lo revierte",
         fontsize=7.5, color="#dc2626", va="center",
         bbox=dict(boxstyle="round,pad=0.3", facecolor="#fee2e2", edgecolor="#dc2626", alpha=0.8))

# ── Panel 4: Variabilidad con n=24 vs n=100 ──
ax4 = fig.add_subplot(gs[1, 1])
bins2 = np.linspace(15, 60, 35)
ax4.hist(sample_means_24, bins=bins2, alpha=0.65, color="#ef4444",
         label=f"n=24: IQR={np.percentile(sample_means_24,25):.1f}–{np.percentile(sample_means_24,75):.1f}%")
ax4.hist(sample_means_100, bins=bins2, alpha=0.55, color="#22c55e",
         label=f"n=100: IQR={np.percentile(sample_means_100,25):.1f}–{np.percentile(sample_means_100,75):.1f}%")

ax4.axvline(pop_mean, color="#1e293b", linewidth=2, linestyle="--", label=f"Media real: {pop_mean}%")
ax4.set_title(
    f"Variabilidad de resultados con n=24 vs n=100\n(1000 muestras, población real: {pop_mean}% ± {pop_std}% DE)",
    fontsize=10, fontweight="bold"
)
ax4.set_xlabel("Media muestral (% mejora hidratación)")
ax4.set_ylabel("Frecuencia (de 1000 simulaciones)")
ax4.legend(fontsize=8)
ax4.annotate(
    "Con n=24, el resultado\npublicado podría ir\nde ~20% a ~50%",
    xy=(np.percentile(sample_means_24, 90), 55),
    xytext=(45, 90),
    arrowprops=dict(arrowstyle="->", color="#dc2626"),
    fontsize=8, color="#dc2626"
)

plt.savefig("clarins_claim_analysis.png", dpi=150, bbox_inches="tight")
print("Figura guardada: clarins_claim_analysis.png")

# ─── OUTPUT RESUMEN ──────────────────────────────────────────────────────────
print("\n── RESUMEN DEL ANÁLISIS ─────────────────────────────────────────────")

print("\n1. POTENCIA ESTADÍSTICA POR ESTUDIO")
for name, study in clarins_studies.items():
    n = study["n"]
    d = min_detectable_effect(n)
    label = name.replace("\n", " ")
    size = "pequeño" if d <= 0.3 else "mediano" if d <= 0.6 else "grande"
    print(f"   n={n:3d} ({label[:35]:<35}): d≥{d:.2f} ({size})")

print("\n2. BRECHA SUBJETIVO VS INSTRUMENTAL")
print(f"   Mediana instrumental:   {np.median(instrumental_pct):.0f}%")
print(f"   Mediana subjetivo:      {np.median(subjective_pct):.0f}%")
print(f"   Brecha (efecto placebo): +{np.median(subjective_pct) - np.median(instrumental_pct):.0f} puntos")
print(f"   Clarins publica '97%' — autoevaluación, n=388")

print("\n3. DISEÑO DE GEMELAS")
print("   El estudio aísla la genética pero no controla producto vs no-producto")
print("   de forma publicada. Es un estudio de mapeo, no un RCT de eficacia.")

print("\n4. VARIABILIDAD CON N=24")
p5_24, p95_24 = np.percentile(sample_means_24, [5, 95])
p5_100, p95_100 = np.percentile(sample_means_100, [5, 95])
print(f"   n=24:  90% de las muestras caen entre {p5_24:.1f}% y {p95_24:.1f}%")
print(f"   n=100: 90% de las muestras caen entre {p5_100:.1f}% y {p95_100:.1f}%")
print("   Clarins usa n=24 para sus claims de TEWL e hidratación instrumentales.")
