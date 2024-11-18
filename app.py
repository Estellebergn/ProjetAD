import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Exemple de jeu de données
df = px.data.gapminder()

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
                dcc.Tab(label="Données", value="tab1", style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label="Analyses", value="tab2", style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label="Informations", value="tab3", style=tab_style, selected_style=tab_selected_style),
            ],
        ),
        html.Div(id="content"),
    ]
)

# Callbacks pour gérer les onglets
@app.callback(
    Output("content", "children"),
    Input("tabs", "value"),
)
def render_tab_content(tab_name):
    if tab_name == "tab1":
        # Graphique interactif
        df = pd.read_csv("data/2020.csv")
        # Histogramme
        data_2020 = df.sort_values(by='Ladder score', ascending=False)
        fig = px.bar(
            data_2020,
            x='Country name',
            y='Ladder score',
            title='Histogramme du score de bonheur par pays en 2020',
            color='Regional indicator'
        )
        fig.update_xaxes(categoryorder='total descending')
        return html.Div(
            [
                dcc.Graph(figure=fig),
            ],
            style={"padding": "10px"},
        )

    elif tab_name == "tab2":
        # Analyse
        html.H3("Heatmap"),
        # Calculate the correlation matrix
        df_heatmap = data_2020[['Ladder score', 'Logged GDP per capita', 'Social support', 'Healthy life expectancy', 'Freedom to make life choices','Perceptions of corruption', 'Generosity']]
        correlation_matrix = df_heatmap.corr()
        # Create the heatmap
        fig = px.imshow(
            correlation_matrix,
            title="Correlation Heatmap",
            labels=dict(x="Columns", y="Columns", color="Correlation"),
            color_continuous_scale="RdBu",
            zmin=-1, zmax=1, text_auto=True
        )
        fig.update_layout(width=900, height=800)
        return html.Div(
        [
            dcc.Graph(figure=fig),
        ],
        style={"padding": "10px"},
    )

    elif tab_name == "tab3":
        # Informations supplémentaires
        return html.Div(
            [
                html.H3("À propos de cette application"),
                html.P("Cette application a été créée avec Dash pour démontrer l'utilisation des onglets."),
                html.Ul(
                    [
                        html.Li("Tab 1 : Graphiques interactifs."),
                        html.Li("Tab 2 : Affichage des données."),
                        html.Li("Tab 3 : Informations supplémentaires."),
                    ]
                ),
            ],
            style={"padding": "20px"},
        )

# Lancer le serveur
if __name__ == "__main__":
    app.run_server(debug=True)
