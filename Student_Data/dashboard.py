"""
Student Performance Dashboard
Reads StudentsPerformance.csv and saves a dark, LinkedIn-style dashboard image.

Run:   python dashboard.py
Needs: pip install pandas matplotlib
Output: dashboard.png  (post this on LinkedIn / add to your README)
"""
import string
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Always look for files next to this script, whatever folder you run it from
HERE = Path(__file__).resolve().parent

# ---------- 1. Load and prepare data ----------
df = pd.read_csv(HERE / "StudentsPerformance.csv")
df.columns = [c.strip().lower().replace(" ", "_").replace("/", "_") for c in df.columns]
df = df.drop_duplicates()
df["average_score"] = df[["math_score", "reading_score", "writing_score"]].mean(axis=1).round(2)

# ---------- 2. Theme ----------
BG, CARD, TEXT, MUTED = "#0b0b0f", "#14141b", "#f2f2f5", "#8b8b99"
BLUE, ORANGE, RED, GREEN = "#4da3ff", "#ff9b71", "#e8604c", "#4cc9a0"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": CARD, "axes.edgecolor": "#2a2a35",
    "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": TEXT, "font.family": "DejaVu Sans", "axes.spines.top": False,
    "axes.spines.right": False,
})

fig = plt.figure(figsize=(16, 9), dpi=120)
fig.text(0.03, 0.955, "Student performance analytics", fontsize=22, fontweight="bold", va="center")

# ---------- 3. KPI tiles ----------
prep = df.groupby("test_preparation_course")["average_score"].mean()
kpis = [
    ("TOTAL STUDENTS", f"{len(df):,}", BLUE),
    ("AVG SCORE", f"{df['average_score'].mean():.1f}", GREEN),
    ("PREP COURSE BOOST", f"+{prep['completed'] - prep['none']:.1f} pts", ORANGE),
    ("COMPLETED PREP", f"{(df['test_preparation_course'] == 'completed').mean() * 100:.1f}%", RED),
]
for i, (label, value, color) in enumerate(kpis):
    x = 0.03 + i * 0.2425
    fig.add_artist(FancyBboxPatch((x, 0.80), 0.232, 0.10, boxstyle="round,pad=0,rounding_size=0.008",
                                  transform=fig.transFigure, facecolor=CARD, edgecolor=color, linewidth=1.2))
    fig.text(x + 0.012, 0.875, label, fontsize=10, color=MUTED, va="center")
    fig.text(x + 0.012, 0.827, value, fontsize=24, fontweight="bold", color=TEXT, va="center")


def panel(pos, title):
    ax = fig.add_axes(pos)
    ax.set_title(title, loc="left", fontsize=12.5, fontweight="bold", color=TEXT, pad=10)
    ax.grid(axis="y", color="#2a2a35", linewidth=0.8)
    ax.set_axisbelow(True)
    return ax


# grid: 3 columns x 2 rows
cols = [0.135, 0.455, 0.765]
w, h = 0.205, 0.26
rows = [0.46, 0.12]

# ---------- 4. Chart 1: avg score by parental education ----------
ax = panel((cols[0], rows[0], w, h), "Average score by parental education")
order = ["some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"]
edu = df.groupby("parental_level_of_education")["average_score"].mean().reindex(order)
bars = ax.barh([string.capwords(o) for o in order], edu.values, color=BLUE, height=0.65)
ax.invert_yaxis()
ax.set_xlim(50, 80)
ax.grid(axis="x", color="#2a2a35"); ax.grid(axis="y", visible=False)
for b, v in zip(bars, edu.values):
    ax.text(v + 0.3, b.get_y() + b.get_height() / 2, f"{v:.1f}", va="center", fontsize=9)

# ---------- 5. Chart 2: test prep course ----------
ax = panel((cols[1], rows[0], w, h), "Average score by test preparation")
vals = [prep["none"], prep["completed"]]
bars = ax.bar(["None", "Completed"], vals, color=[RED, GREEN], width=0.5)
ax.set_ylim(0, 85)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.2f}", ha="center", fontsize=11, fontweight="bold")

# ---------- 6. Chart 3: gender split of subject scores ----------
ax = panel((cols[2], rows[0], w, h), "Subject scores by gender")
g = df.groupby("gender")[["math_score", "reading_score", "writing_score"]].mean()
x = range(3); bw = 0.36
for k, (gender, color) in enumerate([("female", ORANGE), ("male", BLUE)]):
    xs = [i + (k - 0.5) * bw for i in x]
    bars = ax.bar(xs, g.loc[gender].values, width=bw, color=color, label=gender.title())
    for b, v in zip(bars, g.loc[gender].values):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.0f}", ha="center", fontsize=9)
ax.set_xticks(list(x)); ax.set_xticklabels(["Math", "Reading", "Writing"])
ax.set_ylim(0, 85)
ax.legend(frameon=False, labelcolor=TEXT, loc="upper right", ncol=2, fontsize=9)

# ---------- 7. Chart 4: lunch type donut ----------
ax = fig.add_axes((cols[0] + 0.01, rows[1], w - 0.02, h))
ax.set_title("Students by lunch type", loc="center", fontsize=12.5, fontweight="bold", pad=10)
lunch = df["lunch"].value_counts()
ax.pie(lunch.values, colors=[BLUE, ORANGE], startangle=90, counterclock=False,
       wedgeprops=dict(width=0.38, edgecolor=CARD, linewidth=2),
       )
ax.legend([f"{k.title()}  {lunch[k] / lunch.sum() * 100:.1f}%" for k in lunch.index], frameon=False, labelcolor=TEXT,
          loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=2, fontsize=9)
avg_l = df.groupby("lunch")["average_score"].mean()
ax.text(0, 0, f"Std {avg_l['standard']:.1f}\nFree {avg_l['free/reduced']:.1f}\navg score",
        ha="center", va="center", fontsize=9, color=MUTED)

# ---------- 8. Chart 5: score distribution ----------
ax = panel((cols[1], rows[1], w, h), "Distribution of average scores")
counts, edges = pd.cut(df["average_score"], bins=range(0, 101, 5)).value_counts(sort=False), range(0, 101, 5)
mids = [e + 2.5 for e in list(edges)[:-1]]
ax.fill_between(mids, counts.values, color=RED, alpha=0.35)
ax.plot(mids, counts.values, color=RED, linewidth=2.2)
ax.axvline(df["average_score"].mean(), color=TEXT, linestyle="--", linewidth=1)
ax.text(df["average_score"].mean() + 1, counts.max() * 0.95, f"mean {df['average_score'].mean():.1f}", fontsize=9)
ax.set_xlabel("Average score"); ax.set_ylabel("Students")

# ---------- 9. Chart 6: prep x gender ----------
ax = panel((cols[2], rows[1], w, h), "Average score by prep and gender")
pg = df.groupby(["test_preparation_course", "gender"])["average_score"].mean().unstack()
x = range(2)
for k, (gender, color) in enumerate([("female", ORANGE), ("male", BLUE)]):
    xs = [i + (k - 0.5) * bw for i in x]
    bars = ax.bar(xs, pg.loc[["none", "completed"], gender].values, width=bw, color=color, label=gender.title())
    for b, v in zip(bars, pg.loc[["none", "completed"], gender].values):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}", ha="center", fontsize=9)
ax.set_xticks(list(x)); ax.set_xticklabels(["No prep", "Prep completed"])
ax.set_ylim(0, 90)
ax.legend(frameon=False, labelcolor=TEXT, loc="upper left", ncol=2, fontsize=9)

fig.text(0.97, 0.02, "Data: Kaggle - Students Performance in Exams  |  Python, Pandas, Matplotlib",
         ha="right", fontsize=8.5, color=MUTED)

fig.savefig(HERE / "dashboard.png", facecolor=BG)
print("Saved", HERE / "dashboard.png")
