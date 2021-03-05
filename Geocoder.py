from typing import Dict

import requests
import pandas as pd
import json
import os
from main import df_col2

for i, row in df_col2.iterrows():
    apiAddress = str(df_col2.at[i, 'City']) + str(df_col2.at[i, 'State'])

    parameters: Dict[str, str] = {
        'key': os.environ.get('API_KEY'),
        'location': apiAddress
        }

    response = requests.get('http://www.mapquestapi.com/geocoding/v1/batch', params=parameters)

    data = json.loads(response.text)['results']

    lat = data[0]['locations'][0]['latlng']['lat']
    lng = data[0]['locations'][0]['latlng']['lng']

    df_col2.at[i, 'lat'] = lat
    df_col2.at[i, 'lng'] = lng

df_col2.to_csv('Bear_Geo3.cvs')
