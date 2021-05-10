import json
import logging
import os
from typing import Dict, Any

from ci.bamboo_build_creator import BambooBuildCreator
from ci.bitbucket_pipeline_build_creator import BitBucketPipelineBuildCreator
from ci.travis_build_creator import TravisBuildCreator
from service.service import Service

build_system_map: Dict[str, Any] = {
    BambooBuildCreator.get_type(): BambooBuildCreator(),
    BitBucketPipelineBuildCreator.get_type(): BitBucketPipelineBuildCreator(),
    TravisBuildCreator.get_type(): TravisBuildCreator()}
build_systems = [key for key in build_system_map.keys()]


class BuildCreator(object):
    def __init__(self, template_directory, dry_run):
        super(BuildCreator, self).__init__()
        default_path = os.path.join(template_directory, "build-config.json")
        if os.path.exists(default_path):
            with open(default_path) as fp:
                defaults = json.load(fp)
                self.default_provider = defaults.get('provider', None)
                self.build_templates = defaults.get('build-templates', {})
                self.user = defaults.get('user', os.environ.get('BUILD_SYSTEM_USER'))
                self.password = defaults.get('password', os.environ.get('BUILD_SYSTEM_PASSWORD'))
                self.always_recreate_builds = defaults.get('build-creation-is-idempotent', True)
                self.default_config = defaults
        else:
            logging.warning("Could not local 'build-config.json' in code template directory")
            self.default_provider = "bamboo"
        if self.default_provider not in build_system_map:
            raise Exception("Requested provider is not configured {}".format(self.default_provider))
        else:
            creator = self._get_default_build_creator()
            creator.init(
                dry_run=dry_run,
                default_config=self.default_config,
                build_templates=self.build_templates,
                user=self.user, password=self.password
            )

    def _get_default_build_creator(self):
        return build_system_map[self.default_provider]

    def create_project(self, service_definition: Service, app_dir: str, force_build_creation: bool = False):
        do_create = not service_definition.repo_exists() or self.always_recreate_builds or force_build_creation
        logging.info(
            '[create project] repo exists: %r, always_recreate: %r, force create: %r do_create: %r',
            service_definition.repo_exists(), self.always_recreate_builds, force_build_creation, do_create
        )
        if do_create:
            return self._get_default_build_creator().create_project(
                service_definition=service_definition,
                app_dir=app_dir
            )
