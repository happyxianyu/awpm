import sys
import subprocess
import platform
import pathlib

os_name = platform.system().lower()

def run_cmd(cmd, cwd):
    subprocess.run(cmd, cwd=cwd , shell=True)

def check_run_cmd(cmd, cwd, enable_print=True):
    if enable_print:
        stdout = None
    else:
        stdout = subprocess.PIPE
    subprocess.check_call(cmd, cwd=cwd, shell=True, stdout=stdout)

def ask_for_check_run_cmd(cmd, cwd):
    print(f'Require to execute: {cmd}')
    w = input("Press Enter to continue...")
    check_run_cmd(cmd, cwd)

def insert_python_module_path(path):
    sys.path.insert(0, str(path))



def parse_argv(argv):
    import argparse
    class MyArgParser(argparse.ArgumentParser):
        def error(self, message):
            self.print_help()
            exit(1)

    def add_flags(parser, flags):
        for arg, kwargs in flags:
            parser.add_argument(arg, **kwargs)

    common_flags = [
        ('-y', dict(help='skip asking', action='store_true'))
    ]

    parser = MyArgParser()
    add_flags(parser, common_flags)

    subparsers = parser.add_subparsers(dest='command', required=True)

    subparser_build = subparsers.add_parser('build')
    add_flags(subparser_build, common_flags)

    subparser_install = subparsers.add_parser('install')
    add_flags(subparser_install, common_flags)

    subparser_uninstall = subparsers.add_parser('uninstall')
    add_flags(subparser_uninstall, common_flags)

    args = parser.parse_args(argv[1:])
    return args

def install_python_requirements():
    ask_for_check_run_cmd(f'pip install -r requirements.txt', cwd=pathlib.Path(__file__).parent)

def config_self(enable_ask:bool):
    global ask_for_check_run_cmd
    if not enable_ask:
        ask_for_check_run_cmd = check_run_cmd



def main():
    args = parse_argv(sys.argv)
    config_self(enable_ask=not args.y)
    # install_python_requirements()

    # now we can import non-standard packages
    from cbutil import Path
    proj_root = Path(__file__).prnt
    insert_python_module_path(str(proj_root/'info'))

    from project_info import PATH

    if args.command == 'build':
        return
    
    if args.command == 'install':
        if os_name == 'windows':
            cmd = (PATH.root/'export/awpm.bat').quote
            self_project=PATH.root.absolute().quote
            check_run_cmd(f'{cmd} add {self_project}', cwd=PATH.root)
        else:
            raise NotImplementedError
        return
    
    if args.command == 'uninstall':
        if os_name == 'windows':
            cmd = 'awpm del --id ngnjIMR5RUuj2O5SGAdbWA=='
            check_run_cmd(cmd, cwd=PATH.root)
        else:
            raise NotImplementedError
        return

if __name__ == '__main__':
    main()
