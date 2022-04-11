import requests
from oauthlib.oauth2 import WebApplicationClient

# Basic information 
client_id = 'client-credentials-mock-client'
client_secret = 'client-credentials-mock-client-secret'
base_url = 'http://localhost:4011/connect'
redirect_uri = 'http://localhost:3000/auth/oidc'

# Create oauth2 client
client = WebApplicationClient(client_id)
# Create PKCE code verifier used in the authorization code
code_verifier = client.create_code_verifier(50)
code_challenge = client.create_code_challenge(code_verifier, code_challenge_method='S256')

# Create a URL to which client (user) browser should be redirected to
uri = client.prepare_request_uri(f'{base_url}/authorize',
                                 redirect_uri=redirect_uri,
                                 scope=['some-app-scope-1', 'offline_access'], # offline_access provides refresh token
                                 code_challenge=code_challenge,
                                 code_challenge_method='S256'
                                 )


# Print the link & ask for the link to which user was redirected to
# Note: There should be a server running to catch that redirection...
print(uri)
response_uri = input("Enter response uri: ")

# Prepare a token request 
token_request = client.prepare_token_request(f'{base_url}/token', authorization_response=response_uri, redirect_url=redirect_uri, code_verifier=code_verifier, client_secret=client_secret)
url, headers, dada = token_request
r = requests.post(url, headers=headers, data=dada)
r_json = r.json()

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