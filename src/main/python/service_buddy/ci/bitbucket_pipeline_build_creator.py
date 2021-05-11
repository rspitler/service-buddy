import os

from service_buddy.ci.build_creator import FileBasedBuildCreator
from service_buddy.service.service import Service


class BitBucketPipelineBuildCreator(FileBasedBuildCreator):

    @classmethod
    def get_type(cls):
        return "bitbucket"

    def options(self):
        return {}

    def init(self, dry_run: bool, default_config: dict, build_templates: dict, template_directory: str,
             user: str = None, password: str = None):
        super(BitBucketPipelineBuildCreator, self).init(dry_run, default_config, build_templates, template_directory)

    def _get_build_file(self, service_dir: str):
        return os.path.join(service_dir, "bitbucket-pipelines.yml")

    def _build_exists_action(self, service_dir: str, build_template: dict, service_definition: Service):
        super(BitBucketPipelineBuildCreator, self).create_build(service_dir, build_template, service_definition)
