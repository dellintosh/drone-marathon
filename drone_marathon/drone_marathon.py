#!/usr/bin/env python
"""
Deploys to a Marathon cluster
"""
import json

from drone import plugin
import requests


class DroneMarathon(object):

    def __init__(self):
        args = plugin.get_input()
        try:
            self.cwd = args['workspace']['path']
        except KeyError:
            self.cwd = None
        self.vargs = args['vargs']

    def __get_argument(self, key):
        try:
            return self.vargs[key]
        except KeyError:
            raise KeyError("Must provide value for `{}`".format(key))

    def __docker_port_mapping(self, mapping):
        return {
            'containerPort': mapping.get('container_port', 0),
            'hostPort': mapping.get('host_port', 0),
            'servicePort': mapping.get('service_port', 0),
            'protocol': mapping.get('protocol', 'tcp'),
        }

    def __marathon_health_check(self, check):
        return {
            'path': check.get('path', '/'),
            'protocol': check.get('protocol', 'HTTP'),
            'portIndex': check.get('port_index', 0),
            'gracePeriodSeconds': check.get('grace_period_seconds', 300),
            'intervalSeconds': check.get('interval_seconds', 60),
            'timeoutSeconds': check.get('timeout_seconds', 20),
            'maxConsecutiveFailures': check.get('max_consecutive_failures', 3)
        }
        # TODO: Add these?
        # 'port': health_check.get('port'),
        # 'command': health_check.get('command', )

    def __build_marathon_payload(self):
        result = {}

        result['id'] = self.__get_argument('id')
        result['instances'] = self.__get_argument('instances')
        result['cpus'] = self.__get_argument('cpus')
        result['mem'] = self.__get_argument('mem')
        result['cmd'] = self.vargs.get('cmd', None)

        # Docker container
        result['container'] = {
            'type': 'DOCKER',
            'volumes': [],
            'docker': {
                'forcePullImage': self.vargs.get('docker_force_pull', False),
                'image': self.__get_argument('docker_image'),
                'network': self.vargs.get('docker_network', 'BRIDGE'),
                'parameters': self.vargs.get('docker_parameters', []),
                'portMappings': [self.__docker_port_mapping(param) for param in self.vargs.get('docker_port_mappings', [])],
                'privileged': self.vargs.get('docker_privileged', False),
            }
        }

        # Health Checks
        result['healthChecks'] = [
            self.__marathon_health_check(check) for check in self.vargs.get('health_checks', [])
        ]

        # Labels
        result['labels'] = self.vargs.get('labels', {})

        # Process Environment
        result['env'] = self.vargs.get('process_environment', {})

        # Check these arrays ?
        result['uris'] = self.vargs.get('uris', [])
        result['args'] = self.vargs.get('args', [])

        return result

    def run(self):
        """
        The main entrypoint for the plugin.
        """
        server = self.__get_argument('server')
        app_uri = '{}/v2/apps'.format(server)
        data = self.__build_marathon_payload()
        payload = json.dumps(data)

        print("Deploying Marathon Application (at {})".format(app_uri))

        check_app_exists = requests.get('{}{}'.format(app_uri, data['id'])).ok
        if check_app_exists:
            app_id = data['id']
            print("Application {} already exists...updating.".format(app_id))

            temp = json.loads(payload)
            del temp['id']
            payload = json.dumps(temp)
            # print("Application id removed.  New data: {}".format(payload))

            response = requests.put('{}{}'.format(app_uri, app_id), data=payload)
        else:
            print("Application {} does not exist...creating it now.".format(data['id']))
            response = requests.post(app_uri, data=payload)

        # Trigger a restart to get new release (if applicable).
        if self.vargs.get('trigger_restart', False):
            requests.post('{}{}/restart'.format(app_uri, app_id))

        print("Response from Marathon: {}".format(response.json()))

        if not response.ok:
            print("Unable to deploy application to Marathon.")
            raise MarathonCliError("Unable to deploy application to Marathon.")

        return True


class MarathonCliError(Exception):

    returncode = 1
