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
        self.assertEqual({}, os.environ)
        # print("Environment: {}".format(os.environ.get()))
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
