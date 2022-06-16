import mimesis
import random
import time
from contextlib import contextmanager

from awpm import *

from .common import logger


__all__ = ['generate_fake_project_install_info', 'log_perf']



@contextmanager
def log_perf(name=''):
    t0 = time.perf_counter_ns() * 1e-9
    yield
    t1 = time.perf_counter_ns() * 1e-9
    dt = t1-t0
    logger.info(f'Time of {name} consumed: {dt}')


def generate_fake_project_install_info(n=1):
    make_uuid = mimesis.Cryptographic().uuid
    make_name = mimesis.Business().company
    make_version = mimesis.Development().version
    make_proj_path = mimesis.Path().project_dir
    make_fruit = mimesis.Food().fruit

    def random_make_many(make, min_val, max_val):
        return [make() for _ in range(random.randint(min_val, max_val))]

    def random_make(make, rate=0.8):
        if random.random()<rate:
            return make()

    for _ in range(n):
        yield AWProjectInstallInfo(
                id = make_uuid().encode('utf8'),
                name= random_make(make_name),
                version = random_make(make_version),
                project_root= make_proj_path(),
                export_paths= random_make(lambda:random_make_many(make_fruit, 0, 10))
                )
