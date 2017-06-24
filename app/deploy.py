#!/usr/bin/env python
"""
Everything needed to publish an application to a Marathon server.
"""
import json
import requests


def deploy_application(server, payload, trigger_restart=False):
    app_uri = '{}/v2/apps'.format(server)
    print("Deploying Marathon Application (at {}): {}".format(app_uri, payload))
    headers = {
        'Content-Type': 'application/json',
    }
    app_id = json.loads(payload)['id']

    check_app_exists = requests.get('{}{}'.format(app_uri, app_id), headers=headers).ok
    if check_app_exists:
        print("Application {} already exists...updating.".format(app_id))

        temp = json.loads(payload)
        del temp['id']
        payload = json.dumps(temp)

        response = requests.put('{}{}'.format(app_uri, app_id), data=payload, headers=headers)
    else:
        print("Application {} does not exist, creating it now.".format(app_id))
        response = requests.post(app_uri, data=payload, headers=headers)

    # Trigger a restart to get new release (if applicable).
    if trigger_restart:
        requests.post('{}{}/restart'.format(app_uri, app_id), headers=headers)

    print("Response from Marathon: {}".format(response.json()))

    if not response.ok:
        print("Unable to deploy application to Marathon. Got {}".format(response.json()))
        raise Exception("Unable to deploy application to Marathon. Got {}".format(response.json()))

    return True
