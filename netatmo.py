#!/usr/bin/env python3
import time
import json
import logging
import requests


class netatmo:

    def __init__(self, authtoken):
        self.authtoken = authtoken


    def getmeasure_current(self, device_id, module_id, measure, scale='max'):
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


