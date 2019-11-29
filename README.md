[![CircleCI](https://circleci.com/gh/duckietown/duckietown-shell-commands.svg?style=shield)](https://circleci.com/gh/duckietown/duckietown-shell-commands)

# duckietown-shell-commands

Commands for the Duckietown Shell

Usage custom commands:

- dts keyboard 'duckiename'
	-> launch keyboard teleop
- dts base 'duckiename' 'python script path' 
	-> launch base container with python script
- dts shutdown 'duckiename'
	-> shutdown base container
- dts start_logging 'duckiename'
	-> init logging script & container
- dts stop_logging 'duckiename'
	-> stop logging script & zipping log files
