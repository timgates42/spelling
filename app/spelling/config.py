"""
Tools to load the default `.pyspelling` config and update it with the
nonwords dictionary and the custom exclusions.
"""

import pathlib
import shutil
import tempfile
from contextlib import contextmanager

import pkg_resources
import yaml


class ConfigContext(object):
    """
    Class to load the default `.pyspelling` config and update it with the
    nonwords dictionary and the custom exclusions.
    """

    def __init__(self, tmppath, config):
        self.tmppath = tmppath
        self.origconfig = config
        self.config = tmppath / ".pyspelling"
        self.init()

    @staticmethod
    def load(config=None):
        """
        Open the existing config
        """
        if config is None:
            config = pkg_resources.resource_filename(__name__, ".pyspelling.yml")
        return yaml.safe_load(config)

    @staticmethod
    def save(target, yamldata):
        """
        Save the updated config
        """
        yaml.safe_dump(target, yamldata)

    def init(self):
        """
        Prepare the updated config
        """
        data = self.load(self.origconfig)
        self.update(data)
        self.save(self.config, data)

    @staticmethod
    def update(data):
        """
        Reconfigure the loaded yaml data as required
        """
        print(repr(data))


@contextmanager
def get_config_context_manager(config=None):
    """
    Loads the default `.pyspelling` config or the one provided and then
    updates it with the nonwords dictionary and the custom exclusions in a
    context manager that cleans up on completion.
    """
    tmpdir = tempfile.mkdtemp()
    yield ConfigContext(pathlib.Path(tmpdir), config)
    shutil.rmtree(tmpdir)