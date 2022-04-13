# hello_psg.py

import PySimpleGUI as sg
import webbrowser
import requests
from oauthlib.oauth2 import BackendApplicationClient

client_id = 'client-credentials-mock-client'
client_secret = 'client-credentials-mock-client-secret'
base_url = 'http://localhost:4011/connect'
redirect_uri = 'http://localhost:3000/auth/oidc'

client = BackendApplicationClient(client_id)

description_text = """This is a demo app for showing how MSQ-Kaiku 
authentication & authorization could be implemented with OAuth2.
"""

layout = [
    [sg.Text(description_text)],
    [sg.Text("Kaiku URL"), sg.InputText('http://localhost:4011', key='-KAIKU_URL-')],
    [sg.Text("client_id"), sg.InputText('client-credentials-mock-client', key='-CLIENT_ID-')],
    [sg.Text("client_secret"), sg.InputText('client-credentials-mock-client-secret', key='-CLIENT_SECRET-')],
    [sg.Button("Connect to Kaiku")],
    [sg.Text("--- Auth creds ---")],
    [sg.Text("Expires in:    "), sg.Text("", key='-EXPIRES_IN-')],
    [sg.Text("Token type:    "), sg.Text("", key='-TOKEN_TYPE-')],
    [sg.Text("Access token:  "), sg.Text("", key='-ACCESS_TOKEN-')],
    [sg.Button("Refresh")],

    
]

# Create the window
window = sg.Window("MSQ-Kokko OAuth2 demo", layout, font=('Helvetica', 15))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == 'Connect to Kaiku':
        url = f'{base_url}/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # Create a URL to which client (user) browser should be redirected to
        dada = client.prepare_request_body(scope=['some-app-scope-1'], # offline_access provides refresh token
                                        include_client_id=True,
                                        client_secret=client_secret
                                        )
        r = requests.post(url, headers=headers, data=dada)
        r_json = r.json()
        window['-EXPIRES_IN-'].update(r_json['expires_in'])
        window['-TOKEN_TYPE-'].update(r_json['token_type'])
        window['-ACCESS_TOKEN-'].update(r_json['access_token'][-40:] + "...")
    if event == sg.WIN_CLOSED:
        break

window.close()