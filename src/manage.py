#!/usr/bin/env python

from os import path as p
import sys

import envvars as env


if __name__ == "__main__":
    env_file = p.normpath(p.join(p.abspath(p.dirname(__file__)), "../conf/env"))
    env.load(env_file)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
