import os
import unittest

import run_marathon

BASE_PATH = os.path.dirname(os.path.abspath(__name__))
# We use testapp as a sample application to publish.
TEST_PACKAGE_PATH = os.path.join(BASE_PATH, "testapp")


class MarathonTestCase(unittest.TestCase):
    default_env = {
        "PLUGIN_SERVER": "http://localhost:8080",
        "PLUGIN_PACKAGE_PATH": TEST_PACKAGE_PATH,
        "PLUGIN_VALUES": '{"TAG": "alpine"}'
    }

    def setUp(self):
        os.environ.update(self.default_env)
        run_marathon.environment_variables.load_values()

    @classmethod
    def setUpClass(cls):
        # TODO: This should probably go away once load_values() accepts
        # an optional override kwarg.
        os.environ.update(cls.default_env)
        run_marathon.environment_variables.load_values()

    def test_upload(self):
        """
        Tests a simple application upload to a Marathon server.
        """
        run_marathon.main()


if __name__ == '__main__':
    unittest.main()
