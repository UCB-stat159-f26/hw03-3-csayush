import matplotlib.pyplot as plt
import pandas as pd

REQUIRED_COLUMNS = ["player_age", "age_diff", "result"]


def _check_plot_data(career_data):
    if not isinstance(career_data, pd.DataFrame):
        raise TypeError("career_data must be the data frame from get_career_data()")
    for column_name in REQUIRED_COLUMNS:
        if column_name not in career_data.columns:
            raise ValueError(f"career_data is missing column: {column_name}")
    if len(career_data) == 0:
        raise ValueError("career_data has no matches to plot")


def plot_age_gap(career_data):
    _check_plot_data(career_data)
    figure, axes = plt.subplots()

    win_rows = career_data[career_data["result"] == "W"]
    loss_rows = career_data[career_data["result"] == "L"]

    axes.scatter(win_rows["player_age"], win_rows["age_diff"], color="green", label="Win")
    axes.scatter(loss_rows["player_age"], loss_rows["age_diff"], color="red", label="Loss")
    axes.axhline(0, color="gray", linewidth=1)

    axes.set_xlabel("Player age")
    axes.set_ylabel("Player age - opponent age")
    axes.set_title("Career matches by age difference")
    axes.legend()
    figure.tight_layout()
    return axes
