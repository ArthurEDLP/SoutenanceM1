from dash import Dash, dcc, html, Output, Input
from page_accueil import accueil_layout
from page_donnees import donnees_layout, register_callbacks
import dash_bootstrap_components as dbc

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/donnees':
        return donnees_layout
    return accueil_layout

# Enregistre les callbacks ici 
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)



