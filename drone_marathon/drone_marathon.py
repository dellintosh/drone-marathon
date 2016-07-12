#!/usr/bin/env python
"""
Deploys to a Marathon cluster
"""
import subprocess

from drone import plugin


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

    def __build_marathon_payload(self):
        result = {}

        result['id'] = self.__get_argument('id')
        result['instances'] = self.__get_argument('instances')
        result['cpus'] = self.__get_argument('cpus')
        result['mem'] = self.__get_argument('mem')
        result['cmd'] = self.__get_argument('cmd')

        # Docker container
        result['container'] = {
            'type': 'DOCKER',
            'volumes': [],
            'docker': {
                'forcePullImage': self.vargs.get('docker_force_pull', False),
                'image': self.__get_argument('docker_image'),
                'network': self.vargs.get('docker_network', 'BRIDGE'),
                'parameters': self.vargs.get('docker_parameters', []),  # TODO: Parse these
                'portMappings': self.vargs.get('docker_port_mappings', []),  # TODO: Parse these
                'privileged': self.vargs.get('docker_privileged', False),
            }
        }

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
        # Retrives plugin input from stdin/argv, parses the JSON, returns a dict.
        # payload = plugin.get_input()
        # vargs are where the values passed in the YaML reside.
        # vargs = payload["vargs"]

        # Formulate the POST request.
        server = self.__get_argument('server')

        data = self.__build_marathon_payload()
        print("Built Marathon (at {}) application definition: {}".format(server, data))
        # data = payload["build"]
        # response = requests.post(vargs["url"], data=data)
        # response.raise_for_status()


class MarathonCliError(subprocess.CalledProcessError):

    pass
