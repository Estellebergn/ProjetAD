import pandas as pd
import plotly.express as px

def get_hist(data):
    # Graphique interactif
    fig = px.bar(
        data,
        x='Country',
        y='Happiness Score',
        title='Histogramme du score de bonheur par pays en 2020',
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

def get_carte(data):
    carte = px.choropleth(
        data,
        locations='Country',
        locationmode='country names',
        color='Happiness Score',
        title='Carte du score de bonheur par pays en 2020',
        color_continuous_scale='thermal',
    )
    carte.update_geos(showframe=False, showcoastlines=False)
    carte.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return carte