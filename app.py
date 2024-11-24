from dash import Dash, html, dcc
from dash.dependencies import Output, Input
from dash.dash import PreventUpdate

import pandas as pd
import plotly.express as px

from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc


sent_analysis = pd.read_parquet('processed_datasets/tags_sentiment.parquet')
top_rtd = pd.read_parquet('processed_datasets/top_rtd_dcd.parquet')
pol_movies = pd.read_parquet('processed_datasets/polarizing_movies.parquet')


# APP
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
server = app.server


load_figure_template("DARKLY")


app.layout = dbc.Container([
    dcc.Tabs(className="dbc", children = [
        dbc.Tab(label="IMDB Movie Tags", children = [
            html.H1(id="tags_ratings", style={"text-align": "center"}),
            dbc.Row([
                html.Br(),
                dbc.Card(
                dbc.CardBody(
                        [
                html.H4("Tag Sentiment Analysis", className="card-title"),
                dbc.CardHeader(
                    "Sentiment analysis on the Movie Tags using the Natural Language Toolkit. ",
                    className="card-text",
                ),
                html.Br(),
                        ])),
                dbc.Card(
                dbc.CardBody(
                        [
                html.H6("We created bins with the movies based on their mean rating.",
                    className="card-text",
                ),
                html.H6(["Next, we evaluated which tags are more prevalent in which bins,",
                        html.Br(),
                       " in order to analyze which tags are related with higher-rated movies",
                        html.Br(),
                        " and with worse-rated movies."],
                    className="card-text"),
                        ]))
                        ])
            ,
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Markdown("**Mean Rating Range**"),
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
            # row final com sentiment analysis
            dbc.Row([
                html.Br(),
                dbc.Card(
                dbc.CardBody(
                        [
                #html.H5("Sentiment Analysis for Each Rating Bin", className="card-title"),
                html.H5(
                    "Sentiment Analysis for Each Rating Bin: ",
                    className="card-text",
                ),
                #html.Br(),
                        ])),
                dbc.Card(
                dbc.CardBody(
                        [
                dbc.CardHeader(
                    "Sentiment Analysis for Rating Interval 0 to to to 1 - Negative: ",
                    className="card-text"),
                html.H6(["This is consistent with the expectation that movies with very low ratings will",
                        html.Br(),
                        " tend to have negative tags such as boring, disappointing, or bad.",
                        html.Br(),
                        " The negative sentiment here is relatively mild, but still shows that the tags ",
                        html.Br(),
                        " for these movies reflect a critical or unfavorable view.",
                        html.Br()], className="card-text"),

                    
                        ])),
                dbc.Card(
                dbc.CardBody(
                        [
                dbc.CardHeader(
                    "Sentiment Analysis for Rating Interval 1 to to to 2 - Negative: ",
                    className="card-text"),
                html.H6(["For movies rated between 1 and 2, the negative sentiment remains,",
                        html.Br(),
                        " but its slightly more negative than the previous group. Could indicate that ",
                        html.Br(),
                        " users are still expressing disappointment, though the movies might not be as bad as those rated 0-1.",
                        html.Br(),
                        " They might be tagged with words like underwhelming or not good.",
                        html.Br()], className="card-text"),

                    
                        ])),
                dbc.Card(
                dbc.CardBody(
                        [
                dbc.CardHeader(
                    "Sentiment Analysis for Rating Interval 2 to 3 - Slightly Negative: ",
                    className="card-text"),
                html.H6(["This result shows that movies in this mid-range still lean slightly negative, ",
                        html.Br(),
                        " though less strongly than in the lower rating groups. The sentiment is more neutral-to-negative,",
                        html.Br(),
                        " which fits the profile of movies that are rated average or slightly below average.",
                        html.Br(),
                        " Users might tag these movies with more neutral or mixed descriptors like mediocre or okay.",
                        html.Br()], className="card-text"),

                    
                        ])),
                dbc.Card(
                dbc.CardBody(
                        [
                dbc.CardHeader(
                    "Sentiment Analysis for Rating Interval 3 to 4 - Slightly Positive: ",
                    className="card-text"),
                html.H6(["his marks the first positive sentiment, albeit weakly.",
                        html.Br(),
                        " Movies rated in this range may have mixed reviews but show some degree of positive feedback.",
                        html.Br(),
                        " Tags could include terms like good, decent, or enjoyable, reflecting that these movies are mostly",
                        html.Br(),
                        " appreciated, though not overwhelmingly so.",
                        html.Br()], className="card-text"),

                    
                        ])),
                dbc.Card(
                dbc.CardBody(
                        [
                dbc.CardHeader(
                    "Sentiment Analysis for Rating Interval over 4 - Slightly Positive: ",
                    className="card-text"),
                html.H6(["For highly rated movies, the sentiment is still positive, but not highly so.",
                        html.Br(),
                        " This could suggest that while high ratings are associated with more favorable tags (such as classic, masterpiece, or award-winning),",
                        html.Br(),
                        " they arent necessarily overwhelmingly praised.",
                        html.Br(),
                        " The tags could be slightly positive but not excessively enthusiastic.",
                        html.Br()], className="card-text"),

                    
                        ])),
                dbc.Card(
                dbc.CardBody(
                        [
                dbc.CardHeader(
                    "Interpretation a la Poirer:",
                    className="card-text"),
                html.H6(["The negative sentiment for low-rated movies is expected, but its not very strong,",
                        html.Br(),
                        " suggesting that users may still use somewhat neutral or balanced tags for those movies",
                        html.Br(),
                        " As the ratings increase, the sentiment gradually becomes more positive,",
                        html.Br(),
                        " though the sentiment for mid-rated movies (2-3) remains slightly negative or neutral,",
                        html.Br(),
                        " indicating that these movies are not highly praised but also not intensely criticized.",
                        html.Br(),
                        html.Br(),
                        " The slight positive sentiment for movies rated 3-4 and 4-5 is also reasonable.",
                        html.Br(),
                        " While these movies are generally considered good or better by viewers, the sentiment doesnt spike dramatically,",
                        html.Br(),
                        " implying that even high-rated films might receive mixed feedback from some viewers.",
                        html.Br(),
                        html.Br(),
                        " In conclusion, your sentiment results align well with expectations and indicate a gradual shift from negative",
                        html.Br(),
                        " to neutral-to-positive sentiment as movie ratings increase, which is consistent with how movies are typically",
                        html.Br(),
                        " perceived across different rating scales.",
                        html.Br()
                        ], className="card-text"),

                    
                        ])),
                        ]),

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
                    dcc.Markdown("Number of Ratings:"),
                    dcc.RangeSlider(
                        id="ratingnum_slider",
                        min=1,
                        max=300,
                        step=20,
                        value=[1, 300])], width=10),
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
    #ratingnum = int(ratingnum)
    figure = px.scatter(pol_movies.query(f' decade in @decades and (@ratingnum[0] <= rating_count <= @ratingnum[1])  '),
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