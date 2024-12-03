import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx

def get_hist(data, year):
    # Graphique interactif
    fig = px.bar(
        data,
        x='Country',
        y='Happiness Score',
        title='Histogramme du score de bonheur par pays en {}'.format(year),
        color='Regional indicator',
        color_discrete_sequence=px.colors.qualitative.T10 ,
        template='plotly_white',
    )
    # Supprimer les labels de l'axe des abscisses
    fig.update_xaxes(showticklabels=False)
    fig.update_xaxes(categoryorder='total descending')
    # Modifier les noms des axes
    fig.update_yaxes(range=[0, 10])
    return fig

def get_carte(data, year):
    carte = px.choropleth(
        data,
        locations='Country',
        locationmode='country names',
        color='Happiness Score',
        title='Carte du score de bonheur par pays en {}'.format(year),
        color_continuous_scale='thermal',
    )
    carte.update_geos(showframe=False, showcoastlines=False)
    carte.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    # Diminuer la légende
    carte.update_coloraxes(colorbar_title="Happiness<br>Score", colorbar_thickness=15)

    return carte

def plot_pca(pca_data):
    fig = px.scatter(
        pca_data, 
        template='plotly_white',
        x='PC1', 
        y="PC2", 
        hover_name='Country',
        color='Regional indicator',
        hover_data={   # Masquer ou montrer
            'Country': False,
            'Regional indicator': False,
            'Happiness Score': True,
            'Generosity': True,
            'Social support': True,
            'Logged GDP per capita': True,
            'Healthy life expectancy': True,
            'Freedom': True,
            'Perceptions of corruption': True
        },
        color_discrete_sequence=px.colors.qualitative.G10,
        title='ACP des pays selon le score de bonheur en fonction des variables explicatives',
    )
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(
        height=400)
    return fig



def display_silhouette_scores(scores, method_name) :
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(scores.keys()),
        y=list(scores.values()),
        mode='lines+markers',
        name='Silhouette Score',
        line=dict(color='blue'),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title=f"Méthode de la silhouette pour {method_name}",
        xaxis_title='Nombre de clusters',
        yaxis_title='Indice de silhouette moyen',
        template='plotly_white',
        height=300,
    )

    return fig



def display_clustering(df, title="") :
    """
    Affiche le graphique des clusters obtenus
    sur les deux premières composantes principales
    
    :param df: DataFrame contenant les données
    :type df: pandas.DataFrame
    :return: Le graphique des clusters obtenus
    :rtype: plotly.graph_objs._figure.Figure
    """
    fig_kmeans = px.scatter(
    template='plotly_white',
    data_frame=df, 
    x='PC1', 
    y='PC2', 
    color='Cluster', 
    hover_name='Country',
    color_discrete_sequence=px.colors.qualitative.G10,
    title=title
)
    fig_kmeans.update_layout(showlegend=False)
    return fig_kmeans


def add_centroids(fig, centroids, n_clusters) :
    # Convertir en DataFrame pour manipulation
    centroids_df = pd.DataFrame(centroids, columns=['PC1', 'PC2'])
    centroids_df['cluster'] = range(n_clusters)
    fig.add_trace(
    go.Scatter(
        x=centroids_df['PC1'],
        y=centroids_df['PC2'],
        mode='markers',
        marker=dict(size=12, color='black', symbol='x'),
        name='Centroïdes'
        )
    )
    
    # Cacher la légende
    fig.update_layout(showlegend=False)
    return fig


def plot_heatmap(df) : 
    fig = px.imshow(
    df,
    title="Correlation Heatmap",
    labels=dict(x="Columns", y="Columns", color="Correlation"),
    color_continuous_scale="RdBu",
    zmin=-1, zmax=1, text_auto=True,
    )
    fig.update_layout(width=800, height=700)
    return fig


def display_network(graph, color_by) :
    # Positionnement des nœuds avec spring_layout
    pos = nx.spring_layout(graph, seed=42)

    # Préparer les données pour Plotly
    edge_x = []
    edge_y = []

    # Ajout des arêtes
    for edge in graph.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)  # None pour séparer les lignes
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Tracer les arêtes
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines"
    )

    # Ajouter les nœuds
    node_x = []
    node_y = []
    node_labels = []

    for node in graph.nodes(data=True):
        x, y = pos[node[0]]
        node_x.append(x)
        node_y.append(y)
        node_labels.append(node[1]['label'])

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_labels,
        textposition="top center",
        hoverinfo="text",
        marker=dict(
            color = color_by,
            colorscale="Plasma",
            size=10,
            line_width=2
        )
    )

    # Créer la figure Plotly
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f"Réseau des corrélations",
                        titlefont_size=16,
                        showlegend=False,
                        hovermode="closest",
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    ))

    return fig
