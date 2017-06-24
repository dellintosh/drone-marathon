import os


def build_payload(marathon_file, values):
    # Load marathon_file data
    print('Reading in Marathon File: {}'.format(marathon_file))
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
