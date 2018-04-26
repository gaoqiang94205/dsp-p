import subprocess

import os

def  stack(compose):
    print 'docker stack deply --compose-file '+compose + 'test'
    subprocess.check_call('docker stack deploy --compose-file '+compose + ' test',shell=True)

def compose_up(compose):
    subprocess.check_call('docker-compose -f '+compose+' up -d', shell=True)

if __name__=='__main__':
    #stack('./docker-compose.yml')
    path =  os.path.abspath('./docker-compose111.yml')
