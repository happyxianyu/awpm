from cbutil import Path
import os

from awpm import *

from .common import *
from .helper import *


def test_core():
    N = 17
    data_path = PATH.tmp/'test/core/data'
    data_path.remove()
    mngr = AWProjectManager(data_path)
    test_data_lst = list(generate_fake_project_install_info(N))
    proj_ids = [proj.id for proj in test_data_lst]
    logger.info(proj_ids)
    for data in test_data_lst:
        mngr.add_project(data)
    for id_ in proj_ids:
        info = mngr.get_project_info(id_)
        assert info is not None
    for id_ in proj_ids:
        mngr.del_project(id_)

    assert list(mngr.iter_project_info()) == []
    
        



