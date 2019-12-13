import subprocess
import tempfile
import sys
import shutil

class Project():
    def __init__(self, url, commit, ref):
        self.url = url
        self.commit = commit
        self.branch = ref.split('/')[2]

    def clone_repo(self):
        self.path = tempfile.mkdtemp()
        print(self.path, file=sys.stderr)
        a = subprocess.run(["git", "clone", self.url, self.path], capture_output=True)
        print(a, file=sys.stderr)

    def cleanup(self):
        shutil.rmtree(self.path)
        
        