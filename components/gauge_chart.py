import plotly.graph_objects as go
from config import COLORS


def create_failure_gauge(probability: float) -> go.Figure:
    """Create a gauge chart showing failure probability."""
    fig = go.Figure(data=[go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        title={"text": "Failure Probability (%)"},
        delta={"reference": 50, "suffix": " vs Threshold"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": COLORS['accent_orange']},
            "steps": [
                {"range": [0, 40], "color": COLORS['accent_green']},
                {"range": [40, 70], "color": "#F39C12"},
                {"range": [70, 100], "color": COLORS['accent_red']}
            ],
            "threshold": {
                "line": {"color": "white", "width": 4},
                "thickness": 0.75,
                "value": 60
            }
        },
        number={"suffix": "%"}
    )])

    fig.update_layout(
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor=COLORS['bg_dark'],
        font={"color": COLORS['text_primary'], "size": 14},
        height=400
    )

    return fig
