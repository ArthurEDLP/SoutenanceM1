from dash import html, dcc
import dash_bootstrap_components as dbc

accueil_layout = html.Div([
    html.H1("Bienvenue sur le Tableau de Bord", style={
        "textAlign": "center",
        "marginTop": "60px",
        "color": "white",
        "fontSize": "48px",
        "fontWeight": "bold"
    }),

    html.P("Ce tableau de bord présente les données ayant servi à faire ce mémoire.",
           style={
               "textAlign": "center",
               "margin": "30px auto",
               "color": "white",
               "fontSize": "20px",
               "width": "70%"
           }),

    html.Div([
        dcc.Link(
    dbc.Button("Accéder aux données", color="light", size="lg", className="bouton-hover-shadow"),
    href="/donnees"
),

    html.Img(
    src="/assets/logo.png",
    style={
        "position": "fixed",         # image fixe dans la fenêtre
        "bottom": "20px",            # distance depuis le bas
        "left": "20px",              # distance depuis la gauche
        "width": "400px",            # ou hauteur, selon le cas
        "zIndex": "10"               # s’assurer qu’elle est visible
    }
)
    ], style={"textAlign": "center", "marginTop": "30px"}),

    html.Div([
    html.P("Soutenance du mémoire:  Modélisation, prévisions et analyse de l'évolution des catastrophes naturelles", style={
        "margin": "0",
        "color": "white",
        "fontSize": "24px"
    }),
    html.P("Développé Arthur Ernoul de la Provôté M1 ECAP", style={
        "margin": "0",
        "color": "white",
        "fontSize": "24px"
    })
], style={
    "position": "fixed",
    "bottom": "100px",     # distance depuis le bas
    "right": "20px",      # distance depuis la droite
    "textAlign": "right",
    "zIndex": "10"
})


], style={
    "backgroundImage": "url('/assets/fond_accueil.png')",   #  le fichier .png
    "backgroundSize": "cover",
    "backgroundPosition": "center",
    "height": "100vh",
    "padding": "50px",
    "backgroundRepeat": "no-repeat",
    "backgroundColor": "rgba(0, 0, 0, 0.4)",
    "backgroundBlendMode": "darken"
})
