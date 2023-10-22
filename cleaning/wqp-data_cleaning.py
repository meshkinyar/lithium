##{
import pandas as pd
import numpy as py
import pyreadr
import pickle
import re
from datetime import datetime
##}

## Import csv
wqp_data = pd.read_csv("resultphyschem.csv", low_memory=False)
##

## Restrict to 1960 onward
wqp_data['startDate'] = pd.to_datetime(wqp_data['ActivityStartDate'])
wqp_data = wqp_data[wqp_data['startDate'].dt.year >= 1960]
##

## Quantified?
wqp_data['isQuantified'] = False
wqp_data['isQuantified'] = wqp_data['ResultDetectionConditionText'].isna()
##

## USGS Study?
usgsAliases = ['USGS', 'US Geological Survey', 'U.S. Geological Survey']
wqp_data['isUSGS'] = 0
for i in usgsAliases:
    matchString = '.*'+i+'.*'
    wqp_data['isUSGS'] = wqp_data['isUSGS'] + wqp_data['ActivityConductingOrganizationText'].str.match(matchString)
wqp_data['isUSGS'] = wqp_data['isUSGS'] > 0
##
