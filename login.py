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

s = requests.Session()
payload = {'cmd': 'login', 'languageCd': 'ENG'}
creds = {
    'timezoneOffset': '-120',
    'userid': config['user'],
    'pwd': config['password'],
    'Submit': 'Go'
}
r3 = s.post('https://www.spire.umass.edu/psp/heproda/',
            params=payload,
            data=creds)

r = s.get('https://www.spire.umass.edu/psc/heproda/EMPLOYEE/HRMS/c/UM_H_SELF_SERVICE.UM_H_SS_RMSEL_HOME.GBL?FolderPath=PORTAL_ROOT_OBJECT.HOUSING.UM_H_SS_RMSEL_HOME_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder')

file = open('index.html', 'w')
file.write(r.text)
file.close()
