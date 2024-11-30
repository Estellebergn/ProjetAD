import pandas as pd

# Fonction pour normaliser les noms de colonnes
def normalize_columns(df, filename):
    column_mapping = {
        "Happiness.score": "Happiness Score",
        "Ladder score": "Happiness Score",
        "Score": "Happiness Score",
        "Happiness Score": "Happiness Score",
        "Health..Life.Expectancy." : "Healthy life expectancy",
        "Freedom to make life choices": "Freedom",
        "Trust..Government.Corruption.": "Perceptions of corruption",
        "Family": "Social support",
        'Country name' : "Country",
        "Country or region": "Country",
    
    }
    df.columns = [column_mapping.get(col, col) for col in df.columns]
    if "Regional indicator" not in df.columns:
        df = add_region(df, filename)
    return df


def add_region(df,filename):
    data_with_region = pd.read_csv("data/2020.csv", usecols=["Country name", "Regional indicator"])
    data_with_region.columns = ["Country", "Regional indicator"]
    # Fusionner df1 et df2 sur la colonne "Country"
    df_merged = pd.merge(df, data_with_region[["Country", "Regional indicator"]], on="Country", how="left")
    # Sauvegarder le résultat
    df_merged.to_csv(filename, index=False)
    return df_merged
