"""
Header component of the dashboard.
"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from ...webapp.dashboard import config

header_contents = dmc.Grid(
    align="center",
    justify="space-between",
    children=[
        dmc.GridCol(
            dmc.Group(
                [
                    dmc.Burger(id="burger", opened=False, hiddenFrom="sm", size="md"),
                    dmc.Anchor(
                        dmc.Group(
                            [DashIconify(icon="tdesign:broccoli", height=30), dmc.Text("Veggie", size="xl", fw=700)]
                        ),
                        href=config.APP_BASE_PATH,
                        refresh=False,
                        underline=False,
                        style={"text-decoration": "none", "color": "inherit"},
                    ),
                ]
            ),
            span="content",
        ),
        dmc.GridCol(
            children=[
                dmc.Group(
                    children=[
                        dmc.ActionIcon(
                            id="color-scheme-toggle",
                            children=[
                                dmc.Paper(DashIconify(icon="radix-icons:sun", width=20), lightHidden=True),
                                dmc.Paper(DashIconify(icon="radix-icons:moon", width=20), darkHidden=True),
                            ],
                            color="#FAB005",
                            size="lg",
                            variant="transparent",
                            radius="xl",
                        ),
                        dmc.Menu(
                            [dmc.MenuTarget(dmc.Anchor(children=dmc.Avatar(radius="xl"), href="#"))],
                            position="bottom-end",
                        ),
                    ]
                )
            ],
            span="content",
        ),
    ],
)
