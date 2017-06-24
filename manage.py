#!/usr/bin/env python
import sys

import app


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

        # Build payload
        try:
            payload = app.util.build_payload(marathon_file, values)
        except Exception as ex:
            raise ValueError("Unable to parse marathon_file. Got {}".format(ex))

        # Deploy application
        app.deploy.deploy_application(server, payload, trigger_restart)
    except Exception as ex:
        print("Exception: {}".format(ex))
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
