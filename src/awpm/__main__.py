import sys
import subprocess
import argparse
import json5
import base64
from pprint import pprint

from cbutil import Path

from .persistable import *
from .core import *

self_path = Path(__file__)
proj_root = self_path.parents[2]
sys.path.insert(0, (proj_root/'info').str)
from info import PATH


def run_cmd(cmd, cwd):
    subprocess.run(cmd, cwd=cwd , shell=True)

def check_run_cmd(cmd, cwd):
    subprocess.check_call(cmd, cwd=cwd, shell=True)

def get_project_info_from_project_root(project_root:Path):
    proj_info = project_root/'project_info.json'
    project_root = project_root.absolute()

    with open(proj_info, 'r') as f:
        content:dict = json5.load(f)
        id_:str = content['id']
        name:str = content.get('name', project_root.name)
        version:str = content.get('version')
        export_paths:list = content.get('paths', {}).get('exports', [])
    
    return AWProjectInstallInfo(
        id = base64.urlsafe_b64decode(id_),
        name=name,
        version=version,
        project_root=project_root.str,
        export_paths=export_paths
    )

def parse_argv(argv):
    class MyArgParser(argparse.ArgumentParser):
        def error(self, message):
            self.print_help()
            exit(1)

    parser = MyArgParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    subparser_add = subparsers.add_parser('add', help='manage given project')
    subparser_add.add_argument('project_root', type=str)

    subparser_del = subparsers.add_parser('del', help='remove given project')
    group = subparser_del.add_mutually_exclusive_group()
    group.add_argument('--id', type=str, help='by id')
    group.add_argument('--name', type=str, help='by name')

    subparser_find = subparsers.add_parser('list', help='list project info by name')
    subparser_find.add_argument('name', nargs='?', type=str)

    args = parser.parse_args(argv[1:])
    return args



def main():  
    args = parse_argv(sys.argv)
    command = args.command
    if command is None:
        return
    pm = AWProjectManager(PATH.data/'awpm')
    if command == 'add':
        project_root = Path(args.project_root)
        project_info = get_project_info_from_project_root(project_root)
        res = pm.add_project(project_info)
        if res:
            print(f'add project: {project_info.name}')
        else:
            print(f'fail to add project: {project_info.name}')
            exit(1)
    elif command == 'del':
        if args.id is not None:
            proj_id = args.id
            res = pm.del_project(base64.urlsafe_b64decode(proj_id))
            if res:
                print(f'remove project: {proj_id}')
            else:
                print(f'fail to remove project: {proj_id}')
                exit(1)
        elif args.name is not None:
            proj_name = args.name
            raise NotImplementedError
    elif command == 'list':
        name = args.name
        if name is None:
            res = list(pm.iter_project_info())
            for info in res:
                print(info.to_json())
        else:
            res = pm.list_project_info_by_name(name)
            for info in res:
                print(info.to_json())

    
main()

