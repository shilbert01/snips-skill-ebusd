# Snips  heating system connector eBUS (e.g. Vaillant) connector
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/snipsco/snips-skill-owm/master/LICENSE.txt)

This is a Snips action to interact with your heating system via ebusd. It is written in Python and is compatible with `snips-skill-server`.

## Setup
### Prerequisites

You'll need to add the Vaillant-eBUS skill in your assistant. It's available on [Snips' console](https://console.snips.ai)

### SAM (preferred)
To install the action on your device, you can use [Sam](https://snips.gitbook.io/getting-started/installation)

`sam install actions -g https://github.com/shilbert01/snips-skill-ebusd.git`

### Manually

Copy it manually to the device to the folder `/var/lib/snips/skills/`
You'll need `snips-skill-server` installed on the pi

`sudo apt-get install snips-skill-server`

Stop snips-skill-server & generate the virtual environment
```
sudo systemctl stop snips-skill-server
cd /var/lib/snips/skills/snips-skill-ebusd/
sh setup.sh
sudo systemctl start snips-skill-server
```

## How to trigger

`Hey Snips`

`Ich will duschen.`

## Logs
Show snips-skill-server logs with sam:

`sam service log snips-skill-server`

Or on the device:

`journalctl -f -u snips-skill-server`

Check general platform logs:

`sam watch`

Or on the device:

`snips-watch`

# Configuration

During installation, the assistant will ask for the IP address of the computer running ebusd with mqtt enabled.
It will further ask for the type of heating sytem (e.g. 1: Calormatic 430, 2:GeoTherm plus VWS)
This is because different heating system support different subsets of parameters.

Find out more about which parameters are supported by your heating system by running

`ebusctl -f` and/or `ebusctl -f f`

on the device running ebusd.
