#!/usr/bin/env python2

# -*- coding: utf-8 -*-

# complete ebuds API is at https://github.com/john30/ebusd/wiki/3.3.-MQTT-client

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io, json
from ebusd.ebusd_client import SnipsEbusd


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

# each intent has a language associated with it
# extract language of first intent of assistant since there should only be one language per assistant
lang = json.load(open('/usr/share/snips/assistant/assistant.json'))['intents'][0]['language'] 

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
    if intentname in ["GetHwcQuickVetoTemp","SetHwcQuickVetoTemp","GetHeatingCurve","SetHeatingCurve","GetHotWaterTemp"]:
	conf = read_configuration_file(CONFIG_INI)
	action_wrapper(hermes, intentMessage, conf)
    else:
	pass


def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined 

    Refer to the documentation for further details.
    """
    intentname = intentMessage.intent.intent_name.split(':')[1]

    ebus = SnipsEbusd(conf["secret"]["ebusd_mqtt_ip"],conf["secret"]["heating_system"],conf["secret"]["mqtt_prefix"])

    niy_de = 'Diese Funktion ist fuer dieses Heizungssystem noch nicht implementiert'
    niy_en = 'This feature has not yet been implemented for this heating system'

    if intentname == "GetHwcQuickVetoTemp":
	qwt = ebus.getHwcQuickVetoTemp()
	if qwt is None:
	    if lang == 'de':
		result_sentence = niy_de
	    elif lang == 'en':
		result_sentence = niy_en
	else:
	    if lang == 'de':
		result_sentence = u'Die QuickVetoTemperatur ist %s Grad.' %(qwt)
	    elif lang == 'en':
		result_sentence = u'The QuickVetoTempetarue is %s.' %(qwt)

    if intentname == "SetHwcQuickVetoTemp":
	conn = ebus.setHwcQuickVetoTemp("52.0")
	if conn is None:
	    if lang == 'de':
		result_sentence = niy_de
	    elif lang == 'en':
		result_sentence = niy_en
	else:
	    if lang == 'de':
		result_sentence = u'Die Wassertemperatur wurde auf 52 Grad gesetzt'
	    elif lang == 'en':
		result_sentence = u'The hot water temperature has been set to 52 degree'

    if intentname == "GetHeatingCurve":
	hcurve = ebus.getHeatingCurve()
	if hcurve is None:
	    if lang == 'de':
		result_sentence = niy_de
	    elif lang == 'en':
		result_sentence = niy_en
	else:
	    if lang == 'de':
		result_sentence = u'Die Heizkurve ist %s.' %(hcurve)
	    elif lang == 'en':
		result_sentence = u'The heating curve is %s.' %(hcurve)

    if intentname == "SetHeatingCurve":
	hcurve = ebus.setHeatingCurve("0.30")
	if hcurve is None:
	    if lang == 'de':
		result_sentence = niy_de
	    elif lang == 'en':
		result_sentence = niy_en
	else:
	    if lang == 'de':
		result_sentence = u'Die Heizkurve wurde auf %s gesetzt.' %(hcurve)
	    elif lang == 'en':
		result_sentence = u'The heating curve has been set to %s.' %(hcurve)

    if intentname == "GetHotWaterTemp":
	hwctemp = ebus.getHotWaterTemp()
	if hwctemp is None:
	    if lang == 'de':
		result_sentence = niy_de
	    elif lang == 'en':
		result_sentence = niy_en
	else:
	    if lang == 'de':
		result_sentence = u'Die Wassertemperatur ist %s Grad.' %(int(round(float(hwctemp))))
	    elif lang == 'en':
		result_sentence = u'The hot water temperature is %s degree.' %(int(round(float(hwctemp))))

    hermes.publish_end_session(intentMessage.session_id, result_sentence.encode('utf-8'))

if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
	h.subscribe_intents(subscribe_intent_callback).start()
