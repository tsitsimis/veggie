"""REST API"""

from inspect import signature
from typing import Any, Callable, get_type_hints

from celery import Celery
from flask import Blueprint, Response, jsonify, request

from ..storage import Storage


def function_params_to_json(func: Callable) -> list[dict]:
    """
    Extracts function arguments, their types, and default values into JSON format.

    Args:
        func: The function to extract information from.

    Returns:
        A list of dictionaries, each representing one of the function's arguments.
    """
    # Get the function signature and type hints
    sig = signature(func)
    type_hints = get_type_hints(func)

    # Prepare JSON structure
    arguments = []
    for name, param in sig.parameters.items():
        param_type = type_hints.get(name, "Any")  # Use type hint if available, otherwise default to Any
        default_value = param.default if param.default is not param.empty else None  # Handle default values
        type_name = param_type.__name__ if hasattr(param_type, "__name__") else str(param_type)
        arguments.append({"name": name, "type": type_name, "default": default_value})
    return arguments


def create_api_blueprint(storage: Storage, celery_app: Celery) -> Blueprint:
    """Initializes Flask app"""
    bp = Blueprint(name="api", import_name=__name__)

    @bp.route("/events", methods=["GET"])
    def get_events() -> list[dict]:
        """Gets events"""
        return storage.get_events()

    @bp.route("/events/<string:event_id>", methods=["GET"])
    def get_single_event(event_id: str) -> Any:
        """Gets events"""
        event = storage.get_event_by_id(id=event_id)
        if event is None:
            return Response(status=404, response="Event not found")
        return event

    @bp.route("/tasks", methods=["GET"])
    def get_tasks() -> list[dict]:
        """Gets tasks"""
        user_defined_tasks = {name: task for name, task in celery_app.tasks.items() if not name.startswith("celery.")}
        return [
            {"name": name, "parameters": function_params_to_json(func=task)}
            for name, task in user_defined_tasks.items()
        ]

    @bp.route("/tasks", methods=["POST"])
    def send_task() -> Response:
        data = request.get_json()

        task_name = data.get("task_name")
        task_params = data.get("task_params")

        if task_name is None:
            return Response(status=400, response="Missing task_name")
        if task_params is None:
            return Response(status=400, response="Missing task_params")

        result = celery_app.send_task(task_name, kwargs=task_params)

        return jsonify({"task_id": result.task_id})

    return bp
