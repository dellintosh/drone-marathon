#!/usr/bin/env python
import os
import sys

import app.util
import app.deploy


def main():

    try:
        # Get all input values from environment
        print('Starting...')
        app.config.load_values()
        server = app.config['SERVER']
        marathon_file = '{}/{}'.format(os.getcwd(), app.config['MARATHON_FILE'])
        values = app.config['VALUES'].split(',')
        trigger_restart = app.config['TRIGGER_RESTART']

        # Build payload
        try:
            print('Building payload...')
            payload = app.util.build_payload(marathon_file, values)
            print('Payload Built: {}'.format(payload))
        except Exception as ex:
            raise ValueError('Unable to parse marathon_file. Got {}'.format(ex))

        # Deploy application
        app.deploy.deploy_application(server, payload, trigger_restart)
    except Exception as ex:
        print('Exception: {}'.format(ex))
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
