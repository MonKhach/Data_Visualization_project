import dash
from dash import html, dcc
import plotly.express as px

from data_loader import df, placed_df
from components import kpi_card


dash.register_page(
    __name__,
    path="/",
    name="Overview"
)


def create_status_figure():
    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]

    fig = px.bar(
        status_counts,
        x="status",
        y="count",
        title="Placement Status Distribution",
        text="count"
    )

    fig.update_layout(
        xaxis_title="Placement Status",
        yaxis_title="Number of Students",
        title_x=0.5,
        height=500
    )

    return fig


def create_score_comparison_figure():
    score_columns = ["ssc_p", "hsc_p", "degree_p", "etest_p", "mba_p"]

    score_data = df.groupby("status")[score_columns].mean().reset_index()

    score_data_long = score_data.melt(
        id_vars="status",
        value_vars=score_columns,
        var_name="Score Type",
        value_name="Average Score"
    )

    fig = px.bar(
        score_data_long,
        x="Score Type",
        y="Average Score",
        color="status",
        barmode="group",
        title="Average Academic Scores by Placement Status",
        text="Average Score"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Academic Score Type",
        yaxis_title="Average Score",
        title_x=0.5,
        height=500
    )

    return fig


def layout():
    total_students = len(df)
    placed_students = int(df["placed"].sum())
    not_placed_students = total_students - placed_students
    placement_rate = df["placed"].mean() * 100
    average_salary = placed_df["salary"].mean()

    return html.Div(
        children=[
            html.H1("Overview"),

            html.Div(
                children=[
                    kpi_card("Total Students", total_students),
                    kpi_card("Placed Students", placed_students),
                    kpi_card("Not Placed Students", not_placed_students),
                    kpi_card("Placement Rate", f"{placement_rate:.1f}%"),
                    kpi_card("Average Salary", f"{average_salary:,.0f}")
                ],
                className="kpi-grid"
            ),

            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(figure=create_status_figure())
                        ],
                        className="card"
                    ),

                    html.Div(
                        children=[
                            dcc.Graph(figure=create_score_comparison_figure())
                        ],
                        className="card"
                    )
                ],
                className="graph-grid"
            ),

            html.Div(
                children=[
                    html.H3("Dashboard Story"),
                    html.P(
                        "This dashboard explores student placement outcomes. "
                        "The main goal is to understand which student characteristics "
                        "are related to successful placement and how salary differs "
                        "among placed students."
                    )
                ],
                className="card"
            ),

            html.Div(
                children=[
                    html.H3("Main Questions"),
                    html.P("1. What percentage of students were placed?"),
                    html.P("2. Which academic and personal factors are connected with placement?"),
                    html.P("3. How does salary vary among placed students?")
                ],
                className="card"
            )
        ]
    )
