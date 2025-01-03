"""
Navbar for main app
"""

import dash_mantine_components as dmc
from dash import ALL, Input, Output, callback, callback_context
from dash_iconify import DashIconify

from veggie.webapp.dashboard import config

icon_width = 16

navlink_data = [
    {
        "id": "navlink-status",
        "label": "Status",
        "leftSection": DashIconify(icon="pajamas:status", width=icon_width),
        "variant": "light",
        "href": f"{config.APP_BASE_PATH}",
        "style": {"fontWeight": "100"},
    }
]

navbar_contents = dmc.ScrollArea(
    offsetScrollbars=True,
    type="scroll",
    style={"height": "100%", "padding-inline-end": "0"},
    children=dmc.Stack(
        gap=0,
        mt=30,
        children=[
            dmc.Button(
                "Refresh",
                id="refresh-repos-button",
                leftSection=DashIconify(icon="basil:refresh-solid", width=20),
                style={"display": "none"},
                mb="md",
                ml="md",
                mr="md",
            ),
            dmc.NavLink(
                id={"type": "navlink", "index": f"{config.APP_BASE_PATH}"},
                label="Status",
                leftSection=DashIconify(icon="pajamas:status", width=icon_width),
                variant="light",
                href=f"{config.APP_BASE_PATH}",
            ),
            dmc.NavLink(
                id={"type": "navlink", "index": f"{config.APP_BASE_PATH}tasks"},
                label="Start Tasks",
                leftSection=DashIconify(icon="fluent-mdl2:running", width=icon_width),
                variant="light",
                href=f"{config.APP_BASE_PATH}tasks",
            ),
        ],
    ),
)


@callback(Output({"type": "navlink", "index": ALL}, "active"), Input("url", "pathname"))
def update_navlinks(pathname: str) -> list[bool]:
    """Updates active navlink based on pathname."""
    return [control["id"]["index"] == pathname for control in callback_context.outputs_list]
