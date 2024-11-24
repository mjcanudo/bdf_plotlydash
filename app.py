from dash import Dash, html, dcc
from dash.dependencies import Output, Input
from dash.dash import PreventUpdate

import pandas as pd
import plotly.express as px

from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc


sent_analysis = pd.read_parquet('processed_datasets/tags_sentiment.parquet')
top_rtd = pd.read_parquet('processed_datasets/top_rtd_dcd.parquet')



# APP
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH, dbc_css])
server = app.server


load_figure_template("MORPH")

app.layout = dbc.Container([
    dcc.Tabs(className="dbc", children = [
        dbc.Tab(label="IMDB Movie Tags", children = [
            html.H1(id="tags_ratings", style={"text-align": "center"}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Markdown("**Rating Range**"),
                        dcc.Dropdown(
                                    options=sent_analysis.Tag_Range.sort_values().unique(),
                                    id='tag_range_dropdown',
                                    value='0 to 1'),
                        html.Br(),
                        dcc.Markdown("**Tags for movies with ratings within specified range**"),
                        ])
                ], width=3),
                dbc.Col(dcc.Graph(id="tag_visual"), width=9)
            ]),
            html.Br(),
            #html.Br(),
            #dbc.Row(
            #    dcc.Markdown("**Sentiment for Rating Intervals: 0 to to to 1: -0.18580000000000002**")
            #),

        ]),
        dbc.Tab(label="Top Rated Movies by Decade", children=[ 
            html.H1(id="top-rated", style={"text-align": "center"}),
            dbc.Row([
                dbc.Col([
                    dcc.Markdown("Select A Decade:"),
                    dcc.Dropdown(
                        id="decade_dropdown",
                        options=top_rtd.decade.sort_values().unique(),
                        value="1910s")], width=2),

                dbc.Col([dcc.Graph(id="top_rtd_dcd_visual")]
                        , width=9)
            ])
        ])
    ])
], style={"width":1300})


# Tab 1 Tags by Rating
@app.callback(
    Output("tag_visual", "figure"),
    Input("tag_range_dropdown", "value")
)

def tag_range_dd(tag_range):
    figure = px.bar(sent_analysis.query(f' Tag_Range == "{tag_range}" ').sort_values("Number of Tags"),
            y='Tags',
            x='Number of Tags',
            orientation='h',
            template="plotly_dark"
            )
    return figure


# Tab 2 Top Rated by Decade
@app.callback(
            Output("top_rtd_dcd_visual", "figure"),
            Input("decade_dropdown", "value")
            )

def movie_bar_chart(decade):
    figure = px.bar(top_rtd.query(f' decade == "{decade}" ').sort_values("rating_mean"),
                    y='title',
                    x='rating_mean',
                    orientation='h',
                    template="plotly_dark"
            )
    return figure



if __name__ == "__main__":
    app.run_server(mode='external')