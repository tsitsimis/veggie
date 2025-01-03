"""
Dash app
"""
import dash_mantine_components as dmc
from dash_extensions.enrich import DashProxy, Input, Output, State, dash, dcc, page_container

from veggie.webapp.dashboard import config, style
from veggie.webapp.dashboard.header import header_contents
from veggie.webapp.dashboard.navbar import navbar_contents
from veggie.webapp.dashboard.pages.not_found_404 import blueprint as not_found_blueprint
from veggie.webapp.dashboard.pages.status import blueprint as status_blueprint
from veggie.webapp.dashboard.pages.tasks import blueprint as tasks_blueprint

dash._dash_renderer._set_react_version("18.2.0")


app = DashProxy(
    suppress_callback_exceptions=True,
    use_pages=True,
    url_base_pathname=config.APP_BASE_PATH,
    external_stylesheets=[dmc.styles.DATES, dmc.styles.NOTIFICATIONS],
)
app.layout = dmc.MantineProvider(
    id="mantine-provider",
    forceColorScheme="dark",
    children=[
        dcc.Location(id="url"),
        dmc.NotificationProvider(),
        dmc.AppShell(
            id="appshell",
            header={"height": style.HEADER_HEIGHT_PX},
            transitionDuration=0,
            children=[
                dmc.AppShellHeader(
                    id="header",
                    children=header_contents,
                    style={"align-content": "center"},
                    zIndex=2000,
                    h=style.HEADER_HEIGHT_PX,
                    pl="md",
                    pr="md",
                ),
                dmc.AppShellNavbar(id="navbar", children=navbar_contents, w=style.NAVBAR_WIDTH_PX),
                dmc.AppShellMain(children=page_container, h="100%"),
            ],
            zIndex=1400,
        ),
    ],
)

status_blueprint.register(app, module="dash_apps.dashboard.pages.status", path="/")
tasks_blueprint.register(app, module="dash_apps.dashboard.pages.tasks", path="/tasks")
not_found_blueprint.register(app, module="dash_apps.dashboard.pages.not_found_404")


@app.callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def switch_theme(n_clicks: int, theme: str) -> str:
    """Switches theme between light and dark based on theme toggle."""
    return "dark" if theme == "light" else "light"


@app.callback(Output("appshell", "navbar"), Input("burger", "opened"))
def on_burger_click(burger_opened: bool) -> dict:
    """Toggle navbar when burger menu is clicked."""
    navbar = {
        "width": style.NAVBAR_WIDTH_PX,
        "breakpoint": "sm",
        "collapsed": {"desktop": False, "mobile": not burger_opened},
    }
    return navbar
