from dash import html


def kpi_card(title, value):
    return html.Div(
        children=[
            html.Div(title, className="kpi-title"),
            html.Div(value, className="kpi-value")
        ],
        className="kpi-card"
    )