import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.express as px

from data_loader import placed_df


dash.register_page(
    __name__,
    path="/salary",
    name="Salary Analysis"
)


salary_group_options = [
    {"label": "Gender", "value": "gender"},
    {"label": "Degree Type", "value": "degree_t"},
    {"label": "Work Experience", "value": "workex"},
    {"label": "Specialisation", "value": "specialisation"},
    {"label": "HSC Stream", "value": "hsc_s"}
]


def layout():
    min_salary = int(placed_df["salary"].min())
    max_salary = int(placed_df["salary"].max())

    return html.Div(
        children=[
            html.H1("Salary Analysis"),

            html.Div(
                children=[
                    html.H3("Purpose of this page"),
                    html.P(
                        "This page analyzes salary only for placed students. "
                        "It helps compare salary distribution and average salary "
                        "across different student groups."
                    )
                ],
                className="card"
            ),

            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Label("Choose group for salary comparison:"),
                            dcc.Dropdown(
                                id="salary-group-dropdown",
                                options=salary_group_options,
                                value="specialisation",
                                clearable=False
                            )
                        ],
                        className="card"
                    ),

                    html.Div(
                        children=[
                            html.Label("Minimum salary filter:"),
                            dcc.Input(
                                id="salary-min-input",
                                type="number",
                                value=min_salary,
                                min=min_salary,
                                max=max_salary,
                                step=10000,
                                className="input-field"
                            ),

                            html.Button(
                                "Apply Filter",
                                id="salary-filter-button",
                                n_clicks=0,
                                className="button"
                            )
                        ],
                        className="card"
                    )
                ],
                className="control-grid"
            ),

            html.Div(
                children=[
                    html.P(id="salary-filter-info")
                ],
                className="card"
            ),

            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(id="salary-distribution-graph")
                        ],
                        className="card"
                    ),

                    html.Div(
                        children=[
                            dcc.Graph(id="salary-group-graph")
                        ],
                        className="card"
                    )
                ],
                className="graph-grid"
            )
        ]
    )


@callback(
    Output("salary-distribution-graph", "figure"),
    Output("salary-group-graph", "figure"),
    Output("salary-filter-info", "children"),
    Input("salary-filter-button", "n_clicks"),
    Input("salary-group-dropdown", "value"),
    State("salary-min-input", "value")
)
def update_salary_graphs(n_clicks, selected_group, minimum_salary):
    if minimum_salary is None:
        minimum_salary = int(placed_df["salary"].min())

    filtered_salary_df = placed_df[placed_df["salary"] >= minimum_salary].copy()

    salary_distribution_fig = px.histogram(
        filtered_salary_df,
        x="salary",
        nbins=20,
        title="Salary Distribution for Placed Students"
    )

    salary_distribution_fig.update_layout(
        xaxis_title="Salary",
        yaxis_title="Number of Students",
        title_x=0.5,
        height=500,
        margin=dict(t=80, b=70, l=70, r=40)
    )

    salary_by_group = (
        filtered_salary_df
        .groupby(selected_group)
        .agg(
            average_salary=("salary", "mean"),
            median_salary=("salary", "median"),
            number_of_students=("salary", "size")
        )
        .reset_index()
    )

    salary_group_fig = px.bar(
        salary_by_group,
        x=selected_group,
        y="average_salary",
        text="average_salary",
        hover_data={
            "average_salary": ":,.0f",
            "median_salary": ":,.0f",
            "number_of_students": True
        },
        title=f"Average Salary by {selected_group}"
    )

    salary_group_fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    salary_group_fig.update_layout(
        xaxis_title=selected_group,
        yaxis_title="Average Salary",
        title_x=0.5,
        height=500,
        margin=dict(t=80, b=70, l=70, r=40)
    )

    filter_info = (
        f"Showing placed students with salary greater than or equal to {minimum_salary:,.0f}. "
        f"Number of students after filtering: {len(filtered_salary_df)}."
    )

    return salary_distribution_fig, salary_group_fig, filter_info
