import os
import unittest

# import run_marathon

BASE_PATH = os.path.dirname(os.path.abspath(__name__))
# We use testapp as a sample application to publish.
TEST_PACKAGE_PATH = os.path.join(BASE_PATH, "testapp")


class MarathonTestCase(unittest.TestCase):
    default_env = {
        "PLUGIN_SERVER": "http://localhost:8080",
        "PLUGIN_PACKAGE_PATH": TEST_PACKAGE_PATH,
        "PLUGIN_VALUES": '{"TAG": "alpine"}'
    }

    def test_environment(self):
        values = os.environ.get('PLUGIN_VALUES').split(',')
        for value in values:
            print("Environment {} has value: {}".format(value, os.environ.get(value.upper())))
        self.assertEqual('foo', 'bar')
        # os.environ.update(self.default_env)
        # configs = run_marathon.config_store
        # print(configs)

    # def test_upload(self):
    #     """
    #     Tests a simple application upload to a Marathon server.
    #     """
    #     run_marathon.main()


if __name__ == '__main__':
    unittest.main()
