#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 15:42:11 2021

@author: jpphi
"""

import plotly.graph_objects as go
import pandas as pd
import dash_table

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np

from apps import var

# Figure 1: Nombre de voiture disponible en fonction de leur ancienneté
# Préparation des données
kms= pd.concat([var.dataframe['Year'], var.dataframe['Kms_Driven']], axis= 1)
kms_moyen= kms.groupby("Year").mean()
fig1 = go.Figure(
    data= go.Histogram(x=var.dataframe.Year, xbins=dict(), marker=dict(color='#810303')),
    layout = go.Layout(title="Nombre de voiture en fonction de l'année.") )

# Figure 2: Relation kilométrage ancienneté.
fig2 = go.Figure(
    data= go.Bar( x= var.plage, y= kms_moyen.Kms_Driven, marker= dict(color='#11337E')),
    layout = go.Layout(title="Kilométres parcourus moyens en fonction de l'année.") )

# Figure 3: Répartition  des voiture en fonction de leur motorisation
motorisation= var.dataframe.groupby("Fuel_Type").count()
fig3 = go.Figure(
    data= go.Pie(labels=motorisation.index,
              values=motorisation.Selling_Price, # On peut utiliser n'importe quel colonne du dataframe
              textinfo='label+percent'),
    layout = go.Layout(title= 'Nombre de véhicules disponibles par motorisation.', font_color= 'black') )

# Figure 4: Prix en fonction de l'année ainsi que leur motorisation
#  (j'utilise ici une autre façon de construire la vue par rapport au autre fig)
fig4 = px.scatter(data_frame= var.dataframe, x= "Year", y= "Selling_Price", color= "Fuel_Type")
fig4.update_layout(title="Les différentes motorisations.")

"""
# LES [] DANS data= DOIVENT PERMETTRE DE PASSER PLUSIEURS GRAPHIQUES ???????
couleur= var.dataframe.Fuel_Type.replace(['Petrol', 'Diesel', 'CNG'], [0,1,2])
fig4a = go.Figure(data=[go.Scatter(x= var.dataframe.Year, y= var.dataframe.Selling_Price, mode='markers',
                        labels= var.dataframe.Fuel_Type.unique(),
                        marker=dict(
                                    size= 5,
                                    color= couleur,
                                    colorscale= 'Viridis', # one of plotly colorscales
                                    #showscale=True
                                ))],

                    layout= {'title':"Les différentes motorisations."})
"""

# Tableau
tableau= dash_table.DataTable(id='tableau-carData',
            data= var.dataframe.to_dict('records'), # 'record' fait que chaque ligne du dataframe correspond à une ligne du tableau
            columns=[{'id': col, 'name': col} for col in var.dataframe.columns],
            export_format='csv',
            style_header={'backgroundColor': 'rgb(4, 8, 32)'}, # Bleu profond
            style_table={'overflowX': 'auto',
                         'width' : '1200px',
                         'height': '400px'},
            style_cell={
                'backgroundColor': 'rgb(20, 30, 100)',
                'color': 'white',
                'textAlign':'center' #,'padding-left':'15px' On passe à un alignement centré sans padding
                }
            )

# Construction de la page

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1('Visualisation des données.'))
        ]),
        dbc.Row([
            dbc.Col(html.H4('Chargement et visualisation du fichier carData contenant les données.'))
        ]),
        dbc.Row([
            dbc.Tabs([
                dbc.Tab(tableau, label="carData",label_style={"color":"#0000FF"})
            ]),
        ]),
        dbc.Row([
            dbc.Col(html.H1('Graphiques'))
        ]),
        dbc.Row([
            dbc.Col(
                html.H4("Voitures disponibles à la vente en fonction de l'ancienneté et du kilométrage moyen."))
        ]), 
        dbc.Row([
                dbc.Col(dcc.Graph(id='graph-1',figure=fig1)),
                dbc.Col(dcc.Graph(id='graph-2',figure=fig2)),
        ]),
        dbc.Row([
                dbc.Col(
                    html.P("La majorité des voitures représentées dans ce dataset sont relativement récente. "+\
                    "Le kilométrage moyen en fonction des années est une courbe dont la forme est quelque peu "+\
                    "surprenante au premier abord. On peut cependant penser que les voitures les plus anciennes "+\
                    "qui sont encore sur le marché étaient des voitures peu utilisées et donc avec un faible kilométrage. "+\
                    "Par la suite, plus les voitures sont récentes et moins elles ont de kilométres, ce qui est "+\
                    "cohérent, avec une autre anomalie pour l'année 2008."))
        ]),
        dbc.Row([
                dbc.Col(html.H4('Étude de la motorisation des véhicules.'))
        ]),
        dbc.Row([
                dbc.Col(dcc.Graph(id='graph-3',figure=fig3)),
                dbc.Col(dcc.Graph(id='graph-4',figure=fig4)),
        ]),
        dbc.Row([
                dbc.Col(
                    html.P("3 motorisations sont disponibles. La trés grande majorité sont de voiture "+\
                    "essence. La motorisation CNG ne concerne que 2 véhicules. On notera que le voitures diésel "+\
                    "sont plus chère que les voitures essences.")),
        ]), 
        html.A("Obtenir le code depuis mon repository github", href="https://github.com/jpphi/brief1")
    ]), 
])