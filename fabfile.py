from fabric.api import run, sudo, cd, abort, settings, env

env.hosts = ['ubuntu@ws01.josephgilley.com']
env.key_filename = '/Users/joma/.ssh/aws-ec2-01'

project_path = '/home/ubuntu/foodtruck'
load_data_script = '\\copy foodtruck(location_id, applicant, facility_type, cnn, location_description, address, blocklot, block, lot, permit, status, food_items, x, y, latitude, longitude, schedule_url, noi_sent_on, approved_at, received_at, prior_permit, expires_on) from \'{project_path}/foodtrucks_raw.csv\' DELIMITERS \',\' CSV HEADER;'.format(project_path=project_path)
uwsgi_log_path = '/var/log/uwsgi'

def shove():
  if has_package('git'):
    if not has_directory(project_path):
      if run('git clone https://github.com/joegilley/foodtruck-o-matic.git foodtruck').failed:
        abort('git cloning failed')
    with cd(project_path):
      if run('git pull').failed:
        abort('shoving git failed')

def init():

  safe_install_package('git')

  if not has_directory(project_path):
    if run('git clone https://github.com/joegilley/foodtruck-o-matic.git foodtruck').failed:
      abort('git cloning failed')

  with cd(project_path):
    if run('git pull').failed:
      abort('git pulling failed')

    safe_install_package('build-essential')
    safe_install_package('uwsgi')
    safe_install_package('python-pip')
    safe_install_package('python-virtualenv')
    safe_install_package('libpq-dev')
    safe_install_package('libyaml')
    safe_install_package('postgresql')
    safe_install_package('postgresql-contrib')
    safe_install_package('postgresql-9.3-postgis-2.1')
    safe_install_package('postgis')
    safe_install_package('python-dev')

    with settings(warn_only=True):
      if run('virtualenv .').failed:
        abort('could not create virtualenv')

      if run('source bin/activate && pip install -qr requirements.txt').failed:
        abort('could not activate and install virutalenv')

      if run('psql postgres -tAc "select 1 from pg_roles where rolname=\'{}\'" | grep -q 1'.format('ubuntu')).failed:
        sudo('createuser ubuntu', user='postgres')

      if not run('psql -l | grep -qw foodtruck').failed:
        sudo('dropdb foodtruck', user='postgres')
      sudo('createdb foodtruck', user='postgres')

      sudo('psql -c "CREATE EXTENSION postgis;" foodtruck', user='postgres')

      run('source bin/activate && python manage.py db upgrade')

      if run('psql -c "{};" foodtruck'.format(load_data_script)).failed:
        abort('failed to load data')

      if not has_directory(uwsgi_log_path):
        sudo('mkdir -p {}'.format(uwsgi_log_path))
      sudo('chown -R ubuntu:ubuntu {}'.format(uwsgi_log_path))

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
