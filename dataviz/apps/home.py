#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 15:41:31 2021

@author: jpphi
"""

import dash_html_components as html
import dash_bootstrap_components as dbc

import  pandas as pd
import numpy as np

from apps import var

# Chargement du fichier de donnée et création du dataframe
var.dataframe = pd.read_csv('../carData.csv')

an_mini= var.dataframe.Year.min()
an_maxi= var.dataframe.Year.max()
plage= np.arange(an_mini,an_maxi+1)

var.X= var.dataframe.loc[:,['Year', 'Kms_Driven', "Present_Price", "Fuel_Type", "Transmission"]]
var.X["Fuel_Type"].replace(['Petrol', 'Diesel', 'CNG'], [0,1,2], inplace= True)
var.X["Transmission"].replace(['Manual', 'Automatic'], [0,1], inplace= True)

var.y= var.dataframe['Selling_Price'].values

layout = html.Div([

    dbc.Container([

        dbc.Row([
            dbc.Col(html.H1("Estimation du prix d'une voiture.", className="text-center")
                    , className="mb-5 mt-5")
        ]),

        dbc.Row([
            dbc.Col(html.Img(src="/assets/sunset-3536574_640.jpg", height="300px")
                    , className="mb-5 text-center")
            ]),

        dbc.Row([
            dbc.Col(html.H5("Cette application correspond au 1er brief du cycle d'apprentissage développement data "+\
                "IA Simplon. Il se compose de 4 pages. La récupération des données se fera depuis le fichier 'carData.csv'."
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5("1. La première page est cette même page ! La page 'home'")          
                    , className="mb-3 text-left")
        ]),

        dbc.Row([
            dbc.Col(html.H5("2. La seconde page permet la visualisation des données de la table sous forme de "+\
                "tableau mais aussi sous forme graphique.")          
                    , className="mb-3 text-left")
        ]),

        dbc.Row([
            dbc.Col(html.H5("3. La page 3 donne les caractéristiques des algorithmes utilisés (régression linéaire et "+\
                "SVR).")          
                    , className="mb-3 text-left")
        ]),

        dbc.Row([
            dbc.Col(html.H5("4. La dernière page permet de réaliser des prédiction en fonction des différents "+\
                "paramètres de la voitures (année, kilométrage,...).")          
                    , className="mb-3 text-left")
        ]),

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    html.H3('Visualisation des données', className="text-center"),
                    dbc.Button("Data-Viz", href="/page1",color="primary", className="mt-3")],
                    body=True, color="dark", outline=True), width=4, className="mb-4"),
            dbc.Col(
                dbc.Card([
                    html.H3('Matrice de confusion et erreur', className="text-center"),
                    dbc.Button("Algorithme", href="/page2", color="primary", className="mt-3")],
                    body=True, color="dark", outline=True), width=4, className="mb-4"),
            dbc.Col(
                dbc.Card([
                    html.H3("Prédire le prix d'une voiture",className="text-center"),
                    dbc.Button("Prédiction", href="page3", color="primary", className="mt-3")],
                    body=True, color="dark", outline=True), width=4, className="mb-4")], className="mb-5"),
        
        html.A("Obtenir le code depuis mon repository github", href="https://github.com/jpphi/brief1")], className="text-center")

])