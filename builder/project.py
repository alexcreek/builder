import os
import shutil
import sys
import tempfile
import threading
from logging import getLogger
from subprocess import Popen, PIPE
from git import Repo
import yaml
import builder.utils

# setup logging
builder.utils.setup_logger(__name__)
logger = getLogger(__name__)

class Project(threading.Thread):
    def __init__(self, url, commit, ref):
        super().__init__()
        self.url = url
        self.commit = commit
        self.branch = ref.split('/')[2]
        self.path = None
        self.manifest = {}

    def run(self):
        self.log()
        self.checkout()
        self.parse_manifest()
        self.build()
        self.cleanup()

    def checkout(self):
        self.path = tempfile.mkdtemp()
        logger.info('Cloning %s into %s', self.url, self.path)
        r = Repo.clone_from(self.url, self.path)

        logger.info('Checking out branch %s', self.branch)
        r.git.checkout(self.branch)

        try:
            assert r.active_branch.commit.hexsha == self.commit
        except AssertionError:
            logger.critical('Commit mismatch. %s is not %s',
                            r.active_branch.commit.hexsha, self.commit)
            logger.critical('Cancelling build')
            sys.exit(1)
        try:
            assert r.active_branch.name == self.branch
        except AssertionError:
            logger.critical('Branch mismatch. %s is not %s',
                           r.active_branch.name, self.branch)
            logger.critical('Cancelling build')
            sys.exit(1)


    def build(self):
        logger.info('Changing into directory %s', self.path)
        ocwd = os.getcwd()
        os.chdir(self.path)

        logger.info('Running build command: %s', self.manifest['build'])
        p = Popen(self.manifest['build'], stdout=PIPE, shell=True)
        while True:
            line = p.stdout.readline().rstrip()
            if not line:
                break
            logger.info(line.decode())
        logger.info('Build complete!')
        os.chdir(ocwd)

    def parse_manifest(self):
        logger.info('Reading Builderfile')
        try:
            with open('{}/Builderfile'.format(self.path), 'r') as f:
                self.manifest = yaml.load(f, Loader=yaml.Loader)
        except FileNotFoundError:
            logger.critical('Builderfile not found in project')
            logger.critical('Cancelling build')
            sys.exit(1)


    def test(self):
        pass

    def cleanup(self):
        logger.info('Deleting project directory: %s', self.path)
        shutil.rmtree(self.path)

    def log(self):
        logger.info('Repository: %s', self.url)
        logger.info('Branch: %s', self.branch)
        logger.info('Commit: %s', self.commit)
