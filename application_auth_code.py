# hello_psg.py

import PySimpleGUI as sg
import webbrowser
import requests
from oauthlib.oauth2 import WebApplicationClient


# Define a really simple HTTP server with a handler that is only interested of the request path
import http.server
REQUEST_PATH = ""
HOST = "localhost"
PORT = 8002
class MyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """Response to a request with HTTP 200, and store the request path to global variable
        """
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Connection success!")
        global REQUEST_PATH
        REQUEST_PATH = self.path

def run_blocking_http_server(server_class=http.server.HTTPServer, handler_class=MyHandler):
    """HTTP server that blocks until one request is received, and then shuts down.
    """
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    httpd.handle_request()

# Mock identityserver info
client_id = 'client-credentials-mock-client'
client_secret = 'client-credentials-mock-client-secret'
base_url = 'http://localhost:4011/connect'
redirect_uri = 'http://localhost:8002/auth/oidc'

# Create OAuth2 client
client = WebApplicationClient(client_id)
print(client)
code_verifier = client.create_code_verifier(50)

description_text = """This is a demo app for showing how System-to-System 
authentication & authorization could be implemented with OAuth2.

This application could be any desktop application running on a server.
Instructions:

1. Click the "Connect to Kaiku" button to start the authorization process
(Note: this application will freeze until login is done, see below*)
2. A IdentityServe4 login page is opened in browser. The credentials are
User: User1
password: pwd
3. After clicking "Login", the browser is redirected to a localhost server
(this application). Based on the URL information, access token and refresh
token are fetched from the IdentityServer and shown the user below.
4. Click refresh button to refresh the access and refresh tokens.
5. Press Connect to Kaiku again, the user is already logged in and simply
redirected back to this application. Go to http://localhost:3000 in browser
to logout to reset the demo.

Requests to secured resource could now be made by adding the access token
to each requests header 'Authorization: Bearer <access token>'

*A blocking HTTP server on port 8002 is started when auth flow is starter.
If there's a problem in the login, then to unfreeze this 
application just go to http://localhost:8002 or CTRL+C in terminal.
"""

layout = [
    [sg.Text(description_text)],
    [sg.Text("Kaiku URL")],
    [sg.InputText('http://localhost:4011', key='-KAIKU_URL-')],
    [sg.Button("Connect to Kaiku")],
    [sg.Text("--- Auth creds ---")],
    [sg.Text("Refresh token: "), sg.Text("", key='-REFRESH_TOKEN-')],
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
        # When "Connect to Kaiku" button is pressed, then redirect the user (open a browser) to the IdentityServer
        # which then asks for the credentials.
        # After redirection, start a HTTP server locally which waits for the IdentitySErver to redirect the user
        # back to our application
        code_challenge = client.create_code_challenge(code_verifier, code_challenge_method='S256')
        uri = client.prepare_request_uri(f'{base_url}/authorize',
                                        redirect_uri=redirect_uri,
                                        scope=['some-app-scope-1', 'offline_access'],
                                        code_challenge=code_challenge,
                                        code_challenge_method='S256'
                                        )
        webbrowser.open(uri)

        run_blocking_http_server()
        # HTTP server sets the request path to a global variable, read it from there
        # then parse the request URL for all the necessary information
        response_uri = f"http://{HOST}:{PORT}{REQUEST_PATH}"
        token_request = client.prepare_token_request(f'{base_url}/token', authorization_response=response_uri, redirect_url=redirect_uri, code_verifier=code_verifier, client_secret=client_secret)
        url, headers, dada = token_request
        
        # Get the access and refresh token from identityserver
        r = requests.post(url, headers=headers, data=dada)
        r_json = r.json()
        window['-REFRESH_TOKEN-'].update(r_json['refresh_token'])
        window['-EXPIRES_IN-'].update(r_json['expires_in'])
        window['-TOKEN_TYPE-'].update(r_json['token_type'])
        window['-ACCESS_TOKEN-'].update(r_json['access_token'][-40:] + "...")
    if event == 'Refresh':
        # Use the refresh token to get a new access token (and refresh token)
        refresh_token_request = client.prepare_refresh_token_request(f'{base_url}/token', refresh_token=r_json['refresh_token'], client_id=client_id, scope=['some-app-scope-1'], client_secret=client_secret)
        url, headers, dada = refresh_token_request
        r = requests.post(url, headers=headers, data=dada)
        r_json = r.json()
        window['-REFRESH_TOKEN-'].update(r_json['refresh_token'])
        window['-EXPIRES_IN-'].update(r_json['expires_in'])
        window['-TOKEN_TYPE-'].update(r_json['token_type'])
        window['-ACCESS_TOKEN-'].update(r_json['access_token'][-40:] + "...")
    if event == sg.WIN_CLOSED:
        break

window.close()