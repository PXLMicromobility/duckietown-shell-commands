import argparse
import os
import platform
import subprocess
import shlex
import socket
import docker
from dt_shell import DTCommandAbs, dtslogger
from utils.networking_utils import get_duckiebot_ip
from dt_shell.env_checks import check_docker_environment
from utils.docker_utils import remove_if_running
from utils.cli_utils import start_command_in_subprocess


class DTCommand(DTCommandAbs):

    @staticmethod
    def command(shell, args):
        # dts stop_logging [duckiebot name]

        # params
        hostname = args[0]

        image = 'pxlmicromobility/duckiebot-base:latest'
        duckiebot_ip = get_duckiebot_ip(duckiebot_name= hostname)
        network_mode = 'host'
        sim = False

        if sim:
            duckiebot_ip = "sim"

        run_gui_controller(hostname, image, network_mode, duckiebot_ip)


def run_gui_controller(hostname, image, network_mode, duckiebot_ip):
    client = check_docker_environment()
    container_name = "duckie_copier_%s" % hostname
    remove_if_running(client, container_name2)

    env = {'HOSTNAME': hostname,
           'ROS_MASTER': hostname,
           'VEHICLE_NAME': hostname,
           'ROS_MASTER_URI': 'http://%s:11311' % duckiebot_ip}

    env['QT_X11_NO_MITSHM'] = 1

    volumes = {}

    subprocess.call(["xhost", "+"])

    env['DISPLAY'] = os.environ['DISPLAY']

    # cmd = "python misc/code/{path}.py %s" % hostname

    # subprocess.call(['./helper.sh'])
    cmd = "python misc/code/logging/copy_logs.py %s" % get_ip()
    

    params = {'image': image,
              'name': container_name,
              'network_mode': network_mode,
              'environment': env,
              'privileged': True,
              'stdin_open': True,
              'tty': True,
              'command': cmd,
              'detach': True,
              'volumes': volumes
              }

    container = client.containers.run(**params)
    cmd = 'docker attach %s' % container_name
    start_command_in_subprocess(cmd)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



