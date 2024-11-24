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
                        dcc.RadioItems(
                                    options=sent_analysis.Tag_Range.sort_values().unique(),
                                    id='tag_range_dropdown',
                                    value='0 to 1'),
                        #html.Br(),
                        #dcc.Markdown("**Tags for movies with ratings within specified range**"),
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
                    dcc.RadioItems(
                        id="decade_dropdown",
                        options=top_rtd.decade.sort_values().unique(),
                        value="1910s")], width=2),

                dbc.Col([dcc.Graph(id="top_rtd_dcd_visual")]
                        , width=9)
            ])
        ]),
        dbc.Tab(label="Polarizing Movies by Decade", children=[ 
            html.H1(id="pol-movies", style={"text-align": "center"}),
            dbc.Row([
                dbc.Col([dcc.Graph(id="pol_movies_visual")]
                        , width=12), 
                ], justify='center'),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Markdown("Select A Decade:"),
                    dcc.Dropdown(
                        id="decade_dropdown_pol",
                        options=pol_movies.decade.sort_values().unique(),
                        value=["1950s", "1960s"],
                        multi=True),
                    html.Br(),
                    html.Br(),
                    dcc.Markdown("Minimum Number of Ratings:"),
                    dcc.Slider(
                        id="ratingnum_slider",
                        min=1,
                        max=300,
                        step=20,
                        value=1)], width=10),
                    html.Br()


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
    if tag_range == "5":
        chart_title = f'Tags for Movies with Rating Mean of 5'
    else: 
        chart_title = f'Tags for Movies with Rating Mean in the {tag_range} Range'
    figure = px.bar(sent_analysis.query(f' Tag_Range == "{tag_range}" ').sort_values("Number of Tags"),
            y='Tags',
            x='Number of Tags',
            orientation='h',
            template="plotly_dark",
            title=chart_title
            )
    return figure


# Tab 2 Top Rated by Decade
@app.callback(
            Output("top_rtd_dcd_visual", "figure"),
            Input("decade_dropdown", "value")
            )

def movie_bar_chart(decade):
    if decade == "NA":
        chart_title = 'Top Rated Movies with no specified Decade'
    else:
        chart_title = f'Top Rated Movies by Rating Mean in the {decade}'
    figure = px.bar(top_rtd.query(f' decade == "{decade}" ').sort_values("rating_mean"),
                y='title',
                x='rating_mean',
                orientation='h',
                template="plotly_dark",
                title=chart_title,
                    labels={"title":"Title",
                            "rating_mean":"Rating Mean"}
            )
    return figure

# Tab 3 Top Rated by Decade
@app.callback(
            Output("pol_movies_visual", "figure"),
            Input("decade_dropdown_pol", "value"),
            Input("ratingnum_slider", "value")

            )

def pol_movie_bar_chart(decades, ratingnum):
    ratingnum = int(ratingnum)
    figure = px.scatter(pol_movies.query(f' decade in @decades and rating_count >= @ratingnum '),
                    x="rating_stddev",
                    y='rating_count',
                    template="plotly_dark",
                    hover_data=['title', 'rating_mean'],
                    title='Movies by Rating Standard Deviation',
                    labels={"rating_stddev":"Rating Standard Deviation",
                            "rating_count":"Number of Ratings"}
            )
    return figure

if __name__ == "__main__":
    app.run_server(mode='external')