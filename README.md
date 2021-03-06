# OAuth2/OIDC demo for system to integration

## SOLELY FOR DEMO PURPOSES!

## Purpose

A locally runnable demo for acquiring access token from OAuth2/OIDC server, so requests can be made to a secured endpoints.

## More info

https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow
https://auth0.com/docs/get-started/authentication-and-authorization-flow/client-credentials-flow#how-it-works

## Setup

### Requirements

* Docker https://www.docker.com/get-started/
* Python 3 (tested with 3.8)

### Install dependencies

Python virtual environment is strongly recommended.

* Create virtual environment by running `python -m venv venv`
* Activate virtual env by `source venb/bin/activate` (or on Windows `.venv\Scripts\activate`)
* Install libraries `pip install -r requirements.txt`

### Running the demo

Start the mock OAuth2/OIDC server `docker compose up -d` (Mock server can be shutdown with `docker compose down`)

Allow unsecure connections for Oauth2. WARNING! DO NOT USE FOR ANYTHING ELSE THAN LOCAL DEMO PURPOSES. `export OAUTHLIB_INSECURE_TRANSPORT=1` (or on Windows `set OAUTHLIB_INSECURE_TRANSPORT=1`)

Run either `application_auth_code.py` for Authorization code grant based demo or `application_client_creds.py` for Client credentials grant. `python main.py`. (Program can be exited by CTRL+C in terminal or simply exiting the application by the red cross.)
