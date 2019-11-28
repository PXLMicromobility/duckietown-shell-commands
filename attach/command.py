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
        # dts base [duckiebot name] [python script]

        # ips van de duckiebots
        # greta_ip = '172.16.104.65'

        # params
        bot = args[0]
        path = args[1]

        if os.path.exists(path):
            print("File" + path +"exist")
        hostname = bot
        image = 'pxlmicromobility/duckiebot-base:latest'
        duckiebot_ip = get_duckiebot_ip(duckiebot_name= hostname)
        network_mode = 'host'
        sim = False

        if sim:
            duckiebot_ip = "sim"

        run_gui_controller(hostname, image, network_mode, path, duckiebot_ip)


def run_gui_controller(hostname, image, network_mode, path, duckiebot_ip):
    client = check_docker_environment()
    container_name = "duckie_base_%s" % hostname
    remove_if_running(client, container_name)

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
    if path == "virtualJoy":
        cmd = "python misc/virtualJoy/virtualJoy.py %s" % hostname
    else:
        cmd = "python misc/code" + os.path.basename(path)

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




