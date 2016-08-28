import os,re
from datetime import datetime
from fabric.api import *

env.user = 'ubuntu'
env.sudo_user = 'root'
env.hosts = ['52.35.100.220']

db_user='www-francis'
db_password='francis'

_TAR_FILE = 'dist-fon.tar.gz'
_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/crossroad'

def _current_path():
	return os.path.abspath('.')

def build():
	includes=['blog','crossroad','templates','*.py']
	excludes=['.*','*.pyc','*.pyo','test','.git','.gitignore','venv','migrations']
	local("rm -f dist/%s"% _TAR_FILE)
	with lcd(os.path.join(_current_path(),'crossroad')):
		cmd = ['sudo tar', '--dereference', '-czvf', 'dist/%s' % _TAR_FILE]
		cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
		cmd.extend(includes)
		local(' '.join(cmd))

def deploy():
	newdir = 'fon-%s'%datetime.now().strftime('%y-%m-%d_%H.%M.%S')
	#delete already exitng .tar
	run('rm -f %s'%_REMOTE_TMP_TAR)
	put('dist/%s'%_TAR_FILE,_REMOTE_TMP_TAR)
	with cd(_REMOTE_BASE_DIR):
		sudo('mkdir %s'%newdir)
	with cd ("%s/%s"%(_REMOTE_BASE_DIR,newdir)):
		sudo('tar -xzvf %s'%_REMOTE_TMP_TAR)
	with cd(_REMOTE_BASE_DIR):
		sudo('rm -rf blog')
		sudo('ln -s %s blog'%newdir)
		sudo('chown www-data:www-data blog')
		sudo('chown -R www-data:www-data %s'%newdir)

	with settings(warn_only=True):
		sudo('supervisorctl stop webapp')
		sudo('supervisorctl start webapp')
		sudo('/etc/init.d/nginx reload')
