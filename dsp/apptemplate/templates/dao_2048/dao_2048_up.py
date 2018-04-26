import os.path
from compose.cli.main import TopLevelCommand, project_from_options

def dao_2048(service_name, config_file):
    options = { "--no-deps":False,
                "--always-recreate-deps":False,
               "--abort-on-container-exit": False,
               "SERVICE": service_name,
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
                "--scale": {'master=1'},
                "--file": config_file
               }

    project = project_from_options(os.path.dirname(__file__), options)
    cmd = TopLevelCommand(project)
    cmd.up(options)

if __name__=='__main__':
    path = os.path.abspath('./docker-compose.yml')
    print path
    dao_2048(service_name='my-2048',config_file=path)

    print os.path.dirname(__file__)