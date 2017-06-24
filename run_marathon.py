#!/usr/bin/env python
"""
Everything needed to publish an application to a Marathon server.
"""
import json
import sys

import requests

import app


def deploy_application(server, marathon_file, values, trigger_restart=False):
    app_uri = '{}/v2/apps'.format(server)
    try:
        payload = app.build_payload(marathon_file, values)
        app_id = json.loads(payload)['id']
    except Exception as ex:
        raise ValueError("Unable to parse marathon_file. Got {}".format(ex))

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


def main():

    try:
        # Get all input values from environment
        app.config.load_values()

        server = app.config['SERVER']
        marathon_file = '{}/{}'.format(
            app.config['PACKAGE_PATH'],
            app.config['MARATHON_FILE']
        )
        values = app.config['VALUES'].split(',')
        trigger_restart = app.config['TRIGGER_RESTART']

        deploy_application(server, marathon_file, values, trigger_restart)
    except Exception as ex:
        print("Exception: {}".format(ex))
        sys.exit(1)
    # sys.exit(0)


if __name__ == "__main__":
    main()
