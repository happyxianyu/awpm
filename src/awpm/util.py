import subprocess

__all__ = [
    'run_cmd'
]

def run_cmd(cmd, cwd, enable_print=False):
    if enable_print:
        stdout = None
    else:
        stdout = subprocess.PIPE
    return subprocess.run(cmd, cwd=cwd, shell=True, stdout=stdout)

