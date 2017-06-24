import json
import os
import unittest

import app.config

BASE_PATH = os.path.dirname(os.path.abspath(__name__))
# We use testapp as a sample application to publish.
TEST_PACKAGE_PATH = os.path.join(BASE_PATH, "testapp")


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

    def test_environment(self):
        self.assertIn('SERVER', self.configs)
        self.assertIn('MARATHON_FILE', self.configs)
        self.assertIn('TRIGGER_RESTART', self.configs)

    def test_build_payload_injects_secrets(self):
        payload = app.build_payload(self.configs['MARATHON_FILE'], self.configs['VALUES'])
        actual = json.loads(payload)

        self.assertEqual(self.marathon_secret_value, actual['env']['SOME_VALUE'])
        self.assertEqual(self.another_secret, actual['env']['ANOTHER_SECRET_IS_HERE'])


if __name__ == '__main__':
    unittest.main()
