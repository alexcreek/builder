import os
import shutil
import sys
import tempfile
import threading
from logging import getLogger
from subprocess import Popen, PIPE
from git import Repo
import requests
import yaml
import builder.common

# setup logging
# log to a separate stream than the main thread
builder.common.setup_logger(__name__)
logger = getLogger(__name__)

if not (os.getenv('GH_USER') or os.getenv('GH_TOKEN')):
    logger.critical('GH_USER and GH_TOKEN not found in environment')
    sys.exit(1)

class Project(threading.Thread):
    def __init__(self, url, commit, ref, status_url):
        super().__init__()
        self.url = url
        self.commit = commit
        self.branch = ref.split('/')[2]
        self.status_url = status_url.replace('{sha}', commit)
        self.path = None
        self.manifest = {}

    def run(self):
        self.send_status('pending')
        self.log()
        self.checkout()
        self.parse_manifest()
        rc = self.build()
        self.cleanup()
        if rc == 0:
            self.send_status('success')
        else:
            self.send_status('failed')

    def log(self):
        logger.info('Repository: %s', self.url)
        logger.info('Branch: %s', self.branch)
        logger.info('Commit: %s', self.commit)

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

    def parse_manifest(self):
        logger.info('Reading Builderfile')
        try:
            with open('{}/Builderfile'.format(self.path), 'r') as f:
                self.manifest = yaml.load(f, Loader=yaml.Loader)
        except FileNotFoundError:
            logger.critical('Builderfile not found in project')
            logger.critical('Cancelling build')
            sys.exit(1)

    def build(self):
        logger.info('Changing into directory %s', self.path)
        ocwd = os.getcwd()
        os.chdir(self.path)

        logger.info('Running build command: %s', self.manifest['build'])
        p = Popen(self.manifest['build'], stdout=PIPE, shell=True)
        sout, _ = p.communicate(timeout=1200)
        logger.info(sout.decode())
        os.chdir(ocwd)
        logger.info('Got return code %i', p.returncode)
        if p.returncode == 0:
            logger.info('Build successful')
        else:
            logger.info('Build failed')
        return p.returncode

    def cleanup(self):
        logger.info('Deleting project directory: %s', self.path)
        shutil.rmtree(self.path)

    def send_status(self, status):
        r = requests.post(
            self.status_url,
            json={'state': status, 'context': 'Builder'},
            auth=(os.getenv('GH_USER'), os.getenv('GH_TOKEN')),
            )
