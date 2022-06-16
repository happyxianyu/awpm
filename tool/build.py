"""
Deprecated
"""


if False:

    import sys
    import subprocess

    from cbutil import Path

    from common import *


    def run_cmd(cmd, cwd):
        subprocess.run(cmd, cwd=cwd , shell=True)

    def check_run_cmd(cmd, cwd):
        subprocess.check_call(cmd, cwd=cwd, shell=True)


    def build():
        pass
        

    if __name__ == '__main__':
        build()


