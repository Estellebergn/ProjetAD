import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import graph_func as graph
import util_func as util
import data_analysis_func as analysis

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
                dcc.Tab(label="Clustering", value="tab2"),
                dcc.Tab(label="Graph", value="tab3"),
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
        return html.Div([
    # Section ACP
    html.H3("Clustering des données"),
    html.H2("Analyse en Composantes Principales (ACP)"),
    html.P("L'Analyse en Composantes Principales (ACP) est une méthode de réduction de dimensionnalité qui permet de visualiser les données dans un espace à deux dimensions."),
    html.P("Cette technique permet de réduire la dimensionnalité des données en les projetant dans un nouvel espace composé de composantes principales."),
    html.P("Les composantes principales sont des combinaisons linéaires des variables initiales qui capturent le maximum de variance des données."),
    
    # Dropdown pour sélection de données
    html.Label("Sélectionner les données à afficher :"),
    dcc.Dropdown(
        id="chosen_year_2",
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
    
    # Graphique ACP
    html.Div([
        dcc.Graph(id="dynamic_pca"),
    ], style={"width": "100%", "padding": "10px"}),

    # Section Clustering
    html.H2("Le Clustering (K-means et Gaussian Mixture)"),
    html.P("Le clustering est une méthode d'apprentissage non supervisée qui permet de regrouper les données en fonction de leurs similarités."),
    html.P("Les algorithmes de clustering permettent de diviser les données en groupes homogènes, appelés clusters."),
    html.P("Deux algorithmes de clustering couramment utilisés sont le K-means et le Gaussian Mixture."),
    html.P("Le K-means divise les données en K clusters en minimisant la somme des distances au carré entre les points et les centres de chaque cluster."),
    html.P("Le Gaussian Mixture modélise les données comme un mélange de distributions gaussiennes, permettant de modéliser des clusters de formes complexes."),

    # Dropdown pour choix d'algorithme
    html.Label("Sélectionner l'algorithme de clustering :"),
    dcc.Dropdown(
        id="chosen_clustering",
        options=[
            {"label": "K-means", "value": "kmeans"},
            {"label": "Gaussian Mixture", "value": "gmm"},
            {"label": "Consensus", "value": "consensus"},
        ],
        value="kmeans",
        style={"width": "100%", "marginBottom": "20px"},
    ),
    
    # Graphique Scoring et paragraphe silhouette score
    html.Div([
        # Graphique des scores
        html.Div([
            dcc.Graph(id="dynamic_scoring"),
        ], style={"width": "50%", "display": "inline-block"}),

        # Paragraphe silhouette score
        html.Div([
            html.P("Le silhouette score mesure la cohérence des clusters en évaluant à quel point les points d'un cluster sont proches les uns des autres (cohésion) par rapport aux points des clusters voisins (séparation)."),
            html.P(
                id="dynamic_n_clusters_text",
                children="Nombre de clusters trouvé :",
            ),
        ], style={"width": "40%", "display": "inline-block", "verticalAlign": "top", "padding": "10px"}),
    ]),

    # Graphique Clustering
    html.Div([
        dcc.Graph(id="dynamic_clustering", style={"width": "80%", "display": "inline-block", "verticalAlign": "top", "padding": "10px"}),
        html.Div(
        id="radioitems-container",  # Conteneur pour les RadioItems
        children=[
            dcc.RadioItems(
                id="centroides",
                options=[
                    {"label": "Avec centroides", "value": True},
                    {"label": "Sans centroides", "value": False},
                ],
                value=False,
                style={"marginTop": "10px"},
            ),
        ],
        style={"width": "15%", "display": "inline-block", "verticalAlign": "top",   "padding": "10px"},
        ),
    ]),


])

    elif tab_name == "tab3":
        return html.Div("Contenu de l'onglet 3.")


@app.callback(
    [Output("dynamic_carte", "figure"), Output("dynamic_hist", "figure")],
    Input("chosen_year", "value"),
)
def update_graphs(selected_file):
    # Charger les données
    data_sorted, selected_year = util.charge_data(selected_file)


    # Générer les graphiques
    carte_figure = graph.get_carte(data_sorted,selected_year)
    hist_figure = graph.get_hist(data_sorted,selected_year)

    return carte_figure, hist_figure


@app.callback(
    Output("radioitems-container", "style"),
    Input("chosen_clustering", "value")
)
def toggle_radioitems_visibility(selected_clustering):
    if selected_clustering == "consensus":
        # Masquer les RadioItems si "consensus" est choisi
        
        return {"display": "none"}
    else:
        # Afficher les RadioItems pour les autres valeurs
        return {"width": "15%", "display": "inline-block", "verticalAlign": "top", "padding": "10px"}
    


@app.callback(
    Output("dynamic_clustering", "figure"),
    Output("dynamic_pca", "figure"),
    Output("dynamic_scoring", "figure"),
    Output("dynamic_n_clusters_text", "children"),
    Input("chosen_year_2", "value"),
    Input("chosen_clustering", "value"),
    Input("centroides", "value"),
)
def update_clustering(selected_file, selected_clustering,centroides):
    # Charger les données
    data_sorted, selected_year = util.charge_data(selected_file)

    # Analyse en Composantes Principales
    pca_data = analysis.get_pca(data_sorted)

    # Générer le graphique
    pca_figure = graph.plot_pca(pca_data)


    # Clustering

    
    if selected_clustering == "kmeans":
        # Silhouette scores
        scores = analysis.silhouette_scores(pca_data[['PC1', 'PC2']], 10, "kmeans")
        dynamic_n_clusters = [k for k, v in scores.items() if v == max(scores.values())][0]
        scoring_figure = graph.display_silhouette_scores(scores, "KMeans")
        # nombre optimal de cluster = n_clusters
        
        cluster, cluster_labels, centroids = analysis.kmeans_clustering(pca_data[['PC1', 'PC2']], dynamic_n_clusters)
        title = f"K-means pour {dynamic_n_clusters} clusters en {selected_year}"


    elif selected_clustering == "gmm":
        # Silhouette scores
        scores = analysis.silhouette_scores(pca_data[['PC1', 'PC2']], 10, "gmm")
        dynamic_n_clusters = [k for k, v in scores.items() if v == max(scores.values())][0]
        scoring_figure = graph.display_silhouette_scores(scores, "Gaussian Mixture")
        cluster, cluster_labels, centroids = analysis.gausian_mixture_clustering(pca_data[['PC1', 'PC2']], dynamic_n_clusters)
        title = f"Gaussian Mixture pour {dynamic_n_clusters} clusters en {selected_year}"

    elif selected_clustering == "consensus":
        centroides = False
        scores = analysis.silhouette_scores(pca_data[['PC1', 'PC2']], 10, "gmm")
        dynamic_n_clusters = [k for k, v in scores.items() if v == max(scores.values())][0]
        scoring_figure = None
        cluster_labels = analysis.consensus_clustering(pca_data[['PC1', 'PC2']], dynamic_n_clusters)
        title = f"Consensus clustering pour {dynamic_n_clusters} clusters en {selected_year}"

    df_clusters = pca_data.copy()
    df_clusters['Cluster'] = cluster_labels.astype(str)
    clustering_figure = graph.display_clustering(df_clusters, title)

    if centroides:
            clustering_figure = graph.add_centroids(clustering_figure, centroids, dynamic_n_clusters)

    # Mettre à jour le texte
    n_clusters_text = f"Meilleur nombre de clusters trouvé par la méthode silhouette : {dynamic_n_clusters}"

    return clustering_figure, pca_figure, scoring_figure, n_clusters_text
    


# Lancer le serveur
if __name__ == "__main__":
    app.run_server(debug=True)
