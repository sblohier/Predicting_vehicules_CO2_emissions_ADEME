import os
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error, root_mean_squared_error, r2_score
)
from adememl.visualization.plot_pred_vs_obs import (pred_vs_reel_scatterplot,
                               residual_boxplot)


# Set encoding var
def sep_var_encoding(df, var_enc):
    other_variables = df.columns.tolist()
    for var in var_enc:
        other_variables.remove(var)
    return var_enc, other_variables


# Définition de la fonction R2_adjusted
def calcul_r2_adjusted (n, r2, k) :
    return 1-(1-r2)*(n-1)/(n-k-1)

# Set pipeline
def set_pipeline(var1, var2):
    # Définition du préprocesseur
    preprocessor = ColumnTransformer(
            transformers=[
                ("cat_text", OrdinalEncoder(handle_unknown="use_encoded_value",
                                            unknown_value=-1), var1),
                ("keep_columns", "passthrough", var2)
            ]
        )

    # Définition du pipeline de transformation pipe_mod1_ord_enc
    pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', LinearRegression())])
    return pipe


# Définition de la fonction get_perf_stat qui calcule la MAE, RMSE, R2 et R2
# ajusté à partir des vecteurs y (target observée) , y_pred (target prédite)
# et de nb_var (le nombre de features)
def get_perf_stat(y, y_pred, nb_var, text) :
    MAE = round(mean_absolute_error(y, y_pred),2)
    RMSE = round(root_mean_squared_error(y, y_pred),2)
    R2 = round(r2_score(y, y_pred),4)
    R2_Adjusted = round(calcul_r2_adjusted (len(y_pred), R2, nb_var),4)
    # Affichage des performances :
    print(f"Les performances sur le set de {text} sont :")
    print(f"MAE :  {MAE}, RMSE : {RMSE}, R2 : {R2}, R2 ajusté : {R2_Adjusted}")

# Concat all methods
def perf_stat(pipe, X, y, text,  dict_order_gamme, dict_order_carrosserie, dir,name):
    print(dir)
    print(name)
    if not os.path.exists(dir):
        os.makedirs(dir)
    y_pred = pipe.predict(X)
    get_perf_stat(y, y_pred, X.shape[1], text)
    pred_vs_reel_scatterplot(y_pred,y,X, dir, name + "_scatter")
    residual_boxplot(y_pred, y, X, dict_order_carrosserie, dict_order_gamme, dir,name + "_residual_error_bp")
    