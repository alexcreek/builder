import subprocess
import tempfile
import sys
import shutil
import time
import threading

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
        print(self.path, file=sys.stderr, flush=True)
        a = subprocess.run(["git", "clone", self.url, self.path], capture_output=True)
        print(a, file=sys.stderr, flush=True)
        time.sleep(5)

    def build(self):
        time.sleep(5)

    def test(self):
        time.sleep(5)

    def cleanup(self):
        shutil.rmtree(self.path)
