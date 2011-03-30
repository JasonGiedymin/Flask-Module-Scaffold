from __future__ import with_statement

import os
import sys
import  shutil

from fabric.api import *
from fabric.colors import blue as _blue, cyan as _cyan, green as _green, magenta as _magenta, red as _red, white as _white, yellow as _yellow
from fabric.contrib.project import rsync_project
from fabric.contrib import files, console
from fabric.contrib.console import confirm
from fabric import utils
from fabric.decorators import hosts


def _virtualenv(command, env_path=None):
    """ Run a command in the virtualenv. This prefixes the command with the source command.
    Usage:
        virtualenv('pip install django')
    """
    
    if env_path is None:
        abort(_red("You must provide the parameter 'env_path' to the virtualenv function"))

    source = 'source %s/bin/activate && ' % env_path

    print(source + command)
    local(source + command)

def staging_local():
    """ * setup staging environment on a local machine, relative to the project."""

    # Development Paths
    env.local_code_root = os.getcwd()

    #
    # We know that fab can only work with a fab file in the working directory.
    # We always want env to be on the same level as deploy.
    # Thus set up virtualenv in root.
    # This is hacky, works for now.
    #
    env.local_root_path_mod = "/../"
    env.local_root_path = env.local_code_root + env.local_root_path_mod
    env.local_virtual_env_path = os.path.join(env.local_root_path, "env")

    env.environment = 'local'

staging_local() # Always present.

def bootstrap_local():
    """ * initialize local virtualenv and pip install requirements. """
	
    require("local_virtual_env_path", provided_by=("staging_local"))
    create_virtualenv_local()
    update_requirements_local()

def create_virtualenv_local(virtual_env_path=env.local_virtual_env_path):
    """ * create a local virtualenv environment.
    Usage:
        create_virtual_local:path_to_env
        create_virtual_local
    Options:
        path_toenv: Optional. Will default to one directory up from fabfile named 'env'.
                    Effectively the path ['../'].
    """

    if not os.path.isdir(virtual_env_path):
        with settings(warn_only=True):
            result = local("virtualenv --no-site-packages --distribute %s" % virtual_env_path)
        if result.failed and not confirm(_white("Installing virtualenv failed. Continue anyway?"), default=False):
            abort(_red("Aborting local staging."))
    
    print(_green("Virtualenv installed and detected."))

def remove_virtualenv_local(virtual_env_path=env.local_virtual_env_path):
    """ * removes the local virtualenv environment, relative to the project.
    Usage:
        remove_localenv:path_to_env
        remove_localenv
    Options:
        path_to_env: Optional. Will default to one directory up from fabfile named 'env'.
                     Effectively the path ['../'].
    """

    #TODO need error catching
    if os.path.isdir(virtual_env_path):
        print("Removing %s" % virtual_env_path)
        shutil.rmtree(virtual_env_path)
    else:
        print(_red("Virtualenv not found [%s]." % virtual_env_path))

def start_dev_server():
    """ * start a local development server. 
    This will automatically activates virtualenv.
    """
    os.environ["MYAPP_DEBUG"]="TRUE"
    require('local_virtual_env_path', provided_by=('staging_local'))
    _virtualenv("python manage.py runserver", env.local_virtual_env_path)

def update_requirements_local():
    """ * update dependencies on local code base. """

    require("local_code_root", provided_by=("staging_local"))
    requirements = os.path.join(env.local_code_root, 'requirements')

    with cd(requirements):
        cmd = ['pip install']
        cmd += ['-E %(local_virtual_env_path)s' % env]
        cmd += ['--requirement %s' % os.path.join(requirements, 'requirements.txt')]
        local(' '.join(cmd))

