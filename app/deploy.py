#!/usr/bin/env python
"""
Everything needed to publish an application to a Marathon server.
"""
import json
import requests


def deploy_application(server, payload, trigger_restart=False):
    app_uri = '{}/v2/apps'.format(server)
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
        print("Unable to deploy application to Marathon. Got {}".format(response.text))
        raise Exception("Unable to deploy application to Marathon. Got {}".format(response.text))

    return True
