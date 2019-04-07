import requests
from bs4 import BeautifulSoup
from typing import List


class Session:
    def __init__(self, username: str, password: str, spire_id: str):
        if (username or password or spire_id) is None:
            Exception('missing credentials')
        self.spire_id = spire_id
        self.session = requests.Session()
        self.session.post(
            'https://www.spire.umass.edu/psp/heproda/',
            params={'cmd': 'login', 'languageCd': 'ENG'},
            data={
                'timezoneOffset': '-120',
                'userid': username,
                'pwd': password,
                'Submit': 'Go'
            }
        )

    def search_area(self, area: str, room_type: str) -> List[dict]:
        """Finds open rooms of a specific type in the desired area of campus.

        Args:
            area (str): area of campus where room is located
                The value should match the value POST-ed to the search form on SPIRE, e.g. 'SY' for Sylvan,
                'NO' for North apartments.
            room_type (str): type of room
                It is assumed the search is filtered by room type. This value should match the value POST-ed via SPIRE,
                e.g. 'DB' for double, 'SG' for single.

        Returns:
            list of dict: contains each room found, bundled with 'building' and 'room'

        """
        # get search page to retrieve form ID and page state
        r_search = self.session.get(
            url='https://www.spire.umass.edu/psc/heproda/EMPLOYEE/HRMS/c/UM_H_SELF_SERVICE.UM_H_SS_RM_SEARCH.GBL',
            params={
                'Page': 'UM_H_SS_RM_SEARCH',
                'Action': 'U',
                'EMPLID': self.spire_id
            }
        )

        # scrape served form values
        soup_search = BeautifulSoup(r_search.text, 'html.parser')
        icsid_search = soup_search.find(id='ICSID').get('value')
        state_search = soup_search.find(id='ICStateNum').get('value')
        form = {
            'ICStateNum': state_search,
            'ICAction': 'UM_H_DRV_RMSRCH_SEARCH_PB',
            'ICSID': icsid_search,
            'UM_H_DRV_RMSRCH_STRM': '1197',
            'UM_H_DRV_RMSRCH_UMH_APPT_TYPE': '119704LFAP',
            'UM_H_DRV_RMSRCH_UMH_RM_SRCH_SCOPE$10$': 'G',
            'UM_H_DRV_RMSRCH_UMH_BLDG_GRP': area,
            'UM_H_DRV_RMSRCH_UMH_RM_SRCH_QUAL1': 'TYPE',
            'UM_H_DRV_RMSRCH_UMH_ROOM_TYPE': room_type,
            'UM_H_DRV_RMSRCH_UMH_RM_SRCH_QUAL2': 'NONE'
        }
        endpoint = 'https://www.spire.umass.edu/psc/heproda/EMPLOYEE/HRMS/c/UM_H_SELF_SERVICE.UM_H_SS_RM_SEARCH.GBL'
        # post a search submission to retrieve table of availability
        response = self.session.post(endpoint, data=form)
        return self._parse_rooms(response.text)

    @staticmethod
    def _parse_rooms(doc: str) -> List[dict]:
        """Parses the response data of a room search result into a friendly format.

        Args:
            doc (str): the response text from the search, expected in XML format.

        Returns:
            list of dict: all of the rooms contained in the results table, keyed under 'building' and 'number'
            containing the building name and full room number, respectively.

        """
        soup = BeautifulSoup(doc, 'html.parser')
        entries = soup.find('table', class_='PSLEVEL1GRID').find_all('tr')[1:]  # first row is just headers
        # column 0 is the building name, column 1 is the full room number
        results = [{'building': col[0].text, 'number': col[1].text} for col in [row.find_all('span') for row in entries]
                   if not col[0].text.isspace()]
        return results
