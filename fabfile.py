from fabric.api import run, sudo, cd, abort, settings, env

def init():

  project_path = '/home/ubuntu/foodtruck'

  if not has_package('git'):
    if sudo('apt-get install git').failed:
      abort('git install failed')

  if not has_directory(project_path):
    if run('git clone https://github.com/joegilley/foodtruck-o-matic.git foodtruck').failed:
      abort('git cloning failed')

  with cd(project_path):
    safe_install_package('python-pip')
    safe_install_package('python-virtualenv')
    safe_install_package('libpq-dev')
    safe_install_package('postgresql')
    safe_install_package('postgis')
    safe_install_package('python-dev')

    with settings(warn_only=True):
      if run('virtualenv .').failed:
        abort('could not create virtualenv')

      if run('source bin/activate && pip install -r requirements.txt').failed:
        abort('could not activate and install virutalenv')

def has_package(package):
  with settings(warn_only=True):
    return not run('dpkg -l | grep -qw {}'.format(package)).failed

def has_directory(dir):
  with settings(warn_only=True):
    return not run('test -d {}'. format(dir)).failed

def install_package(package):
  with settings(warn_only=True):
    return not sudo('apt-get -qq install {}'.format(package)).failed

def safe_install_package(package):
  with settings(warn_only=True):
    if not has_package(package):
      if not install_package(package):
        abort('could not install {}'.format(package))
