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
        title='Histogram of happiness score by country in {}'.format(year),
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
        title='Happiness Score Map by Country in {}'.format(year),
        color_continuous_scale='thermal',
    )
    carte.update_geos(showframe=False, showcoastlines=False)
    carte.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    # Diminuer la légende
    carte.update_coloraxes(colorbar_title="Happiness<br>Score", colorbar_thickness=15)

    return carte

def get_heatmap(corr_data, year) :
    fig = px.imshow(
        corr_data,
        title=f"Correlation of measured heatmap in {year}",
        labels=dict(x="Columns", y="Columns", color="Correlation"),
        color_continuous_scale="RdBu",
        zmin=-1, zmax=1, text_auto=True
        )
    fig.update_layout(width=900, height=800)
    return fig

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
        title='PCA of countries according to happiness score and measured variables.',
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
        title=f"Silhouette method {method_name}",
        xaxis_title='Cluster number',
        yaxis_title='Average Silhouette Index',
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
        name='Centroïds'
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


def display_network(graph, color_by, hapiness_score = None) :
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
        mode="lines",
        showlegend=False
    )

    # Ajouter les nœuds
    node_x = []
    node_y = []
    node_labels = []
    node_hovertext = []
    legend_traces = []

    for i, node in enumerate(graph.nodes(data=True)):
        x, y = pos[node[0]]
        node_x.append(x)
        node_y.append(y)

        label = node[1]['label']
        node_labels.append(label)
        value = color_by[i]

        if hapiness_score != None :
            score = hapiness_score[i]
            node_hovertext.append(f"{label} <br>Community : {value:.0f} <br>Hapiness score : {score:.2f}")
        else : 
            node_hovertext.append(f"{label} <br>Hapiness score : {value:.2f}")

    if hapiness_score == None : 
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=node_labels,
            textposition="top center",
            hoverinfo="text",
            hovertext=node_hovertext,
            marker=dict(
                color = color_by,
                colorscale="Plasma",
                size=10,
                line_width=2,
                colorbar=dict(
                title="Happiness Score Value", 
                thickness=15,
                xanchor="left", 
                titleside="right"),
            ),
            showlegend=False
    )
    else :
        discrete_colorscale = px.colors.qualitative.Set2
        categories = list(set(color_by))
        category_to_color = {cat: discrete_colorscale[i % len(discrete_colorscale)] for i, cat in enumerate(categories)}

        #node color
        node_colors = [category_to_color[col] for col in color_by]

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=node_labels,
            textposition="top center",
            hoverinfo="text",
            hovertext=node_hovertext,
            marker=dict(
                color = node_colors,
                size=10,
                line_width=2
            ),
            showlegend=False
        )

        for cat, color in category_to_color.items():
            legend_trace = go.Scatter(
                x=[None],  # Pas de données réelles, juste pour la légende
                y=[None],
                mode="markers",
                marker=dict(
                    color=color,
                    size=10,
                    line_width=2
                ),
                name=f"Community {cat}",  # Nom de la catégorie
                showlegend=True
            )
            legend_traces.append(legend_trace)


    # Créer la figure Plotly
    fig = go.Figure(data=[edge_trace, node_trace] + legend_traces,
                    layout=go.Layout(
                        title=f"Correlation between countries network",
                        titlefont_size=16,
                        showlegend=True,
                        hovermode="closest",
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    ))

    return fig
