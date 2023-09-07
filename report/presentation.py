import os

from dash import html


def presentation():
    return html.Div(
        html.Iframe(
            src=os.path.join("assets", "EDA_Project.pdf#toolbar=0"), # https://tinytip.co/tips/html-pdf-params/
            style={"display": "block", "width":"99vw", "height": "95vh"}
        ),
    )