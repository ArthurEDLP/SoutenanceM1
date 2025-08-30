from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# si ça marche pas # pip install plotly==5.13.1
# 
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Chargement des données
df = pd.read_csv("Base_fusionnee_nouvelles_bases.csv")
df["geo"] = df["geo"].str.upper()

df_fil = pd.read_excel("catastrophes_filtrees.xlsx")

df_po = pd.read_csv("Population_par_pays_uniquement.csv")

df_po['Pays'] = df_po['Pays'].replace('United States', 'United States of America')

df_co2 = pd.read_csv("CO2.csv")

df_co2 = df_co2.rename(columns={
    "Annual greenhouse gas emissions in CO₂ equivalents": "CO2"
})

df_co2['Entity'] = df_co2['Entity'].replace('United States', 'United States of America')

df_temp = pd.read_excel("Base_moyenne_annuelle.xlsx")
df_temp = df_temp.dropna()
df_temp['Country'] = df_temp['Country'].replace('US', 'United States of America')


# Dropdown options
# Définition des options de sélection
catastrophes_options = [
    {'label': 'Toutes les catastrophes', 'value': 'Catastrophes_totales'},
    {'label': 'Vague de froid', 'value': 'Cold wave'},
    {'label': 'Avalanche', 'value': 'Avalanche (wet)'},
    {'label': 'Inondation', 'value': 'Flood (General)'},
    {'label': 'Canicule', 'value': 'Heat wave'},
    {'label': 'Glissement de terrain', 'value': 'Landslide (wet)'},
    {'label': 'Tempête', 'value': 'Storm (General)'},
    {'label': 'Tornade', 'value': 'Tornado'},
    {'label': 'Crue soudaine', 'value': 'Flash flood'},
    {'label': 'Blizzard/tempête hivernale', 'value': 'Blizzard/winter storm'},
    {'label': 'Cyclone tropical', 'value': 'Tropical cyclone'},
    {'label': 'Feu de forêt', 'value': 'Forest fire'},
    {'label': 'Phénomènes météorologiques extrêmes', 'value': 'Severe weather'},
    {'label': 'Grêle', 'value': 'Hail'}
]

cata_label_map = {
    'Catastrophes_totales': 'toutes les catastrophes',
    'Cold wave': 'la catastrophe vague de froid', 
    'Avalanche (wet)': 'la catastrophe avalanche',
    'Flood (General)': 'la catastrophe inondation',
    'Heat wave': 'la catastrophe canicule',
    'Landslide (wet)': 'la catastrophe glissement de terrain',
    'Storm (General)': 'la catastrophe tempête',
    'Tornado': 'la catastrophe tornade',
    'Flash flood': 'la catastrophe crue soudaine',
    'Blizzard/winter storm': 'la catastrophe  blizzard/tempête hivernale',
    'Tropical cyclone': 'la catastrophe  cyclone tropical',
    'Forest fire': 'la catastrophe feu de forêt',
    'Severe weather': 'la catastrophe phénomènes météorologiques extrêmes',
    'Hail': 'la catastrophe grêle'
}


pays_options = [
    {'label': 'Tous les pays', 'value': 'Tous les pays'},
    {'label': 'France', 'value': 'France'},
    {'label': 'USA', 'value': 'United States of America'},
    {'label': 'Chine', 'value': 'China'},
    {'label': 'Indonesie', 'value': 'Indonesia'},
    {'label': 'Japon', 'value': 'Japan'},
    {'label': 'Inde', 'value': 'India'}
    ]

pays_label_map = {
    'Tous les pays': 'dans le monde',
    'France': 'en France',
    'United States of America': 'aux États-Unis',
    'China': 'en Chine',
    'Indonesia': 'en Indonesie',
    'Japan': 'au Japon',
    'India': 'en Inde'
}

format_options = [
    {'label': 'Annuel', 'value': 'Annuel'},
    {'label': 'Mensuel', 'value': 'Mensuel'}
]

btn_style = {
    "backgroundColor": "rgb(255, 183, 178)",
    "borderColor": "rgb(255, 183, 178)",
    "color": "black",
    "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",
    "fontWeight": "bold"
}



# Layout des données
donnees_layout = dbc.Container([

    # Bouton retour
    html.Div([
        dcc.Link(
            dbc.Button("Retour à l'accueil", color="primary", size="md", className="bouton-hover-shadow"),
            href="/"
        )
    ], style={"textAlign": "left", "marginBottom": "20px"}),

    

    # Titre + dropdown + bouton
    dbc.Row([
        dbc.Col(html.H3("Soutenance mémoire", className="text-left", style={
            "fontSize": "30px", "color": "rgb(255, 183, 178)", "fontWeight": "bold"}), md=6,
            style={"height": "9vh", "display": "flex", "alignItems": "center", 
                   "justifyContent": "flex-start", "backgroundColor": "rgb(52, 73, 94)", "paddingLeft": "15px"}),

        dbc.Col([
            dcc.Dropdown(id="pays", options=pays_options, value="Tous les pays", placeholder="Choisissez un pays",
                         style={"fontSize": "16px", "height": "40px", "width": "100%", "borderRadius": "50px",
                                "backgroundColor": "rgb(255, 183, 178)", "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.2)"}),

            dcc.Dropdown(id="cata", options=catastrophes_options, value="Catastrophes_totales", placeholder="Choisissez une catastrophe",
                         style={"fontSize": "16px", "height": "40px", "width": "100%", "borderRadius": "50px",
                                "backgroundColor": "rgb(255, 183, 178)", "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.2)"}),

            html.Div([
                html.Div("Choisissez le format :", style={"color": "white", "marginBottom": "5px"}),
                dbc.ButtonGroup([
                    dbc.Button("Annuel", id="btn-annuel", n_clicks=0, style=btn_style),
                    dbc.Button("Mensuel", id="btn-mensuel", n_clicks=0, style=btn_style)
    ])
], style={"marginTop": "10px"}),
            # Stockage de l'état du format sélectionné
            dcc.Store(id="format-store", data="Annuel")


        ], md=6, style={"height": "9vh", "display": "flex", "alignItems": "center", "backgroundColor": "rgb(52, 73, 94)"}),
    ], style={"marginBottom": "10px"}),


    # Graphique principal (catastrophes totales divisé par PAYS et catastrophes)
    dbc.Row([
        dbc.Col(dcc.Graph(id='catastrophes_tot'), style={
            "min-height": "100px",
            "textAlign": "center",
            "border": "10px solid rgb(52, 73, 94)",
            "borderRadius": "10px",
            "margin": "10px 10px",
            "margin": "auto",
            "padding": "0"
        }, md=8)
    ]),

    # Graphiques secondaire (catastrophes totales divisé par PAYS ou catastrophes)
    dbc.Row([
        dbc.Col(dcc.Graph(id='catastrophes_pays'), 
            style={
            "width": "45%",
            "min-height": "100px",
            "textAlign": "center",
            "border": "10px solid rgb(52, 73, 94)",
            "borderRadius": "10px",
            "margin": "5px 10px",
            "padding": "0"
        } ),

        dbc.Col(dcc.Graph(id='catastrophes_types'),
            style={
            "width": "45%",
            "min-height": "100px",
            "textAlign": "center",
            "border": "10px solid rgb(52, 73, 94)",
            "borderRadius": "10px",
            "margin": "5px 10px",
            "marginLeft": "auto",
            "padding": "0"
        })

    ], justify="between"),


    dbc.Row([

        dbc.Col(
    html.H3("Population", className="text-center", style={
        "fontSize": "30px", 
        "color": "rgb(255, 183, 178)", 
        "fontWeight": "bold"
    }), 
    md=12,
    style={
        "height": "7vh", 
        "display": "flex", 
        "alignItems": "center", 
        "justifyContent": "center", 
        "backgroundColor": "rgb(52, 73, 94)"
    }
)


    ]),

    # Ligne divisée en 2 colonnes
    dbc.Row([

        # Colonne gauche avec deux graphiques empilés
        dbc.Col([
            dcc.Graph(id='evo_pop', style={
                "min-height": "295px",
                "border": "5px solid rgb(52, 73, 94)",
                "borderRadius": "10px",
                "margin": "10px 0px",
                "marginBottom": "10px",
                "padding": "0"
            }),

            dcc.Graph(id='evo_pop_pourcent', style={
                "min-height": "295px",
                "border": "5px solid rgb(52, 73, 94)",
                "borderRadius": "10px",
                "padding": "0"
            })
        ], md=6),

        # Colonne droite avec la carte
        dbc.Col(
            dcc.Graph(id='map_pop', style={
                "min-height": "620px",
                "border": "5px solid rgb(52, 73, 94)",
                "borderRadius": "10px",
                "margin": "10px 0px",
                "padding": "0"
            }),
            md=6
        )

    ]),

    # graphique CO2

    dbc.Row([

        dbc.Col(
            html.H3("CO2", className="text-center", style={
            "fontSize": "30px", 
            "color": "rgb(255, 183, 178)", 
            "fontWeight": "bold"
                    }), 
        md=12,
            style={
            "height": "7vh", 
            "display": "flex", 
            "alignItems": "center", 
            "justifyContent": "center", 
            "backgroundColor": "rgb(52, 73, 94)"
        }
        )


    ]),

    dbc.Row([

        # Colonne gauche avec la carte

        dbc.Col(
            dcc.Graph(id='map_co2', style={
                "min-height": "620px",
                "border": "5px solid rgb(52, 73, 94)",
                "borderRadius": "10px",
                "margin": "10px 0px",
                "padding": "0"
            }),
            md=6),

        # Colonne droite avec deux graphiques empilés
        dbc.Col([
            dcc.Graph(id='evo_co2', style={
                "min-height": "295px",
                "border": "5px solid rgb(52, 73, 94)",
                "borderRadius": "10px",
                "margin": "10px 0px",
                "marginBottom": "10px",
                "padding": "0"
            }),

            dcc.Graph(id='evo_co2_pourcent', style={
                "min-height": "295px",
                "border": "5px solid rgb(52, 73, 94)",
                "borderRadius": "10px",
                "padding": "0"
            })
        ], md=6)

        
        

    ]),

    # Graphique de température

    dbc.Row([

        dbc.Col(
            html.H3("Température", className="text-center", style={
            "fontSize": "30px", 
            "color": "rgb(255, 183, 178)", 
            "fontWeight": "bold"
                    }), 
        md=12,
            style={
            "height": "7vh", 
            "display": "flex", 
            "alignItems": "center", 
            "justifyContent": "center", 
            "backgroundColor": "rgb(52, 73, 94)"
        }
        )


    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='evo_temp'), 
            style={
            "width": "45%",
            "min-height": "100px",
            "textAlign": "center",
            "border": "10px solid rgb(52, 73, 94)",
            "borderRadius": "10px",
            "margin": "5px 10px",
            "padding": "0"
        } ),

        dbc.Col(dcc.Graph(id='temp_graph'),
            style={
            "width": "45%",
            "min-height": "300px",
            "textAlign": "center",
            "border": "10px solid rgb(52, 73, 94)",
            "borderRadius": "10px",
            "margin": "5px 10px",
            "marginLeft": "auto",
            "padding": "0"
        })

    ], justify="between"),

    

], style={"backgroundColor": "#aaaaaa"}, fluid=True)


# Fonction d'enregistrement des callbacks
def register_callbacks(app):

    # Callback pour gérer le bouton cliquable : annuel ou mensuel
    @app.callback(
        Output("format-store", "data"),
        [Input("btn-annuel", "n_clicks"),
        Input("btn-mensuel", "n_clicks")]
)
    def update_format(n_annuel, n_mensuel):
        if n_mensuel > n_annuel:
            return "Mensuel"
        return "Annuel"



    # Callback principal qui réagit au pays, catastrophe et format sélectionné
    @app.callback(
        [Output('catastrophes_tot', 'figure'),
        Output('map_pop', 'figure'),
        Output('evo_pop', 'figure'),
        Output('catastrophes_types', 'figure'),
        Output('catastrophes_pays', 'figure'),
        Output('evo_pop_pourcent', 'figure'),
        Output('map_co2', 'figure'),
        Output('evo_co2', 'figure'),
        Output('evo_co2_pourcent', 'figure'),
        Output('evo_temp', 'figure'),
        Output('temp_graph', 'figure')],
        [Input('pays', 'value'),
        Input('cata', 'value'),
        Input('format-store', 'data')]
    )
    def update_graphs(selected_pays, selected_cata, selected_format):
        # Filtrage des données en fonction du pays sélectionné
        if selected_pays == "Tous les pays":

            if selected_cata == "Catastrophes_totales":
                df_filtered_cata = df
            else:
                df_filtered_cata = df[["Pays", "Année", "Population", selected_cata]]

        else:
            df_filtered = df[df["Pays"] == selected_pays]

            if selected_cata == "Catastrophes_totales":
                df_filtered_cata = df_filtered
            else:
                df_filtered_cata = df_filtered[["Pays", "Année", "Population", selected_cata]]

        df_cata_tout_pays = df[["Pays", "Année", "Population", selected_cata]]
        df_cata_tout_pays = df_cata_tout_pays.groupby("Année", as_index=False)[selected_cata].sum()


        if selected_pays == "Tous les pays":
            df_tout_cata_pays = df[["Année", "Catastrophes_totales"]]
            df_tout_cata_pays = df_tout_cata_pays.groupby("Année", as_index=False).sum()
        else:
            df_deux = df[df["Pays"] == selected_pays]
            df_tout_cata_pays = df_deux[["Année", "Catastrophes_totales"]]


        tot_cata = df_filtered_cata.groupby("Année", as_index=False)[selected_cata].sum()


        if selected_pays == "Tous les pays":
            tot_pop = df_po
        else:
            tot_pop = df_po[df_po["Pays"] == selected_pays]

        tot_pop = tot_pop.groupby("Année", as_index=False)["Population"].sum()

        tot_pop["diff"] = (tot_pop["Population"].pct_change()) * 100


        ## ---------------------CO2------------------------------------------ ##

        if selected_pays == "Tous les pays":
            tot_CO2 = df_co2
        else:
            tot_CO2 = df_co2[df_co2["Entity"] == selected_pays]

        tot_CO2 = tot_CO2.groupby("Year", as_index=False)["CO2"].sum()

        tot_CO2["diff"] = (tot_CO2["CO2"].pct_change()) * 100

        ## ---------------------Température---------------------------------- ##

        df_erature  = df_temp[df_temp["Year"] !=2020]
 
        if selected_pays == "Tous les pays":
            tot_temp = df_erature
        else:
            tot_temp = df_erature[df_erature["Country"] == selected_pays]

        tot_temp = tot_temp.groupby("Year", as_index=False)["Celsius"].mean()


        tot_temp["diff"] = tot_temp["Celsius"].diff()

        # Définir les couleurs en fonction du signe de la variation
        colors = ["red" if val > 0 else "blue" for val in tot_temp["diff"]]

        ## ---------------------Annuel--------------------------------------- ##

        if selected_cata == "Catastrophes_totales":
            df_flash_cata = df_fil
        else:
            df_flash_cata = df_fil[df_fil["Disaster Subtype"] == selected_cata] 

        ###

        if selected_pays == "Tous les pays":
            df_flash_pays = df_fil
        else:
            df_flash_pays = df_fil[df_fil["Country"] == selected_pays] 

        ###

        if selected_pays == "Tous les pays":

            if selected_cata == "Catastrophes_totales":
                df_flash_cata_pays = df_fil
            else:
                df_flash_cata_pays = df_fil[df_fil["Disaster Subtype"] == selected_cata]
        else:
            df_flash_pays = df_fil[df_fil["Country"] == selected_pays] 

            if selected_cata == "Catastrophes_totales":
                df_flash_cata_pays = df_flash_pays
            else:
                df_flash_cata_pays = df_flash_pays[df_flash_pays["Disaster Subtype"] == selected_cata]

        ## ---------------------Annuel--------------------------------------- ##

        # Comptage des occurrences par année et mois
        df_count = df_flash_cata.groupby(["Start Year", "Start Month"]).size().reset_index(name="Nombre")

        # Limite à l'année 2019 incluse
        years = sorted(df_flash_cata["Start Year"].dropna().unique())
        years = [y for y in years if y < 2020]
        months = range(1, 13)

        # Création de l'ensemble des combinaisons Année x Mois jusqu’à 2019 inclus
        full_index = pd.MultiIndex.from_product([years, months], names=["Start Year", "Start Month"])
        df_full = pd.DataFrame(index=full_index).reset_index()

        # Fusion avec les données comptées
        df_merged_cata = pd.merge(df_full, df_count, how="left", on=["Start Year", "Start Month"])
        df_merged_cata["Nombre"] = df_merged_cata["Nombre"].fillna(0).astype(int)

        # Renommage
        df_merged_cata.rename(columns={"Start Year": "Année", "Start Month": "Mois"}, inplace=True)

        # Tri final
        df_merged_cata = df_merged_cata.sort_values(["Année", "Mois"]).reset_index(drop=True)

        # Conversion des colonnes Année et Mois en Date
        df_merged_cata["Date"] = pd.to_datetime(dict(year=df_merged_cata["Année"], month=df_merged_cata["Mois"], day=1))

        ## ---------------------Annuel--------------------------------------- ##

        # Comptage des occurrences par année et mois
        df_count = df_flash_pays.groupby(["Start Year", "Start Month"]).size().reset_index(name="Nombre")

        # Limite à l'année 2019 incluse
        years = sorted(df_flash_pays["Start Year"].dropna().unique())
        years = [y for y in years if y < 2020]
        months = range(1, 13)

        # Création de l'ensemble des combinaisons Année x Mois jusqu’à 2019 inclus
        full_index = pd.MultiIndex.from_product([years, months], names=["Start Year", "Start Month"])
        df_full = pd.DataFrame(index=full_index).reset_index()

        # Fusion avec les données comptées
        df_merged_pays = pd.merge(df_full, df_count, how="left", on=["Start Year", "Start Month"])
        df_merged_pays["Nombre"] = df_merged_pays["Nombre"].fillna(0).astype(int)

        # Renommage
        df_merged_pays.rename(columns={"Start Year": "Année", "Start Month": "Mois"}, inplace=True)

        # Tri final
        df_merged_pays = df_merged_pays.sort_values(["Année", "Mois"]).reset_index(drop=True)

        # Conversion des colonnes Année et Mois en Date
        df_merged_pays["Date"] = pd.to_datetime(dict(year=df_merged_pays["Année"], month=df_merged_pays["Mois"], day=1))

        ## ---------------------Annuel--------------------------------------- ##

        # Comptage des occurrences par année et mois
        df_count = df_flash_cata_pays.groupby(["Start Year", "Start Month"]).size().reset_index(name="Nombre")

        # Limite à l'année 2019 incluse
        years = sorted(df_flash_cata_pays["Start Year"].dropna().unique())
        years = [y for y in years if y < 2020]
        months = range(1, 13)

        # Création de l'ensemble des combinaisons Année x Mois jusqu’à 2019 inclus
        full_index = pd.MultiIndex.from_product([years, months], names=["Start Year", "Start Month"])
        df_full = pd.DataFrame(index=full_index).reset_index()

        # Fusion avec les données comptées
        df_merged_cata_pays = pd.merge(df_full, df_count, how="left", on=["Start Year", "Start Month"])
        df_merged_cata_pays["Nombre"] = df_merged_cata_pays["Nombre"].fillna(0).astype(int)

        # Renommage
        df_merged_cata_pays.rename(columns={"Start Year": "Année", "Start Month": "Mois"}, inplace=True)

        # Tri final
        df_merged_cata_pays = df_merged_cata_pays.sort_values(["Année", "Mois"]).reset_index(drop=True)

        # Conversion des colonnes Année et Mois en Date
        df_merged_cata_pays["Date"] = pd.to_datetime(dict(year=df_merged_cata_pays["Année"], month=df_merged_cata_pays["Mois"], day=1))

        ## ---------------------Annuel--------------------------------------- ##

        if selected_format == "Annuel":
            # Ajoutez ici le code pour le format annuel, par exemple :
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=tot_cata["Année"], y=tot_cata[selected_cata], mode='lines'))
            fig.update_layout(
                title=f"Évolution annuelle de {cata_label_map[selected_cata]}, {pays_label_map[selected_pays]}",
                xaxis_title="Année",
                yaxis_title="Nombre de catastrophes",
                showlegend=False)

            fig_cata = go.Figure()
            fig_cata.add_trace(go.Scatter(x = df_cata_tout_pays["Année"], y = df_cata_tout_pays[selected_cata], mode='lines'))
            fig_cata.update_layout(
                title=f"Évolution annuelle de {cata_label_map[selected_cata]}, dans le monde",
                xaxis_title="Année",
                yaxis_title="Nombre de catastrophes",
                showlegend=False)
        
            fig_pays = go.Figure()
            fig_pays.add_trace(go.Scatter(x = df_tout_cata_pays["Année"], y = df_tout_cata_pays["Catastrophes_totales"], mode='lines'))
            fig_pays.update_layout(
                title=f"Évolution annuelle des catastrophes {pays_label_map[selected_pays]}",
                xaxis_title="Année",
                yaxis_title="Nombre de catastrophes",
                showlegend=False)

        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_merged_cata_pays["Date"], y=df_merged_cata_pays["Nombre"], mode='lines'))
            fig.update_layout(
                title=f"Évolution de {cata_label_map[selected_cata]}, {pays_label_map[selected_pays]}",
                xaxis_title="Date",
                yaxis_title="Nombre de catastrophes",
                showlegend=False)

            fig_cata = go.Figure()
            fig_cata.add_trace(go.Scatter(x = df_merged_cata["Date"], y = df_merged_cata["Nombre"], mode='lines'))
            fig_cata.update_layout(
                title=f"Évolution de {cata_label_map[selected_cata]}, dans le monde",
                xaxis_title="Date",
                yaxis_title="Nombre de catastrophes",
                showlegend=False)
        
            fig_pays = go.Figure()
            fig_pays.add_trace(go.Scatter(x = df_merged_pays["Date"], y = df_merged_pays["Nombre"], mode='lines'))
            fig_pays.update_layout(
                title=f"Évolution des catastrophes {pays_label_map[selected_pays]}",
                xaxis_title="Date",
                yaxis_title="Nombre de catastrophes",
                showlegend=False)
            

        # Graphique de la population --------------------------------------------#    


        pop_fig = go.Figure()
        pop_fig.add_trace(go.Scatter(x=tot_pop["Année"], y=tot_pop["Population"], mode='lines'))
        pop_fig.update_layout(
            title=f"Évolution de la population {pays_label_map[selected_pays]}",
            showlegend=False)

        fig_map = px.choropleth(df_po,
            locations="ISO",
            color="Population",
            hover_name="Pays",
            animation_frame="Année",
            range_color=[50000, 350000000],
        )
        fig_map.update_layout(
            height=920,
            title="Évolution de la population mondiale par pays",
            geo=dict(showframe=False, showcoastlines=False),
            margin=dict(l=0, r=0, t=50, b=0)  # supprime les marges inutiles
        )

        pop_percent_fig = go.Figure()
        pop_percent_fig.add_trace(go.Scatter(x=tot_pop["Année"], y=tot_pop["diff"], mode='lines'))
        pop_percent_fig.update_layout(
            title=f"Taux de croissance {pays_label_map[selected_pays]} en pourcentage",
            showlegend=False)
        
        # Graphique CO2  ---------------------------------------------------------#

        fig_map_CO2 = px.choropleth(df_co2,
            locations="Code",
            color="CO2",
            hover_name="Entity",
            animation_frame="Year",
            range_color=[690000, 4200000000],
        )
        fig_map_CO2.update_layout(
            height=920,
            title="Évolution des émissions de CO2 mondiale par pays",
            geo=dict(showframe=False, showcoastlines=False),
            margin=dict(l=0, r=0, t=50, b=0)  # supprime les marges inutiles
        )

        CO2_fig = go.Figure()
        CO2_fig.add_trace(go.Bar(
            x=tot_CO2["Year"], 
            y=tot_CO2["CO2"], 
            marker=dict(color="rgb(255, 127, 80)")  # facultatif : couleur orange
        ))
        CO2_fig.update_layout(
            title=f"Évolution du CO2 {pays_label_map[selected_pays]}",
            xaxis_title="Année",
            yaxis_title="Émissions de CO2",
            showlegend=False
        )


        co2_percent_fig = go.Figure()
        co2_percent_fig.add_trace(go.Scatter(x=tot_CO2["Year"], y=tot_CO2["diff"], mode='lines'))
        co2_percent_fig.update_layout(
            title=f"Taux de croissance du CO2 {pays_label_map[selected_pays]} en pourcentage",
            showlegend=False)
        
        ## Graphique de température --------------------------------------------#

        temp_fig = go.Figure()
        temp_fig.add_trace(go.Bar(
            x=tot_temp["Year"],
            y=tot_temp["diff"],
            marker_color=colors,
            name="Variation annuelle"
        ))

        temp_fig.update_layout(
            title=f"Variation annuelle de la température {pays_label_map[selected_pays]} ",
            xaxis_title="Année",
            yaxis_title="Écart de température (°C)",
            showlegend=False,
            height=500
        )
        
        ### Régression linéaire /\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\_/\ ###
        X = tot_temp["Year"].values.reshape(-1, 1)
        y = tot_temp["Celsius"].values
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        # Création du graphique Plotly
        temp = go.Figure()

        # Courbe réelle
        temp.add_trace(go.Scatter(
            x=tot_temp["Year"], y=y,
            mode='lines',
            name="Température réelle",
            line=dict(color='orange')
        ))

        # Courbe de régression
        temp.add_trace(go.Scatter(
            x=tot_temp["Year"], y=y_pred,
            mode='lines',
            name="Régression linéaire",
            line=dict(color='blue', dash='dash')
        ))

        # Layout
        temp.update_layout(
            title=f"Évolution annuelle des températures {pays_label_map[selected_pays]} avec régression",
            xaxis_title="Année",
            yaxis_title="Température moyenne (°C)",
            legend=dict(x=0.02, y=0.98),
            margin=dict(l=40, r=20, t=60, b=40),
            template="plotly_white",
            height=500
        )

        return fig, fig_map, pop_fig, fig_cata, fig_pays, pop_percent_fig, fig_map_CO2, CO2_fig, co2_percent_fig, temp_fig, temp
