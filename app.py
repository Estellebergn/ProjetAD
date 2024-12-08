import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import graph_func as graph
import util_func as util
import data_analysis_func as analysis
import plotly.graph_objects as go

# Initialiser l'application Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Data Analysis Project"

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
        html.H1("Data Analysis Project", style={"textAlign": "center", "padding": "20px"}),
        html.H2("World Hapiness Report Analysis", style={"textAlign": "center", "padding": "20px"}),
        dcc.Tabs(
            id="tabs",
            value="tab1",
            children=[
                dcc.Tab(label="Data overview", value="tab1"),
                dcc.Tab(label="Clustering", value="tab2"),
                dcc.Tab(label="Network view", value="tab3"),
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
                        html.Label("Select data :"),
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
                        html.H3("Data overview"),
                        html.P(
                            """
                            The World Happiness Report is an annual study that measures and ranks countries
                            according to their level of happiness perceived by their citizens. 
                            This report is based on data from Gallup World Poll surveys. 
                            Citizens rate their lives on a scale of 0 to 10, where 10 represents the best possible life. 
                            The following factors are considered to assess happiness:
                            """
                        ),
                        html.Ul(
                            [
                                html.Li("Hapiness Score: An average of subjective ratings of life."),
                                html.Li("Logged GDP per capita : Measure of Gross Domesctic Product per capita."),
                                html.Li("Social Support : The perception of being able to rely on someone in times of need."),
                                html.Li("Healthy Life Expectancy : Life expectancy adjusted for health conditions."),
                                html.Li("Freedom to make life choices : The feeling of freedom in personal decisions."),
                                html.Li("Generosity : Tendencies to donate or help others."),
                                html.Li("Perceptions of Corruption : The perceived level of corruption in government and business."),
                            ]
                        ),
                        html.P(
                            """
                            The countries in grey on the country map are the countries for which no data is available.
                            """
                        )
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
        # Dropdown pour sélection de données
    
    html.Label("Select data :"),
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
    
    # Section ACP
    html.Div([
        html.H3("Data visualization in PCA"),
        html.P("""PCA (Principal Component Analysis) is a method used to reduce the dimensionality of data by
            projecting it onto two axes, called principal components. These axes are chosen to capture 
            the maximum variance from the original data, making it easier to visualize relationships 
            between variables while simplifying their representation."""),
        html.P("""In PCA, the distance between points in the reduced space represents their similarity 
            based on the original variables: points that are close indicate similar observations, 
            while points that are far apart reflect significant differences."""),
    ],
    style={
    "width": "97%",
    "display": "inline-block",
    "verticalAlign": "top",
    "padding": "15px",
    "marginRight": "5px",
    "backgroundColor": "#f9f9f9",
    "borderRadius": "10px",
    "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
    "textAlign": "justify",
    }),

    
    # Graphique ACP
    html.Div([
        dcc.Graph(id="dynamic_pca"),
    ], style={"width": "100%", "padding": "10px"}),

    # Section Clustering
    html.Div([
        html.H2("Clustering (K-means and Gaussian Mixture)"),
        html.P("Clustering is an unsupervised learning method used to group data based on their similarities."),
        html.Ul(
                [
                    html.Li("""K-means: A clustering method that partitions data into K clusters
                        based on the similarity of points. It is fast but assumes that clusters
                        are spherical and of similar size, which can be a limitation."""),
                    html.Li("""Gaussian Mixture Models (GMM): A probabilistic approach that models
                        data as a combination of normal distributions. Each point has a probability
                        of belonging to each cluster, offering greater flexibility compared to K-means."""),
                    html.Li("""Consensus: Used to combine k-means clustering and GMM clustering results to find a more stable
                        and robust partition, particularly useful when dealing with complex or noisy data."""),
                ]
                ),
    ],
    style={
    "width": "97%",
    "display": "inline-block",
    "verticalAlign": "top",
    "padding": "15px",
    "marginRight": "5px",
    "backgroundColor": "#f9f9f9",
    "borderRadius": "10px",
    "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
    "textAlign": "justify",
    }),
    html.P(""),

    # Dropdown pour choix d'algorithme
    html.Label("Select clustering algorithm :"),
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
    html.Div(
        id="score-container",  # ID ajouté pour le conteneur du score
        children=[
            # Graphique des scores
            html.Div([
                dcc.Graph(id="dynamic_scoring"),
            ], style={"width": "50%", "display": "inline-block"}),

            # Paragraphe silhouette score
            html.Div([
                html.P("""The Silhouette Score helps in choosing the optimal    number of clusters k
                        by measuring the quality of the clustering. A high  Silhouette Score indicates
                        that points are well grouped within their clusters  and well separated from other clusters. 
                        By testing different values of k, the highest score     identifies the number of clusters 
                        that provides the best cohesion and separation.     Therefore, the optimal k corresponds 
                        to the value with the highest score."""),
                html.P(
                    id="dynamic_n_clusters_text",
                    children="Nombre de clusters trouvé :",
                ),
            ], style={"width": "40%",
                    "display": "inline-block",
                    "verticalAlign": "top",
                    "padding": "10px",
                    "backgroundColor": "#f9f9f9",
                    "borderRadius": "10px",
                    "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                    "textAlign": "justify"}),
        ],
    ),

    # Graphique Clustering
    html.Div([
        dcc.Graph(id="dynamic_clustering", 
            style={"width": "70%", "display": "inline-block", "verticalAlign": "top", "padding": "10px"}),
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
                    style={"marginTop": "100px",
                        "marginBottom" : "20px",
                        "padding" : "10px",
                        "width" : "100%"},
                ),
                html.Div("""The three methods seem to produce similar clusterings, 
                        highlighting a certain structure in the data.""",
                        style={"width": "100%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "padding": "50px",
                        "backgroundColor": "#f9f9f9",
                        "borderRadius": "10px",
                        "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        "textAlign": "justify"}
                )   
            ],
        style={"width": "100%", "display": "inline-block", "verticalAlign": "top", "padding": "50px"},
        ),
    ],
),
])

    elif tab_name == "tab3":
        return html.Div([
            # Section Network 
            html.Label("Select data :"),
            dcc.Dropdown(
                id="chosen_year_graph",
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
        
            html.Div([
                html.H3("Country/Country correlation heatmap"),
                html.P("""The country/country correlation heatmap
                        helps identify if two countries share similar
                        trends."""),
            ],
            style={
            "width": "97%",
            "display": "inline-block",
            "verticalAlign": "top",
            "padding": "15px",
            "marginRight": "5px",
            "backgroundColor": "#f9f9f9",
            "borderRadius": "10px",
            "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
            "textAlign": "justify",
            }),

            # Heatmap
            dcc.Graph(id="country_heatmap", style={"width": "65%", "display": "inline-block", "padding": "10px"}),
            html.Div(
                html.P("gnagnagni"),
                style={"width": "30%", "display": "inline-block", "padding": "10px", "verticalAlign": "top"},
                ),
            # Network
            html.H2("Visualisation du réseau de pays"),
            html.Label("Seuil de corrélation :"),
            dcc.Slider(
                id="threshold",
                min=0,
                max=1,
                step=0.05,
                value=0.6,
                marks={i: str(i) for i in [0, 0.2, 0.4, 0.6, 0.8, 1]},                
            ),
            dcc.Graph(id="dynamic_network", style={"width": "75%", "display": "inline-block", "padding": "10px"}),
            dcc.RadioItems(
                id="community",
                options=[
                    {"label": "Avec communautés", "value": True},
                    {"label": "Sans communautés", "value": False},
                ],
                value=False,
                style={"marginTop": "-50px", "display": "inline-block", "width": "20%", "marginBottom": "50px"},
            ),

        ]),




# Callback overview
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


# Callback consensus
@app.callback(
    [
        Output("radioitems-container", "style"),
        Output("score-container", "style")
    ],
    Input("chosen_clustering", "value")
)
def toggle_visibility(selected_clustering):
    if selected_clustering == "consensus":
        # Masquer les RadioItems et le conteneur des scores
        return (
            {"display": "none"},  # RadioItems masqués
            {"display": "none"}   # Score masqué
        )
    else:
        # Afficher les RadioItems et le conteneur des scores
        return (
            {"width": "15%", "display": "inline-block", "verticalAlign": "top", "padding": "10px"},
            {"display": "block"}  # Score visible
        )


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

    #Initialisation
    scoring_figure = None
    dynamic_n_clusters = None
    title = ""
    cluster_labels = None
    centroids = None

    # Clustering
    if selected_clustering == "kmeans":
        # Silhouette scores
        scores = analysis.silhouette_scores(pca_data[['PC1', 'PC2']], 10, "kmeans")
        dynamic_n_clusters = [k for k, v in scores.items() if v == max(scores.values())][0]
        scoring_figure = graph.display_silhouette_scores(scores, "KMeans")
        # nombre optimal de cluster = n_clusters
        
        cluster, cluster_labels, centroids = analysis.kmeans_clustering(pca_data[['PC1', 'PC2']], dynamic_n_clusters)
        title = f"K-means for {dynamic_n_clusters} clusters in {selected_year}"


    elif selected_clustering == "gmm":
        # Silhouette scores
        scores = analysis.silhouette_scores(pca_data[['PC1', 'PC2']], 10, "gmm")
        dynamic_n_clusters = [k for k, v in scores.items() if v == max(scores.values())][0]
        scoring_figure = graph.display_silhouette_scores(scores, "Gaussian Mixture")
        cluster, cluster_labels, centroids = analysis.gausian_mixture_clustering(pca_data[['PC1', 'PC2']], dynamic_n_clusters)
        title = f"Gaussian Mixture for {dynamic_n_clusters} clusters in {selected_year}"

    elif selected_clustering == "consensus":
        centroides = False
        scores = analysis.silhouette_scores(pca_data[['PC1', 'PC2']], 10, "gmm")
        dynamic_n_clusters = [k for k, v in scores.items() if v == max(scores.values())][0]
        scoring_figure = None
        cluster_labels = analysis.consensus_clustering(pca_data[['PC1', 'PC2']], dynamic_n_clusters)
        title = f"Consensus clustering for {dynamic_n_clusters} clusters in {selected_year}"

    df_clusters = pca_data.copy()
    df_clusters['Cluster'] = cluster_labels.astype(str)
    clustering_figure = graph.display_clustering(df_clusters, title)

    if centroides:
            clustering_figure = graph.add_centroids(clustering_figure, centroids, dynamic_n_clusters)

    # Mettre à jour le texte
    n_clusters_text = f"Best number of clusters found by the silhouette method : {dynamic_n_clusters}"

    return clustering_figure, pca_figure, scoring_figure, n_clusters_text
    


@app.callback(
    Output("country_heatmap", "figure"),
    Output("dynamic_network", "figure"),
    Input("chosen_year_graph", "value"),
    Input("threshold", "value"),
    Input("community", "value"),
)
def update_network(selected_file, chosen_threshold, community):
    # Charger les données
    data_sorted, selected_year = util.charge_data(selected_file)

    # Générer la heatmap
    correlation_matrix = analysis.get_country_heatmap(data_sorted)
    heatmap_figure = graph.plot_heatmap(correlation_matrix)

    # Générer le graphe
    graph_data = analysis.get_country_graph(correlation_matrix, chosen_threshold)
    if community:
        graph_data, partition = analysis.add_community(graph_data)
        network_figure = graph.display_network(graph_data, list(partition.values()))
    else:
        network_figure = graph.display_network(graph_data, util.standardise(data_sorted)["Happiness Score"])  


    return heatmap_figure, network_figure

# Lancer le serveur
if __name__ == "__main__":
    app.run_server(debug=True)
