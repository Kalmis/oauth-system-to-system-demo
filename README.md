# OAuth2/OIDC demo for system to integration

## SOLELY FOR DEMO PURPOSES!

## Purpose

A locally runnable demo for creating a trusted connection between to systems using OAuth2 Authorization code and Client credentials grant.

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

Run either `application_auth_code.py` for Authorization code grant based demo or `application_client_creds.py` for Client credentials grant. `python main.py`. (Program can be exited by CTRL+C in terminal or simply exiting the application by the red cross.)
