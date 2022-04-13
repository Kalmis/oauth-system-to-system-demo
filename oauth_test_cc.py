import requests
from oauthlib.oauth2 import BackendApplicationClient

# Basic information 
client_id = 'client-credentials-mock-client'
client_secret = 'client-credentials-mock-client-secret'
base_url = 'http://localhost:4011/connect'
redirect_uri = 'http://localhost:3000/auth/oidc'

# Create oauth2 client
client = BackendApplicationClient(client_id)
# Create PKCE code verifier used in the authorization code

url = f'{base_url}/token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
# Create a URL to which client (user) browser should be redirected to
dada = client.prepare_request_body(scope=['some-app-scope-1'], # offline_access provides refresh token
                                 include_client_id=True,
                                 client_secret=client_secret
                                 )
print(dada)
r = requests.post(url, headers=headers, data=dada)
r_json = r.json()
print(r_json)

print(f'Access token: {r_json["access_token"]}')
