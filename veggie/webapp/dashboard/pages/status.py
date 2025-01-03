"""Status page"""
import datetime
import os
from typing import Any, Tuple

import dash_mantine_components as dmc
import humanize
import requests  # type: ignore
from dash_extensions.enrich import ALL, DashBlueprint, Input, Output, ctx
from dash_iconify import DashIconify

from veggie.webapp.dashboard import style

PORT = os.getenv("VEGGIE_PORT", 5000)

blueprint = DashBlueprint()


def get_event_details_card(event: dict) -> Any:
    """Populates a card for the selected event"""
    state_message = style.TYPE_TO_STATE.get(event.get("type", "default"), {}).get("message")
    state_color = style.TYPE_TO_STATE.get(event.get("type", "default"), {}).get("color")

    sent_timestamp = (
        datetime.datetime.fromtimestamp(event.get("sent_timestamp", 0), tz=datetime.timezone.utc)
        if event.get("sent_timestamp")
        else None
    )
    received_timestamp = (
        datetime.datetime.fromtimestamp(event.get("received_timestamp", 0), tz=datetime.timezone.utc)
        if event.get("received_timestamp")
        else None
    )
    started_timestamp = (
        datetime.datetime.fromtimestamp(event.get("started_timestamp", 0), tz=datetime.timezone.utc)
        if event.get("started_timestamp")
        else None
    )
    succeeded_timestamp = (
        datetime.datetime.fromtimestamp(event.get("succeeded_timestamp", 0), tz=datetime.timezone.utc)
        if event.get("succeeded_timestamp")
        else None
    )
    failed_timestamp = (
        datetime.datetime.fromtimestamp(event.get("failed_timestamp", 0), tz=datetime.timezone.utc)
        if event.get("failed_timestamp")
        else None
    )

    if sent_timestamp is not None:
        sent_timestamp_str = sent_timestamp.strftime("%b %m %Y %H:%M:%S")
        natural_delta = humanize.naturaltime(datetime.datetime.now(tz=datetime.timezone.utc) - sent_timestamp)
    else:
        sent_timestamp_str = "N/A"
        natural_delta = "N/A"

    runtime = event.get("runtime")
    runtime = round(runtime, 2) if runtime is not None else None
    runtime_str = f"{runtime} s" if runtime is not None else "N/A"

    return dmc.Stack(
        m="md",
        children=[
            dmc.Text(f"{sent_timestamp_str} ({natural_delta})", c="dimmed"),
            dmc.Group(
                gap="xs",
                justify="flex-start",
                children=[dmc.Text("Task ", c="dimmed", fw=700), dmc.Text([event.get("name")], fw=700)],
            ),
            dmc.Group(
                gap="lg",
                children=[
                    dmc.Stack(children=[dmc.Text("Status", c="dimmed"), dmc.Badge(state_message, color=state_color)]),
                    dmc.Stack(children=[dmc.Text("Runtime", c="dimmed"), dmc.Text(runtime_str)]),
                    dmc.Stack(children=[dmc.Text("UUID", c="dimmed"), dmc.Text(event.get("uuid"))]),
                ],
            ),
            dmc.Divider(variant="solid"),
            dmc.Stack(
                children=[
                    dmc.Text("Details ", fw=700),
                    dmc.Table(
                        withColumnBorders=False,
                        withTableBorder=False,
                        withRowBorders=False,
                        children=[
                            dmc.TableTbody(
                                children=[
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("Sent timestamp", c="dimmed")),
                                            dmc.TableTd(
                                                sent_timestamp.strftime("%b %m %Y %H:%M:%S")
                                                if sent_timestamp
                                                else "N/A"
                                            ),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("Received timestamp", c="dimmed")),
                                            dmc.TableTd(
                                                received_timestamp.strftime("%b %m %Y %H:%M:%S")
                                                if received_timestamp
                                                else "N/A"
                                            ),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("Started timestamp", c="dimmed")),
                                            dmc.TableTd(
                                                started_timestamp.strftime("%b %m %Y %H:%M:%S")
                                                if started_timestamp
                                                else "N/A"
                                            ),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("Succeeded timestamp", c="dimmed")),
                                            dmc.TableTd(
                                                succeeded_timestamp.strftime("%b %m %Y %H:%M:%S")
                                                if succeeded_timestamp
                                                else "N/A"
                                            ),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("Failed timestamp", c="dimmed")),
                                            dmc.TableTd(
                                                failed_timestamp.strftime("%b %m %Y %H:%M:%S")
                                                if failed_timestamp
                                                else "N/A"
                                            ),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("Hostname", c="dimmed")),
                                            dmc.TableTd(event.get("hostname")),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("args", c="dimmed")),
                                            dmc.TableTd(event.get("args")),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("kwargs", c="dimmed")),
                                            dmc.TableTd(event.get("kwargs")),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("result", c="dimmed")),
                                            dmc.Code(event.get("result")),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("pid", c="dimmed")),
                                            dmc.TableTd(event.get("pid")),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("parent_id", c="dimmed")),
                                            dmc.TableTd(event.get("parent_id")),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("retries", c="dimmed")),
                                            dmc.TableTd(event.get("retries")),
                                        ]
                                    ),
                                    dmc.TableTr(
                                        children=[
                                            dmc.TableTd(dmc.Text("routing_key", c="dimmed")),
                                            dmc.TableTd(event.get("routing_key")),
                                        ]
                                    ),
                                ]
                            )
                        ],
                    ),
                ]
            ),
        ],
    )


def layout() -> Any:
    """Creates layout for status page"""
    response = requests.get(f"http://localhost:{PORT}/api/events")
    events = response.json()

    rows = []
    for event in events:
        state_message = style.TYPE_TO_STATE.get(event.get("type"), {}).get("message", "")
        state_color = style.TYPE_TO_STATE.get(event.get("type"), {}).get("color", "gray")

        row = dmc.TableTr(
            children=[
                dmc.TableTd(
                    dmc.ActionIcon(
                        DashIconify(icon="mingcute:more-2-line", width=20),
                        size="md",
                        variant="transparent",
                        id={"type": "event", "uuid": event["uuid"]},
                    )
                ),
                dmc.TableTd(event["name"]),
                dmc.TableTd(dmc.Badge(state_message, color=state_color)),
                dmc.TableTd(
                    humanize.naturaltime(
                        datetime.datetime.now(tz=datetime.timezone.utc)
                        - datetime.datetime.fromtimestamp(event["received_timestamp"], tz=datetime.timezone.utc)
                    )
                ),
            ]
        )
        rows.append(row)

    return dmc.Container(
        children=[
            dmc.Table(
                id="task-status-table",
                withColumnBorders=False,
                withTableBorder=True,
                children=[
                    dmc.TableThead(
                        dmc.TableTr(
                            [dmc.TableTh(""), dmc.TableTh("Task"), dmc.TableTh("Status"), dmc.TableTh("Received")]
                        )
                    ),
                    dmc.TableTbody(rows),
                ],
            ),
            dmc.Drawer(id="event-details-drawer", position="right", size="60%", opened=False),
        ],
        fluid=True,
    )


blueprint.layout = layout


@blueprint.callback(
    Output("event-details-drawer", "opened"),
    Output("event-details-drawer", "children"),
    Input({"type": "event", "uuid": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def open_event_details(n_clicks: int) -> Tuple[bool, Any]:
    """Opens event details drawer."""
    triggered_id = ctx.triggered_id
    task_id = triggered_id["uuid"]

    response = requests.get(f"http://localhost:{PORT}/api/events/{task_id}")
    event = response.json()

    return True, get_event_details_card(event=event)
