#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# complete ebuds API is at https://github.com/john30/ebusd/wiki/3.3.-MQTT-client

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from ebusd.ebusd_client import SnipsEbusd


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()


def subscribe_intent_callback(hermes, intentMessage):
    user,intentname = intentMessage.intent.intent_name.split(':')  # the user can fork the intent with this method
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined 

    Refer to the documentation for further details. 
    """
    intentname = intentMessage.intent.intent_name.split(':')[1]

    ebus = SnipsEbusd(conf["secret"]["ebusd_mqtt_ip"])

    if intentname == "SetHwcQuickVetoTemp":
	conn = ebus.setHwcQuickVetoTemp("52")
	result_sentence = u'Die Wassertemperatur wurde auf 52 Grad gesetzt'

    if intentname == "GetHwcQuickVetoTemp":
	conn = ebus.getHwcQuickVetoTemp("52")
	result_sentence = u'Die QuickVetoTemperatur ist %s Grad.' %(conn)

    if intentname == "GetHeatingCurve":
	hcurve = ebus.getHeatingCurve()
	result_sentence = u'Die Heizkurve ist %s.' %(hcurve)

    if intentname == "SetHeatingCurve":
	hcurve = ebus.setHeatingCurve("0.3")
	result_sentence = u'Die Heizkurve wurde auf %s gesetzt.' %(hcurve)

    hermes.publish_end_session(intentMessage.session_id, result_sentence.encode('utf-8'))

if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
	h.subscribe_intents(subscribe_intent_callback).start()
