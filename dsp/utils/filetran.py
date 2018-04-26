from dsp.utils.dsp_docker_client import DockerHeavyClient

base_url='http+unix://var/run/docker.sock'

def file_trans(from_id,from_path,to_id,to_path):
   docker_hd = DockerHeavyClient(base_url)
   c_from = docker_hd.containers.get(from_id)
   c_to = docker_hd.containers.get(to_id)
