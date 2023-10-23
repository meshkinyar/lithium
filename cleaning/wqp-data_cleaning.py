##{
import pandas as pd
import numpy as py
import pyreadr
import pickle
import re
from datetime import datetime
##}

## Import csv
wqp_data = pd.read_csv("../data/resultphyschem.csv", low_memory=False)
##

## Restrict to 1960 onward
# Notes: We only have crime data going back to 1960 (and even later for the data we need)
wqp_data['startDate'] = pd.to_datetime(wqp_data['ActivityStartDate'])
wqp_data = wqp_data[wqp_data['startDate'].dt.year >= 1960]
##

## Quantified?
# Notes: Basic cleaning step, if a reading cannot be quantified then we cannot use it
wqp_data['isQuantified'] = False
wqp_data['isQuantified'] = wqp_data['ResultDetectionConditionText'].isna()
##

## USGS Study?
# Notes: Some states are overrepresented (e.g. Oregon) so we might want to restrict our sample to USGS led studies
usgsAliases = ['USGS', 'US Geological Survey', 'U.S. Geological Survey']
wqp_data['isUSGS'] = 0
for i in usgsAliases:
    matchString = '.*'+i+'.*'
    wqp_data['isUSGS'] = wqp_data['isUSGS'] + wqp_data['ActivityConductingOrganizationText'].str.match(matchString)
wqp_data['isUSGS'] = wqp_data['isUSGS'] > 0
##

## Dissolved?
# Notes: Dissolved Lithium is probably our best measure as to what is bioavailable to organisms.
# See: https://www.epa.gov/system/files/documents/2022-01/parameter-factsheet_metals_508.pdf

wqp_data['Dissolved'] = wqp_data['ResultSampleFractionText'] == 'Dissolved'

##


