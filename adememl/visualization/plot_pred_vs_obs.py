# Importation des packages
import matplotlib.pyplot as plt
import seaborn as sns



# Création de 2*2 scatterplots des y predits versus les y réels en fonction
# du carburant et de la nature hybride des véhicules
# Les 2 figures du haut sont les comparaisons sur le jeu d'entraînement
# Les 2 figures du bas sont les comparaisons sur le jeu de validation
def pred_vs_reel_scatterplot(y_train_pred, y_train, df_train, dir,name) :
    # 0.  Création de la figure et des axes
    fig, axe = plt.subplots(nrows = 1, ncols = 2, figsize=(14, 6))
    palette_cod_cbr ={"ESSENCE": "green", "GAZOIL": "orange", "AUTRE":"grey"}
    palette_hybride ={"oui": "#CC2D35", "non": "blue"}

    y_reel = y_train
    y_pred = y_train_pred
    df = df_train
    # on itère sur les 2 variables "cod_cbr", "hybride"
    palette = palette_cod_cbr
    for j, var in enumerate(["cod_cbr", "hybride"]) :
        #1. Création du scatterplot
        sns.scatterplot(ax=axe[j], data=df, x = y_reel,
                        y=y_pred, alpha=0.5, hue = var, palette = palette)
        #2. On ajoute la ligne y_pred = y_reel
        sns.lineplot(ax=axe[j],  x = y_reel, y=y_reel,alpha=0.5, color="black")

        #3 Définitions des labels sur les axes
        axe[j].set_xlabel("Emissions de co2 (g/km) - Observations")
        axe[j].set_ylabel('Emissions de co2 (g/km) - Prédictions')

        #4. Ajout des lignes horizontales
        axe[j].grid(visible=True, which='major', axis='y')
        axe[j].spines['top'].set_visible(False)
        axe[j].spines['right'].set_visible(False)
        axe[j].spines['bottom'].set_visible(True)
        axe[j].spines['left'].set_visible(False)

        #5. Ajout de la légende
        legend =axe[j].legend()
        legend.set_title(var)
        if var == "cod_cbr" :
            legend.set_title("Carburant")
        palette = palette_hybride

    #3. Ajout des titres
    axe[0].set_title(
        "Prédiction des émissions de CO2 vs les émissions réelles - Jeu de données d'entrainement",
         loc='left' ,fontsize=13)
    plt.savefig(dir+'/'+ name+'.png', dpi=300)
    


# Création de 6 boxplots représentant la distribution des erreurs résiduelles relatives
# (y_pred - y_reel)/y_reel pour les 6 variables catégorielles.

def residual_boxplot(y_pred, y, df_, dict_carrosserie, dict_gamme, dir, name) :
    df = df_.copy()

    # On calcule les erreurs résiduelles relatives
    y_diff_rel = abs(y_pred - y)/y
    print(y_diff_rel.mean())

    # On génère les dictionnaires inverses pour variables carrosseries et gamme
    dict_carrosserie_inverse = {v: k for k, v in dict_carrosserie.items()}
    dict_gamme_inverse = {v: k for k, v in dict_gamme.items()}

    # On inverse l'encodage ordinal des variables 'Carrosserie' et 'gamme'
    df["Carrosserie"] = df["Carrosserie"].apply(lambda x : dict_carrosserie_inverse[int(x)])
    df["gamme"] = df["gamme"].map(lambda x : dict_gamme_inverse[int(x)])

    # 0. Définition de la figure et des 6 axes :
    fig = plt.figure(constrained_layout=True, figsize = (15,6))
    gs = fig.add_gridspec(2, 4)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax4 = fig.add_subplot(gs[0, 3])
    ax5 = fig.add_subplot(gs[1, :2])
    ax6 = fig.add_subplot(gs[1, 2:])
    ax = [ax1, ax2, ax3, ax4, ax5, ax6]

    # On itère sur chaque variable catégorielle à représenter en abscisse
    for i,v in enumerate(["cod_cbr", "hybride", "Type_Boite_Vitesse",
                          "Nb_rapports","Carrosserie", "gamme"]) :

        # Gestion de l'ordre des catégories
        order = None
        if v == "Carrosserie" :
            order =dict_carrosserie
        if v == "gamme":
            order =dict_gamme

        # 1. Création d'un boxplot
        sns.boxplot(ax=ax[i], y=y_diff_rel ,x = v, data=df, color = "#9a9aff",
                    flierprops={"marker": ".", "markersize" : "4"}, width= 0.7 , order = order)

        # 2. Gestion des axis et labels
        ax[i].set_xlabel(v)
        ax[i].set_ylabel("")
        if (i == 0) | (i == 4)  :
            ax[i].set_ylabel("Erreur résiduelle relative  (-)", fontsize=9)
        # 3. Ajout des lignes horizontales
        ax[i].grid(visible=True, which='major', axis='y')

        # Pour plus de lisibilité pour les variables présentant des modalités
        # caractérisées par de longues chaines de caractères nous pivotons les labels :
        if (v == "Carrosserie")  | (v == "gamme"):
            ax[i].set_xticklabels(ax[i].get_xticklabels(), rotation=30, ha='right', fontsize=9)
        ax[i].spines['top'].set_visible(False)
        ax[i].spines['right'].set_visible(False)
        ax[i].spines['bottom'].set_visible(True)
        ax[i].spines['left'].set_visible(False)
        ax[i].set_ylim(0, 0.001)

    # 4. Ajout du titre principal
    fig.suptitle('Distribution de l\'erreur résiduelle prédite pour les variables catégorielles.')
    plt.savefig(dir+'/'+ name + '.png', dpi=300)
    
