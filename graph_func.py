import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
        template='plotly_white'
    )

    return fig



def display_kmeans(df) :
    """
    Affiche le graphique des clusters obtenus par KMeans
    sur les deux premières composantes principales
    
    :param df: DataFrame contenant les données
    :type df: pandas.DataFrame
    :return: Le graphique des clusters obtenus par KMeans
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
)
    fig_kmeans.update_layout(showlegend=False)
    return fig_kmeans