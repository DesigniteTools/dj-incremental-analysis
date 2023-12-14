import requests
import time

class Utils:
    '''Utility functions.'''

    @staticmethod
    def api_request(url, token, method="GET", data=None, params=None):
        '''Make an API request to GitHub.'''

        headers = {"Authorization": f"Bearer {token}"}
        timeout = 10
        response = requests.request(method, url, headers=headers, timeout=timeout, data=data, params=params)
        if int(response.headers.get("x-ratelimit-remaining",0)) < 10:
            print("API rate limit low. Waiting for a minute")
            time.sleep(60)
        
        return response