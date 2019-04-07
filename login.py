import requests
import yaml
from bs4 import BeautifulSoup

config = {}
with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(-1)

# preserve cookies across requests
s = requests.Session()

# sign in to get auth token cookie
payload = {'cmd': 'login', 'languageCd': 'ENG'}
creds = {
    'timezoneOffset': '-120',
    'userid': config['user'],
    'pwd': config['password'],
    'Submit': 'Go'
}
s.post('https://www.spire.umass.edu/psp/heproda/',
       params=payload,
       data=creds)

# get search page to retrieve form ID and page state
payload = {
    'Page': 'UM_H_SS_RM_SEARCH',
    'Action': 'U',
    'EMPLID': config['spire-id']
}
r_search = s.get('https://www.spire.umass.edu/psc/heproda/EMPLOYEE/HRMS/c/UM_H_SELF_SERVICE.UM_H_SS_RM_SEARCH.GBL',
                 params=payload)

# scrape served form values
soup_search = BeautifulSoup(r_search.text, 'html.parser')
icsid_search = soup_search.find(id='ICSID').get('value')
state_search = soup_search.find(id='ICStateNum').get('value')

# post a search submission
form = {
    'ICStateNum': state_search,
    'ICAction': 'UM_H_DRV_RMSRCH_SEARCH_PB',
    'ICSID': icsid_search,
    'UM_H_DRV_RMSRCH_STRM': '1197',
    'UM_H_DRV_RMSRCH_UMH_APPT_TYPE': '119704LFAP',
    'UM_H_DRV_RMSRCH_UMH_RM_SRCH_SCOPE$10$': 'G',
    'UM_H_DRV_RMSRCH_UMH_BLDG_GRP': 'SY',
    'UM_H_DRV_RMSRCH_UMH_RM_SRCH_QUAL1': 'TYPE',
    'UM_H_DRV_RMSRCH_UMH_ROOM_TYPE': 'DB',
    'UM_H_DRV_RMSRCH_UMH_RM_SRCH_QUAL2': 'NONE'
}
r = s.post('https://www.spire.umass.edu/psc/heproda/EMPLOYEE/HRMS/c/UM_H_SELF_SERVICE.UM_H_SS_RM_SEARCH.GBL',
           data=form)

file = open('index.html', 'w')
file.write(r.text)
file.close()
