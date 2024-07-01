import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from manager_download import DownloadManager as DM

MAX_LANGUAGES = 5  # Number of top languages to add to chart, for each year quarter
GRAPH_PATH = "assets/bar_graph.png"  # Chart saving path.

async def create_loc_graph(yearly_data: dict, save_path: str):
    """
    Draws graph of lines of code added by user by quarters of years.
    Picks top MAX_LANGUAGES languages from each quarter only.

    :param yearly_data: GitHub user yearly data.
    :param save_path: Path to save the graph file.
    """
    colors = await DM.get_remote_yaml("linguist")

    years = len(yearly_data.keys())
    year_indexes = np.arange(years)

    languages_all_loc = {}
    for i, y in enumerate(sorted(yearly_data.keys())):
        for q in yearly_data[y].keys():
            langs = sorted(yearly_data[y][q].keys(), key=lambda n: yearly_data[y][q][n], reverse=True)[0:MAX_LANGUAGES]

            for lang in langs:
                if lang not in languages_all_loc:
                    languages_all_loc[lang] = np.zeros((4, years), dtype=int)
                languages_all_loc[lang][q - 1, i] = yearly_data[y][q][lang]

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1.5, 1])

    language_handles = []
    cumulative = np.zeros((4, years), dtype=int)

    for key, value in languages_all_loc.items():
        color = colors.get(key, {}).get("color", "w")
        language_handles += [mpatches.Patch(color=color, label=key)]

        for quarter in range(4):
            loc_added = np.maximum(value[quarter] - cumulative[quarter], 0)
            ax.bar(year_indexes + quarter * 0.21, loc_added, 0.2, bottom=cumulative[quarter], color=color)
            cumulative[quarter] += value[quarter]

    ax.set_ylabel("LOC added", fontdict=dict(weight="bold"))
    ax.set_xticks(np.array([np.arange(i, i + 0.84, step=0.21) for i in year_indexes]).flatten(), labels=["Q1", "Q2", "Q3", "Q4"] * years)

    sax = ax.secondary_xaxis("top")
    sax.set_xticks(year_indexes + 0.42, labels=sorted(yearly_data.keys()))
    sax.spines["top"].set_visible(False)

    ax.legend(title="Language", handles=language_handles, loc="upper left", bbox_to_anchor=(1, 1), framealpha=0, title_fontproperties=dict(weight="bold"))

    sax.tick_params(axis="both", length=0)
    sax.spines["top"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.ylim(0, 1.05 * np.amax(cumulative))
    plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
