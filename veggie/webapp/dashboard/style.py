"""
Page styling (sizes, colors, etc.) configuration for pages.
"""

HEADER_HEIGHT_PX = 60
NAVBAR_WIDTH_PX = 200

TYPE_TO_STATE = {
    "task-succeeded": {"message": "Succeeded", "color": "green"},
    "task-failed": {"message": "Failed", "color": "red"},
    "task-started": {"message": "In progress", "color": "blue"},
    "task-received": {"message": "Received", "color": "yellow"},
    "task-sent": {"message": "Sent", "color": "gray"},
    "default": {"message": "N/A", "color": "gray"},
}
