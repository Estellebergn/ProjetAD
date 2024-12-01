import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import graph_func as graph
import util_func as util

# Initialiser l'application Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Application Dash Moderne"

# Style des onglets
tab_style = {
    "padding": "12px",
    "fontWeight": "bold",
    "border": "1px solid #d6d6d6",
    "borderRadius": "5px",
    "backgroundColor": "#f9f9f9",
}

tab_selected_style = {
    "padding": "12px",
    "fontWeight": "bold",
    "border": "1px solid #007BFF",
    "borderRadius": "5px",
    "backgroundColor": "#007BFF",
    "color": "white",
}

# Layout principal
app.layout = html.Div(
    [
        html.H1("Tableau de Bord Dash", style={"textAlign": "center", "padding": "20px"}),
        dcc.Tabs(
            id="tabs",
            value="tab1",
            children=[
                dcc.Tab(label="Vue d'ensemble des données", value="tab1"),
                dcc.Tab(label="Analyses", value="tab2"),
                dcc.Tab(label="Informations", value="tab3"),
            ],
        ),
        html.Div(id="content"),
    ]
)

# Callback pour gérer les onglets
@app.callback(
    Output("content", "children"),
    Input("tabs", "value"),
)
def render_tab_content(tab_name):
    if tab_name == "tab1":
        # Charger les données

        # Contenu de l'onglet 1
        return html.Div(
            [
                # Dropdown pour sélectionner les données
                html.Div(
                    [
                        html.Label("Sélectionner les données à afficher :"),
                        dcc.Dropdown(
                            id="chosen_year",
                            options=[
                                {"label": "2017", "value": "data/2017.csv"},
                                {"label": "2018", "value": "data/2018.csv"},
                                {"label": "2019", "value": "data/2019.csv"},
                                {"label": "2020", "value": "data/2020.csv"},
                                {"label": "2021", "value": "data/2021.csv"},
                                
                            ],
                            value="data/2020.csv",
                            style={"width": "100%", "marginBottom": "20px"},
                        ),
                    ]
                ),
                # Texte explicatif
                html.Div(
                    [
                        html.H3("Vue d'ensemble des données"),
                        html.P(
                            """
                            Le World Happiness Report est une étude annuelle qui mesure et classe les pays en fonction 
                            de leur niveau de bonheur perçu par leurs citoyens. Ce rapport repose sur des données issues 
                            des enquêtes du Gallup World Poll. Les citoyens évaluent leur vie sur une échelle de 0 à 10, 
                            où 10 représente la meilleure vie possible.
                            Les facteurs suivants sont pris en compte pour évaluer le bonheur :
                            """
                        ),
                        html.Ul(
                            [
                                html.Li("Ladder Score (Score de bonheur) : Une moyenne des évaluations subjectives de la vie."),
                                html.Li("Logged GDP per capita : Une mesure du PIB par habitant."),
                                html.Li("Social Support (Soutien social) : La perception de pouvoir compter sur quelqu'un en cas de besoin."),
                                html.Li("Healthy Life Expectancy (Espérance de vie en bonne santé) : L'espérance de vie corrigée en fonction des conditions de santé."),
                                html.Li("Freedom to make life choices (Liberté de faire des choix de vie) : Le sentiment de liberté dans les décisions personnelles."),
                                html.Li("Generosity (Générosité) : Les tendances à faire des dons ou à aider les autres."),
                                html.Li("Perceptions of Corruption (Perception de la corruption) : Le niveau perçu de corruption dans le gouvernement et les affaires."),
                            ]
                        ),
                    ],
                    style={
                        "width": "37%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "padding": "15px",
                        "marginRight": "5px",
                        "backgroundColor": "#f9f9f9",
                        "borderRadius": "10px",
                        "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        "textAlign": "justify",
                    },
                ),
                # Graphique interactif 1 : Carte
                html.Div(
                    [
                        dcc.Graph(id="dynamic_carte"),
                    ],
                    style={"width": "57%", "display": "inline-block", "verticalAlign": "top", "padding": "10px"},
                ),
                
                # Graphique interactif 2 : Histogramme
                html.Div(
                    [
                        dcc.Graph(id="dynamic_hist"),
                    ],
                    style={"width": "100%", "display": "inline-block", "verticalAlign": "top", "padding": "10px"},
                ),
            ]
        )

    # Autres onglets
    elif tab_name == "tab2":
        return html.Div("Contenu de l'onglet 2.")
    elif tab_name == "tab3":
        return html.Div("Contenu de l'onglet 3.")


@app.callback(
    [Output("dynamic_carte", "figure"), Output("dynamic_hist", "figure")],
    Input("chosen_year", "value"),
)
def update_graphs(selected_file):
    # Charger les données
    df = pd.read_csv(selected_file)
    selected_year = selected_file.split("/")[-1].split(".")[0]
    data_sorted = util.normalize_columns(df, selected_file)
    data_sorted = df.sort_values(by="Happiness Score", ascending=False)


    # Générer les graphiques
    carte_figure = graph.get_carte(data_sorted,selected_year)
    hist_figure = graph.get_hist(data_sorted,selected_year)

    return carte_figure, hist_figure


# Lancer le serveur
if __name__ == "__main__":
    app.run_server(debug=True)
