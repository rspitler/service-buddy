import os

from service_buddy.ci.ci import BuildCreatorManager
from service_buddy.service.service import Service
from testcase_parent import ParentTestCase

DIRNAME = os.path.dirname(os.path.abspath(__file__))


class BitbucketBuildTestCase(ParentTestCase):


    @classmethod
    def setUpClass(cls):
        super(BitbucketBuildTestCase, cls).setUpClass()
        cls.test_resources = os.path.join(DIRNAME, '../resources/bitbucket_build_test')
        cls.test_bad_resources = os.path.join(DIRNAME, '../resources/bitbucket__bad_build_config_test')
        cls.yml_folder = os.path.join(cls.test_resources, "app1", "service")
        cls.app_dir = os.path.join(cls.test_resources, "app1")

    def test_bitbucket_build_creation(self):
        build_creator = BuildCreatorManager(dry_run=False, template_directory=self.test_resources)
        test_service = Service(app="app1", role="service", definition={"service-type": "test"})
        build_creator.create_project(
                          service_definition=test_service,
                          app_dir=self.temp_dir)
        listdir = os.listdir(self.temp_dir)
        self.assertTrue('app1-service' in listdir, "Failed to find app dir")
        listdir = os.listdir(os.path.join(self.temp_dir, 'app1-service'))
        self.assertTrue('bitbucket-pipelines.yml' in listdir,"Failed to find build file")

    def test_bitbucket_failure(self):
        build_creator = BuildCreatorManager(dry_run=True, template_directory=self.test_bad_resources)
        test_service = Service(app="app1", role="service", definition={"service-type": "test"})
        self.assertRaises(Exception,
                          build_creator.create_project,
                          service_definition=test_service,
                          app_dir=self.app_dir)

    def _assertInList(self, param, line_list, error_message):
        for line in line_list:
            if param in line:
                return
        self.fail(error_message)

    def _assertInYaml(self, expected_error_msg, directory):
        destination = os.path.join(directory, '.travis.yml')
        with open(destination) as desty:
            readlines = desty.readlines()
            for expected, error_msg in expected_error_msg.items():
                self._assertInList(expected, readlines, error_msg)
