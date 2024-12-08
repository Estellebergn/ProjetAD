import pandas as pd

# Fonction pour normaliser les noms de colonnes
def normalize_columns(df, filename):    

    # Filtre colonnes
    exclude_keywords = ["Dystopia", "whisker", "Explained by", "error"]
    df = df[[col for col in df.columns if not any(keyword in col for keyword in exclude_keywords)]]
    # Renommage des colonnes
    column_mapping = {
        "Happiness.Score": "Happiness Score",
        "Ladder score": "Happiness Score",
        "Score": "Happiness Score",
        "Health..Life.Expectancy." : "Healthy life expectancy",
        "Freedom to make life choices": "Freedom",
        "Trust..Government.Corruption.": "Perceptions of corruption",
        "Family": "Social support",
        'Country name' : "Country",
        "Country or region": "Country",
        "Economy..GDP.per.Capita.": "Logged GDP per capita",
        "GDP per capita" : "Logged GDP per capita",

    
    }
    df.columns = [column_mapping.get(col, col) for col in df.columns]
    # Ajout de la colonne "Regional indicator" si manquante
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


# Standardisation du df
def standardise(df):
    df_numeric = df.select_dtypes(include=['float64', 'int64'])
    df_standardise = (df_numeric - df_numeric.mean()) / df_numeric.std()
    return df_standardise


def charge_data(filename):
    df = pd.read_csv(filename)
    selected_year = filename.split("/")[-1].split(".")[0]
    data = normalize_columns(df, filename)
    data_sorted = data.sort_values(by="Happiness Score", ascending=False)
    return data_sorted, selected_year
