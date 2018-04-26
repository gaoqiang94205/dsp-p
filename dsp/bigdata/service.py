# -*- coding:utf-8 -*-
import os.path
import pytest
from compose.cli.main import TopLevelCommand, project_from_options

# @pytest.fixture(scope='session')
# def docker_compose(request):
#     """
#     :type request: _pytest.python.FixtureRequest
#     """
#     options = {"--no-deps": False,
#                "--abort-on-container-exit": False,
#                "SERVICE": "",
#                "--remove-orphans": False,
#                "--no-recreate": True,
#                "--force-recreate": False,
#                "--build": False,
#                '--no-build': False,
#                '--no-color': False,
#                "--rmi": "none",
#                "--volumes": "",
#                "--follow": False,
#                "--timestamps": False,
#                "--tail": "all",
#                "-d": True,
#                }
#
#     project = project_from_options(os.path.dirname(__file__), options)
#     cmd = TopLevelCommand(project)
#     cmd.up(options)
#
#     def fin():
#         cmd.logs(options)
#         cmd.down(options)
#
#     request.addfinalizer(fin)
from dsp.utils.docker_stack import compose_up


def init_hadoop(slaves):
    options = { "--no-deps":False,
                "--always-recreate-deps":False,
               "--abort-on-container-exit": False,
               "SERVICE": "",
               "--remove-orphans": False,
               "--no-recreate": True,
               "--force-recreate": False,
               "--build": False,
               '--no-build': False,
               '--no-color': False,
               "--rmi": "none",
               "--volumes": "",
               "--follow": False,
               "--timestamps": False,
               "--tail": "all",
               "-d": True,
                "--scale":{'master=1'}
               }

    project = project_from_options(os.path.dirname(__file__), options)
    cmd = TopLevelCommand(project)
    cmd.up(options)

def hadoop_up(compose_yml):
    compose_up(compose_yml);
    return '初始化成功'

if __name__=='__main__':
    hadoop_up('./docker-compose.yaml')