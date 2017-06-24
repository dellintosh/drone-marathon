import os
import urllib.parse

from evarify import ConfigStore, EnvironmentVariable
from evarify.filters.python_basics import validate_is_not_none, value_to_none,\
    value_to_bool, comma_separated_str_to_list


def build_payload(marathon_file, values):
    # Load marathon_file data
    with open(marathon_file, encoding='utf-8') as data_file:
        data = data_file.read()

    for value in values:
        key = '<<{}>>'.format(value.upper())
        val = os.environ.get(value.upper())
        if val:
            data = data.replace(key, val)
        else:
            raise Exception('Unable to find a value for {}. Did you forget to add the secret?'.format(key))

    return data


def validate_marathon_server_url(config_val, evar):
    parsed = urllib.parse.urlsplit(config_val)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError(
            "You must specify the full, absolute URI to your Marathon server "
            "(including ).: %s", config_val)
    return config_val


config = ConfigStore({
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
    'MARATHON_FILE': EnvironmentVariable(
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
        filters=[validate_is_not_none, comma_separated_str_to_list],
        default_val=[],
        help_txt=(
            "Replace these keys (in your Marathon file) with values from the "
            "environment. This can be used to inject secrets or other "
            "environment variables into the marathon.json file."
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