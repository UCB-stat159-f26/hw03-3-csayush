import matplotlib
import pandas as pd
import pytest

matplotlib.use("Agg")

from tennis_career.plot import plot_age_gap


@pytest.fixture(autouse=True)
def close_figures():
    yield
    matplotlib.pyplot.close("all")


def sample_matches():
    return pd.DataFrame({
        "player_age": [14.1, 15.2, 16.0],
        "age_diff": [-4.7, 1.2, -0.5],
        "result": ["L", "W", "W"],
    })


def test_plot_age_gap_labels():
    axes = plot_age_gap(sample_matches())
    assert axes.get_xlabel() == "Player age"
    assert axes.get_ylabel() == "Player age - opponent age"
    legend_text = axes.get_legend().get_texts()
    legend_labels = [text.get_text() for text in legend_text]
    assert legend_labels == ["Win", "Loss"]


def test_plot_age_gap_point_counts():
    axes = plot_age_gap(sample_matches())
    win_points = axes.collections[0].get_offsets()
    loss_points = axes.collections[1].get_offsets()
    assert len(win_points) == 2
    assert len(loss_points) == 1


def test_plot_age_gap_rejects_wrong_type():
    with pytest.raises(TypeError):
        plot_age_gap([14.1, 15.2])


def test_plot_age_gap_rejects_missing_column():
    matches = sample_matches().drop(columns=["result"])
    with pytest.raises(ValueError, match="missing column: result"):
        plot_age_gap(matches)


def test_plot_age_gap_rejects_empty_data():
    empty_matches = sample_matches().iloc[0:0]
    with pytest.raises(ValueError, match="no matches"):
        plot_age_gap(empty_matches)
