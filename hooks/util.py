#!/usr/bin/env python
"""
Shared pygithooks utils.
"""

import shlex
import subprocess

def run_command(command, shell=False):
    command_subprocess = subprocess.Popen(shlex.split(command),
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          shell=shell)
    command_out, command_err = command_subprocess.communicate()
    return_code = command_subprocess.returncode
    return command_out, command_err, return_code

def get_config(config_key, as_bool=False, default=None):
    """
    Retrieves the value of pygithooks.<config_key> from git config, optionally forcing to be boolean.
    """
    git_config_command = "git config --null {bool_flag} --get pygithooks.{config_key}".format(config_key=config_key,
                                                                                              bool_flag="--bool" if as_bool else "")
    git_out, git_err, git_rc = run_command(git_config_command)

    if git_err or not git_out or git_rc:
        return default

    null_index = git_out.find(chr(0))
    if null_index < 0:
        return default

    config_val = git_out[:null_index]

    if as_bool:
        return config_val == "true"
    else:
        return config_val
