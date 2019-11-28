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
        # dts shutdown [duckiebot name]

        # params
        hostname = args[0]

        client = check_docker_environment()
        container_name = "duckie_base_%s" % hostname
        remove_if_running(client, container_name)


