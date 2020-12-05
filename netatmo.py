#!/usr/bin/env python3
import re
import time
import json
import logging
import requests


class netatmo:
    """
    Simple abstraction of the netatmo REST API
    """

    def __init__(self, authtoken):
        """
        Create netatmo REST API abstraction with authtoken
        """
        self.authtoken = authtoken

    def update_authtoken(self):
        headers = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0'
        }
        response = requests.get('https://weathermap.netatmo.com/', headers=headers)
        if not response.text:
            return False
        tokens = re.findall(r'accessToken: "(.*)"', response.text)
        if(len(tokens) == 0):
            logging.warning("Could not find token in response.")
            return False
        for token in tokens:
            if(token == self.authtoken):
                logging.debug("Token is still uptodate. Not updating")
                return True
            logging.info("Updating accessToken.")
            self.authtoken = token


    def getmeasure_current(self, device_id, module_id, measure, scale='max'):
        """
        Get specific measurement from specific device module.
        """
        current_time = int(time.time())
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': 'Bearer {}'.format(self.authtoken),
        }
        data = {
            'date_begin': '{}'.format(current_time-1200),
            'date_end': '{}'.format(current_time),
            'device_id': device_id,
            'module_id': module_id,
            'scale':scale,
            'type':measure
        }

        json_string = json.dumps(data)
        try:
            response = requests.post('https://app.netatmo.net/api/getmeasure', headers=headers, data=json_string)
            if(response.status_code!=200):
                logging.warning('Invalid HTTP status code from API')
                return None
        except Exception as error:
            logging.warning('HTTP error: {}'.format(error))
            return None
        
        if not (response.json):
            logging.warning('API did not return valid JSON')
            return None

        try:
            body_list = response.json().get("body",[])
            if not (len(body_list)):
                return None
        except Exception as error:
            logging.warning('body element not found in JSON: {}'.format(error))
        
        try:
            values = body_list[-1].get("value")
            value = [0.0,0.0,0.0]
            for c_val in values:
                for i,x in enumerate(c_val):
                    if x is not None:
                        value[i] = value[i] + x
                    else:
                        return None
            value = list(map(lambda x: float(x)/float(len(values)),value))
            return value
        except Exception as error:
            logging.warning('Unexpected value error: {}'.format(error))


