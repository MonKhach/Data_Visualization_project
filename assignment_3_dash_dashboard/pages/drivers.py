import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px

from data_loader import df


dash.register_page(
    __name__,
    path="/drivers",
    name="Placement Drivers"
)


categorical_options = [
    {"label": "Gender", "value": "gender"},
    {"label": "SSC Board", "value": "ssc_b"},
    {"label": "HSC Board", "value": "hsc_b"},
    {"label": "HSC Stream", "value": "hsc_s"},
    {"label": "Degree Type", "value": "degree_t"},
    {"label": "Work Experience", "value": "workex"},
    {"label": "Specialisation", "value": "specialisation"}
]


def layout():
    return html.Div(
        children=[
            html.H1("Placement Drivers"),

            html.Div(
                children=[
                    html.H3("Purpose of this page"),
                    html.P(
                        "This page shows how placement rate changes across different "
                        "student characteristics such as gender, degree type, work experience, "
                        "and specialization."
                    )
                ],
                className="card"
            ),

            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Label("Choose a category:"),
                            dcc.Dropdown(
                                id="category-dropdown",
                                options=categorical_options,
                                value="workex",
                                clearable=False
                            )
                        ],
                        className="card"
                    ),

                    html.Div(
                        children=[
                            html.Label("Minimum SSC percentage:"),
                            dcc.Slider(
                                id="ssc-slider",
                                min=int(df["ssc_p"].min()),
                                max=int(df["ssc_p"].max()),
                                step=1,
                                value=int(df["ssc_p"].min()),
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": True
                                }
                            )
                        ],
                        className="card"
                    )
                ],
                className="control-grid"
            ),

            html.Div(
                children=[
                    html.H3("Placement Rate by Selected Category"),
                    html.P(id="drivers-filter-info"),
                    dcc.Graph(id="drivers-placement-graph")
                ],
                className="card"
            )
        ]
    )


@callback(
    Output("drivers-placement-graph", "figure"),
    Output("drivers-filter-info", "children"),
    Input("category-dropdown", "value"),
    Input("ssc-slider", "value")
)
def update_drivers_graph(selected_category, minimum_ssc):
    filtered_df = df[df["ssc_p"] >= minimum_ssc].copy()

    placement_by_category = (
        filtered_df
        .groupby(selected_category)
        .agg(
            placement_rate=("placed", "mean"),
            placed_students=("placed", "sum"),
            total_students=("placed", "size")
        )
        .reset_index()
    )

    placement_by_category["placement_rate"] = placement_by_category["placement_rate"] * 100

    placement_by_category["not_placed_students"] = (
        placement_by_category["total_students"] -
        placement_by_category["placed_students"]
    )

    fig = px.bar(
        placement_by_category,
        x=selected_category,
        y="placement_rate",
        text="placement_rate",
        hover_data={
            "placement_rate": ":.1f",
            "placed_students": True,
            "not_placed_students": True,
            "total_students": True
        },
        title=f"Placement Rate by {selected_category}"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title=selected_category,
        yaxis_title="Placement Rate (%)",
        yaxis_range=[0, 110],
        title_x=0.5,
        height=520,
        margin=dict(t=90, b=80, l=70, r=40)
    )

    filter_text = (
        f"Showing students with SSC percentage greater than or equal to {minimum_ssc}. "
        f"Number of students after filtering: {len(filtered_df)}. "
        f"The bars show placement percentage, not the number of students."
    )

    return fig, filter_text
