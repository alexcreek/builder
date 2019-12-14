import subprocess
import tempfile
import shutil
import time
import threading
import uuid
from logging import getLogger

import builder.utils 

builder.utils.init_logging(__name__, 'asdf.log')
logger = getLogger(__name__)

class Project(threading.Thread):
    def __init__(self, url, commit, ref):
        super().__init__()


        self.url = url
        self.commit = commit
        self.branch = ref.split('/')[2]

    def run(self):
        self.checkout()
        self.build()
        self.cleanup()

    def checkout(self):
        self.path = tempfile.mkdtemp()
        logger.info('what up')

        a = subprocess.run(["git", "clone", self.url, self.path],
                           capture_output=True, 
                           text=True)

        logger.info(a.stderr)

        time.sleep(5)

    def build(self):
        time.sleep(5)

    def test(self):
        time.sleep(5)

    def cleanup(self):
        shutil.rmtree(self.path)