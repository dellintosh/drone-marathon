import json
import os
import unittest

import app.deploy
import app.util

BASE_PATH = os.path.dirname(os.path.abspath(__name__))


class MarathonTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

        # Add secrets
        self.marathon_secret_value = 'SomeSecretValue'
        self.another_secret = 'AnotherSecretValueIsHere'
        os.environ['MARATHON_SECRET_VALUE'] = self.marathon_secret_value
        os.environ['ANOTHER_SECRET'] = self.another_secret

        # Bootstrap environment
        app.config.load_values()
        self.configs = app.config
        # In testing mode, the values need to be split (in prod they come in as a list already)
        self.configs['VALUES'] = self.configs['VALUES'].split(',')

    def test_environment(self):
        self.assertIn('SERVER', self.configs)
        self.assertIn('MARATHON_FILE', self.configs)
        self.assertIn('TRIGGER_RESTART', self.configs)

    def test_build_payload_injects_secrets(self):
        payload = app.util.build_payload(self.configs['MARATHON_FILE'], self.configs['VALUES'])  # SUT
        actual = json.loads(payload)

        self.assertEqual(self.marathon_secret_value, actual['env']['SOME_VALUE'])
        self.assertEqual(self.another_secret, actual['env']['ANOTHER_SECRET_IS_HERE'])

    def test_deploy(self):
        # TODO: Figure out how to test `deploy_application`!!
        # payload = app.util.build_payload(self.configs['MARATHON_FILE'], self.configs['VALUES'])  # SUT
        # server = 'https://localhost:8080'
        # actual = app.deploy.deploy_application(server, payload, False)

        # self.assertEqual('foo', actual)
        pass


if __name__ == '__main__':
    unittest.main()
