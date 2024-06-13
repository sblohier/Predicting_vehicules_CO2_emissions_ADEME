# Predicting_vehicules_CO2_emissions_ADEME

## Description du projet

Ce projet de scoring consiste en la construction d'une modélisation prédictive ayant pour objectif d’identifier les clients fragiles d’une entreprise de télécommunication, à savoir les clients susceptibles de résilier leur contrat prochaînement.

Cette étude a pour objectif de bâtir une modélisation prédictive des émissions de CO2 des véhicules basée sur leurs caractéristiques techniques et environnementales.

Nous disposons pour ce faire d'un jeu de données labellisées provenant de l'ADEME. Ces données ont été collectées depuis 2001, leur dernière mise à jour date d'octobre 2015. Elles contiennent la liste des références des véhicules commercialisés en France ainsi que leurs caractéristiques techniques, administratives, leurs émissions en polluants et gaz à effet de serre (CO, CO2, NOx ..) et leur norme EURO.

Nos données étant labellisées, le modèle que nous allons mettre en place est un modèle d'apprentissage supervisé suivant une tâche de régression.

L'évaluation de notre solution et de sa capacité de généralisation sera effectuée principalement par le biais des métriques suivantes : la MAE, le coefficient de détermination (R2) et la RMSE.

L'analyse préalable concernant la présélection des variables pertinentes est disponible dans ./notebooks/ADEME_Project.ipynb et n'est pas reprise dans `main.py`.
En utilisant un filtre univarié, nous avons réduit le nombre de variables explicatives de 25 à 8.

Les librairies utilisées sont dispo dans `requirements.txt`

## Structure du projet 


```bash
├── data
│   └── raw            <- vehicules.csv
├── docs               <- main.py
│
├── notebooks          <- Jupyter notebooks.
|                         ADEME_Project.ipynb
│
├── reports            <- presentation.pdf
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
│
└── adememl                <- Source code for use in this project.
    │
    ├── __init__.py    <- Makes scoring_project a Python module
    │
    ├── data           <- Scripts to read and preprocess data
    │   └── preprocess_variables.py
    │   └── read_data.py
    |
    ├── models         <- Scripts to train models and then use trained models to make
    │   │                 predictions
    │   ├── train_model.py
    |
    ├── visualization  <- Scripts for visualize model results
    │   ├── plot_pred_vs_obs.py


```



