import os

from dash import html


def presentation():
    return html.Div(
        html.Iframe(
            src=os.path.join("assets", "EDA_Project.pdf"),
            style={"display": "block", "width": "100vw", "height": "100vh"}
        ),
    )