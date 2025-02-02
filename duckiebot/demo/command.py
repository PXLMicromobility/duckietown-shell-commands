import argparse
import docker

from dt_shell import DTCommandAbs, dtslogger
from dt_shell.env_checks import check_docker_environment
from utils.cli_utils import start_command_in_subprocess
from utils.docker_utils import default_env, bind_duckiebot_data_dir, remove_if_running
from utils.networking_utils import get_duckiebot_ip

usage = """

## Basic usage

    Runs a demo on the Duckiebot. Effectively, this is a wrapper around roslaunch. You
    can specify a docker image, ros package and launch file to be started. A demo is a 
    launch file specified by `--demo_name`. The argument `--package_name` specifies 
    the package where the launch file should is located (by default assumes `duckietown`).
    
    To find out more, use `dts duckiebot demo -h`.

        $ dts duckiebot demo --demo_name [DEMO_NAME] --duckiebot_name [DUCKIEBOT_NAME]

"""
class InvalidUserInput(Exception):
    pass

class DTCommand(DTCommandAbs):

    @staticmethod
    def command(shell, args):
        prog = 'dts duckiebot demo'
        parser = argparse.ArgumentParser(prog=prog, usage=usage)

        parser.add_argument('--demo_name', '-d', dest="demo_name", default=None,
                            help="Name of the demo to run")

        parser.add_argument('--duckiebot_name', '-b', dest="duckiebot_name", default=None,
                            help="Name of the Duckiebot on which to run the demo")

        parser.add_argument('--package_name', '-p', dest="package_name", default="duckietown",
                            help="You can specify the package that you want to use to look for launch files")

        parser.add_argument('--image', '-i', dest="image_to_run",
                           default="duckietown/rpi-duckiebot-base:master19",
                           help="Docker image to use, you probably don't need to change ",)

        parser.add_argument('--debug', '-g', dest="debug", action='store_true', default=False,
                            help="will enter you into the running container")

        parsed = parser.parse_args(args)

        check_docker_environment()
        demo_name = parsed.demo_name
        if demo_name is None:
            msg = 'You must specify a demo_name'
            raise InvalidUserInput(msg)

        duckiebot_name=parsed.duckiebot_name
        if duckiebot_name is None:
            msg = 'You must specify a duckiebot_name'
            raise InvalidUserInput(msg)


        package_name=parsed.package_name
        dtslogger.info("Using package %s" % package_name)

        duckiebot_ip = get_duckiebot_ip(duckiebot_name)
        duckiebot_client = docker.DockerClient('tcp://' + duckiebot_ip + ':2375')

        container_name='demo_%s' % demo_name
        remove_if_running(duckiebot_client, container_name)
        image_base=parsed.image_to_run
        env_vars = default_env(duckiebot_name,duckiebot_ip)
        env_vars.update({'VEHICLE_NAME':duckiebot_name})

        if demo_name == 'base':
            cmd = '/bin/bash'
        else:
            cmd = 'roslaunch %s %s.launch veh:=%s' % (package_name, demo_name, duckiebot_name)

        dtslogger.info("Running command %s" % cmd)
        demo_container = duckiebot_client.containers.run(image=image_base,
                                        command= cmd,
                                        network_mode='host',
                                        volumes=bind_duckiebot_data_dir(),
                                        privileged=True,
                                        name=container_name,
                                        mem_limit='800m',
                                        memswap_limit='2800m',
                                        stdin_open=True,
                                        tty=True,
                                        detach=True,
                                        environment=env_vars)

        if demo_name == 'base' or parsed.debug:
            attach_cmd = 'docker -H %s.local attach %s' % (duckiebot_name, container_name)
            start_command_in_subprocess(attach_cmd)

