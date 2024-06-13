# Importation des packages
from sklearn.model_selection import train_test_split
from adememl.data.read_data import (get_data, import_yaml_config)
from adememl.data.preprocess_variables import (transform_variables, get_dict,outlier_treatment)
from adememl.models.train_model import (set_pipeline, sep_var_encoding, perf_stat)



if __name__ == '__main__':
    FIGNAME, DATA,FIGDIR, SEED,selected_variables,variables_for_encoding = import_yaml_config()
   

    # Importation des données de l'ADEME
    X,y =get_data(DATA['dir']+'/' + DATA['name'], selected_variables)

    # Création du jeu de train/validation et de test
    X_train_val,  X_test, y_train_val,y_test = train_test_split(X,y, test_size=0.25, random_state=SEED)

    # Récupérer les dictionnaies
    dict_order_gamme, dict_order_carrosserie = get_dict(X_train_val)

    ## Appliquons la fonction transform_variables à df_train_val
    X_train_val = transform_variables(X_train_val,dict_order_gamme, dict_order_carrosserie)
    X_train_val = outlier_treatment(X_train_val)

    # Split train / val
    X_train, X_val, y_train,y_val = train_test_split(X_train_val,y_train_val,
                                                    test_size = 0.3, random_state = SEED)

    # Définition de la liste de variables catégorielles pour lesquelles
    # nous testerons 2 types d'encodage
    variables_for_encoding, other_variables = sep_var_encoding(X_train,
                                                            ["hybride", "cod_cbr", "Type_Boite_Vitesse"])

    pipe = set_pipeline(variables_for_encoding, other_variables)


    # Entrainement du modèle à l'aide de (X_train, y_train), et prédiction de y_train_pred
    pipe.fit(X_train, y_train)
    # Evaluation des performances du modèle sur l'échantillon d'entraînement
    perf_stat(pipe, X_train, y_train, 'train',dict_order_gamme, dict_order_carrosserie, FIGDIR+"/train",FIGNAME )
    perf_stat(pipe, X_val, y_val, 'validation',dict_order_gamme, dict_order_carrosserie, FIGDIR+"/val",FIGNAME )
    # Appliquons la fonction transform_variables à nos données test (nous obtiendrons une variable de plus)
    X_test = transform_variables(X_test,dict_order_gamme, dict_order_carrosserie)

    # Prédictions sur l'échantillon de test
    perf_stat(pipe, X_test, y_test, 'test',dict_order_gamme, dict_order_carrosserie, FIGDIR+"/test",FIGNAME )