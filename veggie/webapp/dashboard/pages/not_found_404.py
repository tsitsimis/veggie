"""Not found page"""
from dash_extensions.enrich import DashBlueprint, html

blueprint = DashBlueprint()
blueprint.layout = html.H1("404 - Page not found")
