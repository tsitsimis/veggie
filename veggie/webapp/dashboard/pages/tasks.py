"""Task execution page"""

import os
from typing import Any

import dash_mantine_components as dmc
import requests  # type: ignore
from dash import set_props
from dash_extensions.enrich import ALL, MATCH, DashBlueprint, Input, Output, State, ctx, html
from loguru import logger

PORT = os.getenv("VEGGIE_PORT", 5000)

blueprint = DashBlueprint()


def create_input_component(task_name: str, param: dict) -> Any:
    """Creates a Dash input component based on the parameter type."""
    param_type = param["type"]
    default_value = param["default"]
    param_name = param["name"]

    if param_type == "str":
        return dmc.TextInput(
            label=param_name, id={"type": "input", "task": task_name, "param": param_name}, value=default_value or ""
        )
    elif param_type == "int":
        return dmc.NumberInput(
            label=param_name, id={"type": "input", "task": task_name, "param": param_name}, value=default_value or None
        )
    elif param_type == "datetime":
        return dmc.DateTimePicker(
            label=param_name,
            id={"type": "input", "task": task_name, "param": param_name},
            value=default_value or None,
            valueFormat="YYYY-MM-DD HH:mm:ss",
        )
    elif param_type == "bool":
        return dmc.Switch(label=param_name, id={"type": "input", "task": task_name, "param": param_name}, checked=False)
    else:
        return dmc.JsonInput(
            label=param_name,
            id={"type": "input", "task": task_name, "param": param_name},
            validationError="Invalid JSON",
            formatOnBlur=True,
            autosize=True,
            maxRows=4,
        )


def create_task_section(task_info: dict) -> Any:
    """
    Creates input components and run button for a task.
    """
    task_name = task_info["name"]
    parameters = task_info["parameters"]
    input_components = [create_input_component(task_name=task_name, param=param) for param in parameters]

    return dmc.Card(
        children=[
            dmc.Group([dmc.Text(task_name, fw=500)], justify="flex-start", mt="md", mb="xs"),
            dmc.Stack(children=input_components),
            dmc.Group(
                children=[dmc.Button(children="Run", id={"type": "run", "task": task_name}, mt="md")],
                justify="flex-end",
                mt="md",
                mb="xs",
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        w="70%",
    )


def layout() -> Any:
    """Creates layout for tasks page"""
    tasks = requests.get(f"http://localhost:{PORT}/api/tasks").json()
    tasks = sorted(tasks, key=lambda task: task["name"])

    task_layouts = []
    for task in tasks:
        task_card = create_task_section(task_info=task)
        task_layouts.append(task_card)

    return dmc.Container(
        children=dmc.Stack(align="center", mt="md", children=task_layouts + [html.Div(id="notifications-container")]),
        fluid=True,
    )


blueprint.layout = layout


@blueprint.callback(
    Output({"type": "run", "task": MATCH}, "dummy"),
    Input({"type": "run", "task": MATCH}, "n_clicks"),
    State({"type": "input", "task": ALL, "param": ALL}, "id"),
    State({"type": "input", "task": ALL, "param": ALL}, "value"),
    State({"type": "input", "task": ALL, "param": ALL}, "checked"),
    prevent_initial_call=True,
)
def handle_run(n_clicks: int, param_ids: list[dict], param_values: list, param_checked: list) -> Any:
    """Reads input values corresponding to a task and runs the task with Celery."""
    triggered_id = ctx.triggered_id
    task_name = triggered_id["task"]

    params = []
    for param_id, value, checked in zip(param_ids, param_values, param_checked, strict=True):
        if param_id["task"] == task_name:
            param_value = checked if isinstance(checked, bool) else value
            params.append({**param_id, "value": param_value})

    task_kwargs = {param["param"]: param["value"] for param in params}
    logger.info(task_kwargs)

    response = requests.post(
        url=f"http://localhost:{PORT}/api/tasks",
        json={"task_name": task_name, "task_params": task_kwargs},
        headers={"Content-Type": "application/json"},
    )
    if response.status_code != 200:
        logger.error(response.text)
        return None

    notification = dmc.Notification(
        title=f"Task {task_name} started",
        message=f"Task ID: {response.json()['task_id']}",
        action="show",
        position="bottom-right",
        autoClose=3000,
    )

    set_props(component_id="notifications-container", props={"children": [notification]})

    return None
