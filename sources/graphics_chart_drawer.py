from typing import Dict
from numpy import arange, array, add, amax
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

MAX_LANGUAGES = 5  # Number of top languages to add to chart, for each year quarter
GRAPH_PATH = "assets/bar_graph.png"  # Chart saving path.

async def create_loc_graph(yearly_data: Dict, save_path: str):
    languages_all_loc = dict()
    years = len(yearly_data.keys())
    year_indexes = arange(years)

    for i, y in enumerate(sorted(yearly_data.keys())):
        for q in yearly_data[y].keys():
            langs = sorted(yearly_data[y][q].keys(), key=lambda n: yearly_data[y][q][n]["add"], reverse=True)[0:MAX_LANGUAGES]
            for lang in langs:
                if lang not in languages_all_loc:
                    languages_all_loc[lang] = array([[0] * years] * 4)
                languages_all_loc[lang][q - 1][i] = yearly_data[y][q][lang]["add"]

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1.5, 1])
    language_handles = []
    cumulative = array([[0] * years] * 4)

    for key, value in languages_all_loc.items():
        color = colors[key]["color"] if colors[key]["color"] is not None else "w"
        language_handles += [mpatches.Patch(color=color, label=key)]
        for quarter in range(4):
            ax.bar(year_indexes + quarter * 0.21, value[quarter], 0.2, bottom=cumulative[quarter], color=color)
            cumulative[quarter] = add(cumulative[quarter], value[quarter])

    ax.axhline(y=0.5, lw=0.5, snap=True, color="k")
    ax.set_ylabel("LOC added", fontdict=dict(weight="bold"))
    ax.set_xticks(array([arange(i, i + 0.84, step=0.21) for i in year_indexes]).flatten(), labels=["Q1", "Q2", "Q3", "Q4"] * years)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.ylim(0, 1.05 * amax(cumulative))
    plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
