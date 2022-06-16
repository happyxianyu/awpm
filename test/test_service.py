import random
import mimesis
import copy

from awpm import *
from awpm.db.service import *
from awpm.db import *

from .common import *
from .helper import *




def test_service():
    N = 97 # test cases

    data_path = PATH.tmp/'test/service'
    data_path.remove()
    data_path.mkdir()
    service_mngr = AWDBServiceMngr(data_path/'dbservice', enable_debug=False)
    service = service_mngr.project_install_info_service

    fake_info_list = list(generate_fake_project_install_info(N))
    proj_ids = [proj.id for proj in fake_info_list]
    # logger.info(proj_ids)

    # test add
    with log_perf('test add'):
        for info in fake_info_list:
            service.add_project_info(info)

    # test iter project info
    queried_infos = list(service.iter_project_info())
    assert len(queried_infos) == len(fake_info_list)

    # test query
    for id_ in proj_ids:
        info = service.get_project_info(id_)
        assert info is not None

    # test add duplicates
    for _ in range(10):
        info = random.choice(fake_info_list)
        info = copy.deepcopy(info)
        # edit name
        info.name = mimesis.Food().drink()
        service.add_project_info(info)
        queried_info = service.get_project_info(info.id)
        assert queried_info.name == info.name


    # test iter specified fields
    fields = service.project_install_info_fields
    l = list(service.iter_fields_of_project_info([fields.project_root, fields.export_paths]))

    # test deletion
    for id_ in proj_ids:
        service.del_project_info(id_)
        assert service.get_project_info(id_) is None



