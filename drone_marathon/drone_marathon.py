#!/usr/bin/env python
"""
Deploys to a Marathon cluster
"""
import drone
import requests


def __get_argument(args, key):
    try:
        return args[key]
    except KeyError:
        raise KeyError("Must provide value for `{}`".format(key))


def __build_marathon_payload(args):
    result = {}

    result['id'] = __get_argument(args, 'id')
    result['instances'] = __get_argument(args, 'instances')
    result['cpus'] = __get_argument(args, 'cpus')
    result['mem'] = __get_argument(args, 'mem')
    result['cmd'] = __get_argument(args, 'cmd')

    # Docker container
    result['container'] = {
        'type': 'DOCKER',
        'volumes': [],
        'docker': {
            'forcePullImage': args.get('docker_force_pull', False),
            'image': __get_argument(args, 'docker_image'),
            'network': args.get('docker_network', 'BRIDGE'),
            'parameters': args.get('docker_parameters', []),  # TODO: Parse these
            'portMappings': args.get('docker_port_mappings', []),  # TODO: Parse these
            'privileged': args.get('docker_privileged', False),
        }
    }

    # Process Environment
    result['env'] = args.get('process_environment', {})

    # Check these arrays ?
    result['uris'] = args.get('uris', [])
    result['args'] = args.get('args', [])

    return result


def main():
    """
    The main entrypoint for the plugin.
    """
    # Retrives plugin input from stdin/argv, parses the JSON, returns a dict.
    payload = drone.plugin.get_input()
    # vargs are where the values passed in the YaML reside.
    vargs = payload["vargs"]

    # Formulate the POST request.
    server = __get_argument(vargs, 'server')

    data = __build_marathon_payload(vargs)
    print("Built Marathon (at {}) application definition: {}".format(server, data))
    # data = payload["build"]
    # response = requests.post(vargs["url"], data=data)
    # response.raise_for_status()


if __name__ == "__main__":
    main()
