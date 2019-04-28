#!/usr/bin/env python3
import logging
import time
import sched
import argparse
import yaml
from influxdb import influxdb
from netatmo import netatmo

def request_nodes(sc,interval):
    logging.debug('Requesting and adding...')
    for node in myconfig['netatmo']['nodes']:
        if(node.get('rain_module_id',None)):
            rain = mynetatmo.getmeasure_current(node.get('device_id'),node.get('rain_module_id'),'Rain')
            if(rain):
                myinfluxdb.add_measure({'mac':node.get('device_id')},"rain","{:.1f}".format(rain[0]))

        temp_humid = mynetatmo.getmeasure_current(node.get('device_id'),node.get('temp_module_id'),'Temperature,Humidity')
        if(temp_humid):
            myinfluxdb.add_measure({'mac':node.get('device_id')},"temperature","{:.1f}".format(temp_humid[0]))
            myinfluxdb.add_measure({'mac':node.get('device_id')},"humidity","{:.1f}".format(temp_humid[1]))
        pressure = mynetatmo.getmeasure_current(node.get('device_id'),node.get('device_id'),'Pressure')
        if(pressure):
            myinfluxdb.add_measure({'mac':node.get('device_id')},"pressure","{:.1f}".format(pressure[0]))
    
    myinfluxdb.write_influxdb()
    myscheduler.enter(interval,1,request_nodes, (sc,interval))


def read_config(configfile):
    try:
        with open(configfile, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
            return cfg
    except Exception as error:
        print("Could not open config file.")
        return None

if __name__ == "__main__":
    # Execute API requests
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Enable Debug Logging")
    parser.add_argument('--config', type=str, default='config.yml', help='Specify the location of the config file. Defaults to config.yml.')
    args = parser.parse_args()
    if(args.debug):
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    myconfig = read_config(args.config)

    logging.basicConfig(filename=myconfig['logfile'], level=loglevel)

    myinfluxdb = influxdb(myconfig['influxdb']['host'],
                            myconfig['influxdb']['port'],
                            myconfig['influxdb']['user'],
                            myconfig['influxdb']['password'],
                            myconfig['influxdb']['dbname'],
                            myconfig['influxdb']['measurename'])
    mynetatmo = netatmo(myconfig['netatmo']['authtoken'])
    
    logging.info('Started netatmo weather collection')
    print("Started netatmo weather collection!")
    myscheduler = sched.scheduler(time.time,time.sleep)
    myscheduler.enter(1,1,request_nodes,(myscheduler,myconfig['interval']))
    myscheduler.run()


