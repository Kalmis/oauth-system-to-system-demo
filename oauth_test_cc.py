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
code_verifier = client.create_code_verifier(50)
code_challenge = client.create_code_challenge(code_verifier, code_challenge_method='S256')

url = f'{base_url}/token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
# Create a URL to which client (user) browser should be redirected to
dada = client.prepare_request_body(scope=['some-app-scope-1'], # offline_access provides refresh token
                                 include_client_id=True,
                                 code_challenge=code_challenge,
                                 code_challenge_method='S256',
                                 client_secret=client_secret
                                 )
print(dada)
r = requests.post(url, headers=headers, data=dada)
r_json = r.json()
print(r_json)

print(f'Access token: {r_json["access_token"]}')
print(f'Refresh token: {r_json["refresh_token"]}')


print ("------------")

# Refresh the access token
# Note: Refresh token is also regenerated
refresh_token_request = client.prepare_refresh_token_request(f'{base_url}/token', refresh_token="8B287C4A50D3C95ACFA4CFE83B71CAC23A1102476E4F5314D9B28D9FC1BC27B7", client_id=client_id, scope=['some-app-scope-1'], client_secret=client_secret)
url, headers, dada = refresh_token_request
r = requests.post(url, headers=headers, data=dada)
r_json = r.json()

print(f'Access token: {r_json["access_token"]}')
print(f'Refresh token: {r_json["refresh_token"]}')