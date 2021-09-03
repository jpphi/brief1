#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 15:43:44 2021

@author: jpphi
"""

import pandas as pd
import dash_table

import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import plotly.graph_objects as go

#import pickle

from apps import var

from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import RobustScaler, LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error

# La standardisation est nécessaire avec le SVR sinon les résultats sont abbérant
var.clf_svr = make_pipeline(StandardScaler(), SVR(C=10, epsilon=0.2))
var.clf_svr.fit(var.X, var.y)

# Régression linéaire
var.clf_reg = LinearRegression()
var.clf_reg.fit(var.X, var.y)

final = {}
num_model= 0
for model in [var.clf_reg, var.clf_svr]:
    pred= model.predict(var.X)
    rmse= np.sqrt(mean_squared_error(var.y,pred))
    mae= mean_absolute_error(var.y,pred)
    medae= median_absolute_error(var.y,pred)
    r2= model.score(var.X, var.y)

    final[num_model] = {
        "Modèle" : str(model),
        "Root Mean Squared Error" : rmse,
        "Mean Absolute Error": mae,
        "Median Absolute Error": medae,
        "precision": r2}

    num_model+= 1

res1 = pd.DataFrame.from_dict(final, orient="index").round(3)
#print("res1:\n",res1)
#print("final", final)
# Évaluation des models (le r2)
print(f"R2 du modèle SVR: {100 * var.clf_svr.score(var.X, var.y)} % .")
print(f"R2 du modèle régression linéaire: {100 * var.clf_reg.score(var.X, var.y)} % .")

fig_heatmap = go.Figure(data=go.Heatmap(
                            z= var.X.corr(), x= var.X.columns, y= var.X.columns, 
                            colorscale = [[0, "#FF0000"], [0.5, "#0000FF"], [1, "#FFFF00"]]),
                        layout = {
                            'title': {'text': "Matrice de corrélation"},
                            'xaxis': {'title': "Caractéristiques étudiées"},
                            'yaxis': {'title': "Caractéristiques étudiées"}
    })

# On prépare l'affichage de dbc.Tabs 
tab1_content2 = dbc.Row([html.H4(children='Comparaison des algorithmes', className="mt-4"),

            dash_table.DataTable(id='container-button-timestamp',
            data=res1.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in res1.columns],
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_table={'overflowX': 'auto',
                         'width' : '1200px',
                         'margin-bot': '100px'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white',
                'textAlign':'left',
                'padding-left':'5px'
                },
            css=[ {'selector': '.row', 'rule': 'margin: 0'}]
            ),
            html.H6(children="Les différentes méthodes de calcul d'erreur sont listées ici. À noter qu'il n'y a "+\
                "pas eu de jeu de test et jeux d'entrainement et donc que les résultat ont été obtenu sur "+\
                "l'intégralité du jeu de donnée.", className="mt-4"),
            ])

# Affichage de la page
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Régression linéaire et SVR'), className="text-center")
        ]),
        dbc.Row([
            dbc.Col(html.P(children="Nous utiliserons la régression linéaire et l'algorithme de SVR pour prédire "+\
                "le prix d'un véhicule en fonction de l'année, du prix d'achat, du nombre de kilométre, de la "+\
                "motorisation ainsi que du mode de transmission."), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H4(children="Étude de la matrice de corrélation"), className="text-center")
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure= fig_heatmap),
                ], className="text-center"),
        ]),
        dbc.Row([
            dbc.Col(html.H4(children="Comparatif des algorithmes"), className="text-center")
        ]),

        dbc.Row([
            dbc.Tabs([
                dbc.Tab(tab1_content2, label="Algorithme",label_style={"color":"#810303"}),
                ],),   
        ], className="mb-4"),
        

        dbc.Row([
            dbc.Col([
                html.A("Obtenir le code depuis mon repository github", href="https://github.com/jpphi/brief1"),
            ])
        ])
    ])
])