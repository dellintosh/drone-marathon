#!/usr/bin/env python
"""
Deploys to a Marathon cluster
"""
import json
import subprocess

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
        health_checks = []
        for health_check in self.vargs.get('health_checks', []):
            health_checks.append({
                'path': health_check.get('path', "/"),
                'protocol': health_check.get('protocol', 'HTTP'),
                'portIndex': health_check.get('port_index', 0),
                'gracePeriodSeconds': health_check.get('grace_period_seconds', 300),
                'intervalSeconds': health_check.get('interval_seconds', 60),
                'timeoutSeconds': health_check.get('timeout_seconds', 20),
                'maxConsecutiveFailures': health_check.get('max_consecutive_failures', 3)
            })

        # TODO: Add these?
        # 'port': health_check.get('port'),
        # 'command': health_check.get('command', )

        if health_checks:
            result['healthChecks'] = health_checks

        # Labels
        # result['labels'] = self.vargs.get('labels', {})

        # Process Environment
        # result['env'] = self.vargs.get('process_environment', {})

        # Check these arrays ?
        # result['uris'] = self.vargs.get('uris', [])
        # result['args'] = self.vargs.get('args', [])

        return result

    def run(self):
        """
        The main entrypoint for the plugin.
        """
        # Retrives plugin input from stdin/argv, parses the JSON, returns a dict.
        # payload = plugin.get_input()
        # vargs are where the values passed in the YaML reside.
        # vargs = payload["vargs"]

        # Formulate the POST request.
        server = self.__get_argument('server')
        # app_uri = '{}/v2/apps{}'.format(server, self.vargs.get('id', ''))
        app_uri = '{}/v2/apps'.format(server)
        data = self.__build_marathon_payload()
        payload = json.dumps(data)

        print("Deploying Marathon Application (at {}) definition: {}".format(app_uri, payload))
        response = requests.post(app_uri, data=payload)
        print("Response from Marathon: {}".format(response.json()))

        # data = payload["build"]
        # response = requests.post(vargs["url"], data=data)
        # response.raise_for_status()
        # print("TODO: Implement push to Marathon here!")

        return True


class MarathonCliError(subprocess.CalledProcessError):

    pass
