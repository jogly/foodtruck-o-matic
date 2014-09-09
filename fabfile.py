from fabric.api import run, sudo, cd, abort, settings

def init(host):
  if host:
    env.hosts.append(host)

  project_path = '/home/ubuntu/foodtruck'

  if not has_package('git'):
    if sudo('apt-get install git').failed:
      abort('git install failed')

  if not has_directory(project_path):
    if run('git clone git@git://github.com/joegilley/foodtruck-o-matic.git foodtruck').failed:
      abort('git cloning failed')

  with cd(project_path):
    with settings(warn_only=True):
      if not has_package('python-pip'):
        if sudo('apt-get install python-pip').failed:
          abort('pip install failed')

      if not has_package('python-virtualenv'):
        if sudo('apt-get install python-virtualenv').failed:
          abort ('virtualenv install failed')

      if run('virtualenv .').failed:
        abort('could not create virtualenv')

      if run('source bin/activate').failed:
        abort('could not activate virutalenv')

      if run('pip install -r requirements.txt').failed:
        abort('pip could not install requirements')

def has_package(package):
  with settings(warn_only=True):
    return run('dpkg -l | grep -qw {}'.format(package)).failed

def has_directory(dir):
  with settings(warn_only=True):
    return run('test -d {}'. format(dir)).failed
