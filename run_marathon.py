#!/usr/bin/env python
"""
Everything needed to publish an application to a Marathon server.
"""
import json
import os
import sys
import urllib.parse

from evarify import ConfigStore, EnvironmentVariable
from evarify.filters.python_basics import validate_is_not_none, value_to_none,\
    value_to_bool
import requests


def validate_marathon_server_url(config_val, evar):
    parsed = urllib.parse.urlsplit(config_val)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError(
            "You must specify the full, absolute URI to your Marathon server "
            "(including ).: %s", config_val)
    return config_val


def __build_marathon_payload(marathon_file, values):
    # Load marathon_file data
    with open(marathon_file, encoding='utf-8') as data_file:
        data = data_file.read()

    # Update the values in the marathon_file
    for k, v in values.items():
        data = data.replace('<<{}>>'.format(k), v)

    return data


def deploy_application(server, marathon_file, values, trigger_restart=False):
    app_uri = '{}/v2/apps'.format(server)
    payload = __build_marathon_payload(marathon_file, values)
    app_id = json.loads(payload)['id']

    print("Deploying Marathon Application (at {})".format(app_uri))

    check_app_exists = requests.get('{}{}'.format(app_uri, app_id)).ok
    if check_app_exists:
        print("Application {} already exists...updating.".format(app_id))

        temp = json.loads(payload)
        del temp['id']
        payload = json.dumps(temp)

        response = requests.put('{}{}'.format(app_uri, app_id), data=payload)
    else:
        print("Application {} does not exist, creating it now.".format(app_id))
        response = requests.post(app_uri, data=payload)

    # Trigger a restart to get new release (if applicable).
    if trigger_restart:
        requests.post('{}{}/restart'.format(app_uri, app_id))

    print("Response from Marathon: {}".format(response.json()))

    if not response.ok:
        print("Unable to deploy application to Marathon.")
        raise Exception("Unable to deploy application to Marathon.")

    return True


config_store = ConfigStore({
    'SERVER': EnvironmentVariable(
        name='PLUGIN_SERVER',
        filters=[
            value_to_none, validate_is_not_none, validate_marathon_server_url
        ],
        default_val='http://marathon.mesos:8080',
        help_txt=(
            "Full path to the root of the Marathon server. Make sure to "
            "include the protocol (and port)."
        )
    ),
    'MARATHONFILE': EnvironmentVariable(
        name='PLUGIN_MARATHONFILE',
        is_required=False,
        filters=[validate_is_not_none],
        default_val='marathon.json',
        help_txt=(
            "Name of your marathon.json configuration file. (optional, "
            "default: marathon.json)"
        )
    ),
    'VALUES': EnvironmentVariable(
        name='PLUGIN_VALUES',
        is_required=False,
        filters=[validate_is_not_none],
        default_val='{}',
        help_txt=(
            "Values (as an object) where key/value will be replaced in "
            "your specified marathonfile, as needed."
        )
    ),
    'PACKAGE_PATH': EnvironmentVariable(
        name='PLUGIN_PACKAGE_PATH',
        is_required=False,
        filters=[value_to_none, validate_is_not_none],
        default_val=os.getcwd(),
        help_txt="Path to the package to upload.",
    ),
    'TRIGGER_RESTART': EnvironmentVariable(
        name='PLUGIN_TRIGGER_RESTART',
        is_required=False,
        filters=[value_to_bool],
        default_val=False,
        help_txt=(
            "Force Marathon to restart application? (default: false)"
        )
    )
})


def main():

    try:
        # Get all input values from environment
        config_store.load_values()

        server = config_store['SERVER']
        marathon_file = '{}/{}'.format(
            config_store['PACKAGE_PATH'],
            config_store['MARATHONFILE']
        )
        print('Got environment values of: {}'.format(
            config_store['VALUES'])
        )
        values = json.loads(config_store['VALUES'])
        trigger_restart = config_store['TRIGGER_RESTART']

        print(server, marathon_file, values, trigger_restart)
        deploy_application(server, marathon_file, values, trigger_restart)
    except Exception:
        sys.exit(1)
    # sys.exit(0)


if __name__ == "__main__":
    main()
