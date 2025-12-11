import plotly.graph_objects as go
from config import COLORS


def create_failure_gauge(probability: float) -> go.Figure:
    """
    Create a gauge chart showing failure probability.

    Args:
        probability: A float representing failure probability.
                     Expected range 0.0-1.0; values >1 are normalized.
    """
    # Normalize: if value > 1, assume it's already a percentage and clamp
    if probability > 1.0:
        display_value = min(probability, 100.0)
    else:
        display_value = probability * 100.0

    fig = go.Figure(data=[go.Indicator(
        mode="gauge+number+delta",
        value=display_value,
        title={"text": "Probabilité de défaillance (%)"},
        delta={"reference": 50, "suffix": " vs Seuil"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": COLORS.get('warning', '#F59E0B')},
            "steps": [
                {"range": [0, 40], "color": COLORS.get('success', '#10B981')},
                {"range": [40, 70], "color": COLORS.get('warning', '#F59E0B')},
                {"range": [70, 100], "color": COLORS.get('danger', '#EF4444')}
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
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font={"color": "#111827", "size": 14},
        height=400
    )

    return fig
