import pandas as pd
import os
from os.path import exists
import yaml

def get_data(url, selected_variables): 
# Importation des données de l'ADEME
    df = pd.read_csv(url, encoding="latin1", sep=";", decimal=',') # les nombres décimaux sont séparées par des virgules dans le csv.
    df.dropna(subset=['co2'], inplace = True)
    df = df.drop_duplicates(keep = "first")
    y = df['co2']
    X  = df[selected_variables]
    return X, y


def import_yaml_config():
    CONFIG_PATH = './configuration/config.yaml'
    FIGNAME=""
    DATADIR = ""
    DATANAME= ""
    FIGDIR = ""
    SEED = ""
 

 
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as stream:
            config = yaml.safe_load(stream)
            print(config)
            FIGNAME = config.get("figname", "train.csv")
            DATA = config['data']#
            #DATANAME = config['data']['name'] 
            FIGDIR = config.get("figdir", "./reports/figures2")
            SEED = config.get("SEED", 1022)
            selected_variables  = config.get("selected_variables") 
            variables_for_encoding = config.get("variables_for_encoding")
            # TEST_FRACTION = config.get("test_fraction", .1)
    return FIGNAME, DATA, FIGDIR, SEED,selected_variables,variables_for_encoding
