#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 15:44:01 2021

@author: jpphi
"""

#import pandas as pd
import numpy as np

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from sklearn.pipeline import Pipeline
#from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier

#import nltk
from app import app

# ---------------------------------------------------
# - Code -

# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import RobustScaler, LabelEncoder, StandardScaler, MinMaxScaler
# from sklearn.svm import SVR
# from sklearn.pipeline import make_pipeline

from apps import var

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Prédiction du prix d'un véhicule"), className="mb-4 text-center")
        ]),
        dbc.Row([
            dbc.Col(html.H6('Tout les paramètres sont obligatoire pour une bonne prédiction.'),
                className="mb-4 text-center")
        ]),
        dbc.Row([
            dbc.Col([
                html.H6('Kilométrage'),
                dcc.Input(id="kilometrage", type="number", placeholder="Type your text", debounce=True, 
                className="mb-4 text-center", value= 10000, min= 0)], className="mb-4 text-center"),
            
            dbc.Col([
                html.H6('Valeur à neuf'),
                dcc.Input(id="neuf", type="number", placeholder="Prix du véhicule neuf", min= 0,
                className="mb-4 text-center", debounce=True, value= 5)], className="mb-4 text-center"),
            dbc.Col([
                html.H6('Année'),
                dcc.Dropdown(id='annee',
                    options=[
                        {'label': '2003', 'value': '2003'},
                        {'label': '2004', 'value': '2004'},
                        {'label': '2005', 'value': '2005'},
                        {'label': '2006', 'value': '2006'},
                        {'label': '2007', 'value': '2007'},
                        {'label': '2008', 'value': '2008'},
                        {'label': '2009', 'value': '2009'},
                        {'label': '2010', 'value': '2010'},
                        {'label': '2011', 'value': '2011'},
                        {'label': '2012', 'value': '2012'},
                        {'label': '2013', 'value': '2013'},
                        {'label': '2014', 'value': '2014'},
                        {'label': '2015', 'value': '2015'},
                        {'label': '2016', 'value': '2016'},
                        {'label': '2017', 'value': '2017'},
                        {'label': '2018', 'value': '2018'}
                    ],
                    value='2010',className="mb-4 text-center", clearable= False)], className="mb-4 text-center"),
            dbc.Col([
                html.H6('Motorisation'),
                dcc.RadioItems(
                    options=[
                        {'label': 'Essence', 'value': 'Petrol'},
                        {'label': 'Diésel', 'value': 'Diesel'},
                        {'label': 'CNG', 'value': 'CNG'}],
                    value='Petrol', id="motorisation", labelStyle={'display': 'block'} )], className= "text-left"),
            dbc.Col([
                html.H6('Transmission'),
                dcc.RadioItems(
                    options=[
                        {'label': 'Manuelle', 'value': 'Manual'},
                        {'label': 'Automatique', 'value': 'Automatic'}],
                    value='Manual', id="bav", labelStyle={'display': 'block'})]),
        ]),
        dbc.Row([
            dbc.Col(html.Div(id="sortie"), className="mb-4 text-center")
        ]),
        html.A("Obtenir le code depuis mon repository github", href="https://github.com/jpphi/brief1"),
    ])
])

@app.callback(
    Output("sortie", "children"),
    Input("kilometrage", "value"),
    Input("neuf", "value"),
    Input("annee", "value"),
    Input("motorisation", "value"),
    Input("bav", "value"),
    )
def update_output(kilometrage, neuf, annee, motorisation, bav):
    mot= 0
    if motorisation== "Diesel":
        mot= 1
    elif motorisation== "CNG":
        mot= 2
    bv= 1
    if bav== "Manual":
        bv= 0

    Xp= np.array([[annee, kilometrage, neuf, mot, bv]])

    estimation_svr= var.clf_svr.predict(Xp)  
    estimation_reg= var.clf_reg.predict(Xp)  

    if var.dataframe is None:
        return "Le dataframe n'est pas chargé !"
    else:
        return [html.P(f"Le prix d'une voiture de {annee}, ayant {kilometrage} km, d'une valeur d'achat de "+\
            f"{neuf}, avec motorisation {motorisation}, et une boite de vitesse {bav} est de: "),
            html.P(f"Par la méthode SVR : {estimation_svr}"),
            html.P(f"Par la méthode de régression Linéaire : {estimation_reg}"),
            ]
