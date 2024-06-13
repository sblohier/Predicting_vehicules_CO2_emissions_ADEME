# Explication de la fonction
def get_dict(df) :
    dict_order_gamme = { "ECONOMIQUE" : 0, "INFERIEURE" : 1,
                        "MOY-INFER": 2,  "MOY-SUPER" : 3,
                        "SUPERIEURE" : 4,  "LUXE" : 5}
    df.loc[df["Carrosserie"] == "COMBISPCACE","Carrosserie"] = "COMBISPACE"
    # Création de la base df0 qui associe à chaque catégorie de la 
    # variable Carrosserie, la masse médiane des véhicules, triées par order croissant de masse :
    df0 = df.groupby(by="Carrosserie").agg({
        'masse_ordma_min' : 'median'}).sort_values(by="masse_ordma_min", 
                                                   ascending= True).reset_index()
    # Création d'un dictionnaire préservant l'ordre des catégories de la variable 'Carrosserie'
    dict_order_carrosserie = dict(zip(df0["Carrosserie"], df0.index))
    return dict_order_gamme, dict_order_carrosserie

# Création de la fonction convert_carburant qui convertit :
# "ES", EH, EE --> "ESSENCE"
# "GO", "GH", "GL" --> "GAZOIL"
# Les autres carburants --> "AUTRE"
def convert_carburant(x) :
    carburant = "ESSENCE"
    if x.startswith("G") and x not in ["GP", "GN"] :
        carburant = "GAZOIL"
    elif x in["GN", "FE", "GP"] :
        carburant = "AUTRE"
    return carburant


# Définition d'une fonction traitant les variables catégorielles
def transform_variables(df, dict_order_gamme, dict_order_carrosserie) :
    df_new = df.copy()

    # Transformation des modalités de la variable 'cod_cbr' :
    df_new["cod_cbr"] = df["cod_cbr"].apply(lambda x : str(x).split("/", maxsplit=1)[0])
    df_new["cod_cbr"] = df["cod_cbr"].map(convert_carburant).to_list()

    # Split de 'typ_boite_nb_rapp' en 2 variables 'Type_Boite_Vitesse' et 'Nb_rapports' :
    df_new[["Type_Boite_Vitesse", "Nb_rapports"]] =  df["typ_boite_nb_rapp"].str.split(expand = True)
    df_new.loc[df_new['Nb_rapports'] == ".", 'Nb_rapports'] = "0"
    df_new['Nb_rapports'] = df_new['Nb_rapports'].astype(int)
    df_new["Type_Boite_Vitesse"]= df_new["Type_Boite_Vitesse"].map({"A" : "AUTOMATIQUE", "M" : "MANUELLE", "V" : "AUTRE", "S" : "AUTRE", "D" : "AUTRE"})
    df_new.drop(columns = "typ_boite_nb_rapp", inplace = True)

    # Transformation et encodage des modalités de la variable 'gamme' :
    df_new.loc[df_new["gamme"] == "MOY-INFERIEURE","gamme"] = "MOY-INFER"
    df_new["gamme"] = df_new["gamme"].map(dict_order_gamme)

    # Transformation et encodage des modalités de la variable 'Carrosserie' :
    df_new.loc[df_new["Carrosserie"] == "COMBISPCACE","Carrosserie"] = "COMBISPACE"
    df_new["Carrosserie"] = df_new["Carrosserie"].map(dict_order_carrosserie)

    return df_new


def outlier_treatment(df_):
    df = df_.copy()
    # Création d'une variable booléenne 'outlier_puiss_max' spécifiant si l'observation est un outlier :
    df["outlier_puiss_max"] = False
    df.loc[(df["puiss_max"]> 500) | (df["puiss_max"] < 40), "outlier_puiss_max"] = True

    # Imputation des seuils pour la puissance max :
    df.loc[(df["puiss_max"]> 500) & (df["outlier_puiss_max"] is True), "puiss_max"] = 500
    df.loc[(df["puiss_max"]< 40) & (df["outlier_puiss_max"] is True), "puiss_max"] = 40

    # Création d'une variable booléenne 'outlier_conso_mixte' spécifiant si l'observation est un outlier :
    df["outlier_conso_mixte"] = False
    df.loc[(df["conso_mixte"]> 20) | (df["conso_mixte"] < 3), "outlier_conso_mixte"] = True


    # Imputation des seuils pour la conso_mixte :
    df.loc[(df["conso_mixte"]> 20), "conso_mixte"] = 20
    df.loc[(df["conso_mixte"]< 3), "conso_mixte"] = 3

    # Imputation des seuils pour la conso_mixte :
    df.loc[(df["conso_mixte"] == 3) & (df["cod_cbr"] == "GAZOIL"), "co2"] =  3*(2.6*10)
    df.loc[(df["conso_mixte"] == 3) & (df["cod_cbr"] == "ESSENCE"), "co2"] =  3*(2.3*10)
    df.loc[(df["conso_mixte"] == 20) & (df["cod_cbr"] == "ESSENCE"), "co2"] =  20*(2.3*10)
    df.drop(columns=['outlier_puiss_max', "outlier_conso_mixte"], inplace= True)
    return df
