from dash import Dash, html, dcc, page_container, page_registry

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True
)

server = app.server

app.title = "Placement Data Dashboard"


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div("Placement Dashboard", className="navbar-title"),

                html.Div(
                    children=[
                        dcc.Link(
                            page["name"],
                            href=page["path"],
                            className="nav-link"
                        )
                        for page in page_registry.values()
                    ],
                    className="nav-links"
                )
            ],
            className="navbar"
        ),

        html.Div(
            children=page_container,
            className="page-container"
        )
    ]
)


if __name__ == "__main__":
    app.run(debug=True)