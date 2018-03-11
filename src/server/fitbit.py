import datetime
import fitbit
import requests_oauthlib as Oauth2
import pandas as pd

def getSleepData():
    CLIENT_ID = '22CNND'
    CLIENT_SECRET = 'd50713c7425870e331710a35954fb293'
    server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    server.browser_authorize()

    ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
    REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

    auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
