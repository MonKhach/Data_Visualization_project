from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State

BASE_DIR = Path(__file__).resolve().parent

DATA_PATHS = [
    BASE_DIR / "Placement_Data_Full_Class.csv",
    BASE_DIR / "data" / "Placement_Data_Full_Class.csv"
]
data_path = None
for path in DATA_PATHS:
    if path.exists():
        data_path = path
        break
if data_path is None:
    raise FileNotFoundError('CSV file not found. Put Placement_Data_Full_Class.csv in the project folder '
        'or inside the data folder.')
df = pd.read_csv(data_path)

df["placed"] = df["status"].map({
    "Placed": 1,
    "Not Placed": 0
})

placed_df = df[df["status"] == "Placed"].copy()
# print("Dataset loaded successfully")
# print(df.head())
# print(df.columns)
categorical_options = [
    {"label": "Gender", "value": "gender"},
    {"label": "SSC Board", "value": "ssc_b"},
    {"label": "HSC Board", "value": "hsc_b"},
    {"label": "HSC Stream", "value": "hsc_s"},
    {"label": "Degree Type", "value": "degree_t"},
    {"label": "Work Experience", "value": "workex"},
    {"label": "Specialisation", "value": "specialisation"}
]

salary_group_options = [
    {"label": "Gender", "value": "gender"},
    {"label": "Degree Type", "value": "degree_t"},
    {"label": "Work Experience", "value": "workex"},
    {"label": "Specialisation", "value": "specialisation"},
    {"label": "HSC Stream", "value": "hsc_s"}
]

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = 'Placment Data Dashboard'

NAV_STYLE = {'backgoundColor': '#1f2937',
             'padding': '18px',
             'display': 'flex',
             'alignItems': 'center',
             'gap': '25px'}
TITLE_STYLE = {'color': 'white',
    'fontSize': '24px',
    'fontWeight': 'bold',
    'marginRight': '30px'}

LINK_STYLE = {'color': 'white',
    'textDecoration': 'none',
    'fontSize': '17px',
    'padding': '8px 12px',
    'borderRadius': '8px',
    'backgroundColor': '#374151'}

PAGE_STYLE = {'padding': '30px',
    'fontFamily': 'Arial'}

CARD_STYLE = {'backgroundColor': 'white',
    'padding': '20px',
    'borderRadius': '12px',
    'boxShadow': '0 4px 12px rgba(0,0,0,0.08)',
    'marginBottom': '20px'}

KPI_GRID_STYLE = {'display': 'grid',
    'gridTemplateColumns': 'repeat(5, 1fr)',
    'gap': '20px',
    'marginBottom': '25px'}

KPI_CARD_STYLE = {'backgroundColor': 'white',
    'padding': '22px',
    'borderRadius': '14px',
    'boxShadow': '0 4px 14px rgba(0,0,0,0.10)',
    'textAlign': 'center'}

KPI_TITLE_STYLE = {'fontSize': '15px',
    'color': '#6b7280',
    'marginBottom': '10px'}

KPI_VALUE_STYLE = {'fontSize': '28px',
    'fontWeight': 'bold',
    'color': '#111827'}

GRAPH_GRID_STYLE = {'display': 'grid',
    'gridTemplateColumns': 'repeat(2, 1fr)',
    'gap': '20px',
    'marginBottom': '25px'}

CONTROL_GRID_STYLE = {'display': 'grid',
    'gridTemplateColumns': 'repeat(2, 1fr)',
    'gap': '20px',
    'marginBottom': '25px'}

app.layout = html.Div(
    children=[
        dcc.Location(id="url"),

        html.Div(
            children=[
                html.Div("Placement Dashboard", style=TITLE_STYLE),

                dcc.Link("Overview", href="/", style=LINK_STYLE),
                dcc.Link("Placement Drivers", href="/drivers", style=LINK_STYLE),
                dcc.Link("Salary Analysis", href="/salary", style=LINK_STYLE),
            ],
            style=NAV_STYLE
        ),

        html.Div(id="page-content", style=PAGE_STYLE)
    ]
)

def kpi_card(title, value):
    return html.Div(
        children=[
            html.Div(title, style=KPI_TITLE_STYLE),
            html.Div(value, style=KPI_VALUE_STYLE)
        ],
        style=KPI_CARD_STYLE
    )
def create_score_comparison_figure():
    score_columns = ['ssc_p', 'hsc_p', 'degree_p', 'etest_p', 'mba_p']
    score_data = df.groupby('status')[score_columns].mean().reset_index()

    score_data_long = score_data.melt(
        id_vars = 'status',
        value_vars = score_columns,
        var_name = 'Score Type',
        value_name = 'Average Score'
    )

    fig = px.bar(
        score_data_long,
        x = 'Score Type',
        y = 'Average Score',
        color = 'status',
        barmode = 'group',
        title = 'Average Academic Score by Placement Status',
        text = 'Average Score'
    )

    fig.update_traces(
        texttemplate = '%{text:.1f}',
        textposition = 'outside'
    )

    fig.update_layout(
        xaxis_title = 'Academic Score Type',
        yaxis_title = 'Average Score',
        title_x = 0.5
    )
    return fig

def create_status_figure():
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    fig = px.bar(
        status_counts,
        x = 'status',
        y = 'count',
        title = 'Placement Status Distribution',
        text = 'count'
    )
    fig.update_layout(
        xaxis_title = 'Placement Statys',
        yaxis_title = 'Number of Students',
        title_x = 0.5
    )
    return fig

def overview_page():
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
                style=KPI_GRID_STYLE
            ),

            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(figure=create_status_figure())
                        ],
                        style=CARD_STYLE
                    ),

                    html.Div(
                        children=[
                            dcc.Graph(figure=create_score_comparison_figure())
                        ],
                        style=CARD_STYLE
                    )
                ],
                style=GRAPH_GRID_STYLE
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
                style=CARD_STYLE
            ),

            html.Div(
                children=[
                    html.H3("Main Questions"),
                    html.P("1. What percentage of students were placed?"),
                    html.P("2. Which academic and personal factors are connected with placement?"),
                    html.P("3. How does salary vary among placed students?")
                ],
                style=CARD_STYLE
            )
        ]
    )

def drivers_page():
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
                style=CARD_STYLE
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
                        style=CARD_STYLE
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
                                tooltip={"placement": "bottom", "always_visible": True}
                            )
                        ],
                        style=CARD_STYLE
                    )
                ],
                style=CONTROL_GRID_STYLE
            ),

            html.Div(
                children=[
                    html.H3("Placement Rate by Selected Category"),
                    html.P(id="drivers-filter-info"),
                    dcc.Graph(id="drivers-placement-graph")
                ],
                style=CARD_STYLE
            )
        ]
    )

def salary_page():
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
                style=CARD_STYLE
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
                        style=CARD_STYLE
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
                                style={
                                    "width": "100%",
                                    "padding": "10px",
                                    "fontSize": "16px",
                                    "marginTop": "8px",
                                    "marginBottom": "12px"
                                }
                            ),

                            html.Button(
                                "Apply Filter",
                                id="salary-filter-button",
                                n_clicks=0,
                                style={
                                    "backgroundColor": "#1f2937",
                                    "color": "white",
                                    "border": "none",
                                    "padding": "10px 18px",
                                    "borderRadius": "8px",
                                    "cursor": "pointer",
                                    "fontSize": "15px"
                                }
                            )
                        ],
                        style=CARD_STYLE
                    )
                ],
                style=CONTROL_GRID_STYLE
            ),

            html.Div(
                children=[
                    html.P(id="salary-filter-info")
                ],
                style=CARD_STYLE
            ),

            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(id="salary-distribution-graph")
                        ],
                        style=CARD_STYLE
                    ),

                    html.Div(
                        children=[
                            dcc.Graph(id="salary-group-graph")
                        ],
                        style=CARD_STYLE
                    )
                ],
                style=GRAPH_GRID_STYLE
            )
        ]
    )

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/drivers":
        return drivers_page()

    elif pathname == "/salary":
        return salary_page()

    else:
        return overview_page()
    
@app.callback(
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
        placement_by_category["total_students"] - placement_by_category["placed_students"]
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

@app.callback(
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

if __name__ == '__main__':
    app.run(debug=True)
