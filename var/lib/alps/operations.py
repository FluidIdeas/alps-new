#!/usr/bin/env python3

import sys
sys.path.append('/var/lib/alps')
from misc import script_path
from console import begin_install
import subprocess
from misc import script_path
from misc import abnormal_exit
from misc import execute_cmd
import shlex
import deps
import console
import os
import misc

def install_pkg(pkg_name, config):
	try:
		dep_chain = deps.dep_chain_status(misc.list_for_item(pkg_name), False, config)
		console.print_status(dep_chain)
		if not ('-ni' in opts or '--no-interactive' in opts):
			response = console.prompt_choice('Are you sure you want to install these packages?', ['y', 'n'], 'y')
		else:
			response = 'y'
		if response == 'y':
			for (pkg, status) in dep_chain.items():
				if not status:
					begin_install(script_path(pkg, config))
					execute_cmd(script_path(pkg, config).split())
	except KeyboardInterrupt:
		abnormal_exit()

def install_pkgs(pkg_names, opts, config):
	try:
		dep_chain = deps.dep_chain_status(pkg_names, False, config)
		console.print_status(dep_chain)
		if not ('-ni' in opts or '--no-interactive' in opts):
			response = console.prompt_choice('Are you sure you want to install these packages?', ['y', 'n'], 'y')
		else:
			response = 'y'
		if response == 'y':
			for (pkg, status) in dep_chain.items():
				if not status:
					begin_install(script_path(pkg, config))
					execute_cmd(script_path(pkg, config).split())
	except KeyboardInterrupt:
		abnormal_exit()

def execute_script(script_path, params=None):
	try:
		if params != None:
			execute_cmd(script_path.split().extend(params))
		else:
			execute_cmd(script_path.split())
	except KeyboardInterrupt:
		abnormal_exit()

def update_scripts(config):
	execute_script(config['LIB'] + 'updatescripts.sh')
	generate_package_list()

def self_update(config):
	execute_script(config['LIB'] + 'selfupdate.sh')

def url_install(url, config):
	params = list()
	params.append
	execute_script(config['LIB'] + 'urlinstall.sh', misc.list_for_item(url))

def src_install(tarball_path, config):
	execute_script(config['LIB'] + 'srcinstall.sh', misc.list_for_item(tarball_path))

def list_installed(config):
	print()
	heading = '%-30s%-15s%-30s' % ('Package Name', 'Version', 'Installation Date')
	print(heading)
	pkgs = load_installed_pkgs(config)
	pkg_versions = load_installed_versions(config)
	pkg_names = list()
	for (name, date) in pkgs.items():
		try:
			# pkg_names.append(name + ' (' + date + ', ' + pkg_versions[name] + ') ')
			line = '%-30s%-15s%-30s' % (name, pkg_versions[name], date)
			pkg_names.append(line)
		except KeyError:
			pass
	print()
	print('\n'.join(pkg_names))
	print()

def get_updates(config):
	updateable = list()
	with open(config['VERSION_LIST']) as f:
		installed_versions = f.readlines()
	for installed_version in installed_versions:
		parts = line.split(':')
		script_name = parts[0]
		version = parts[1]
		available_version = script_version(script_name)
		if available_version > version:
			updateable.append(script_name)
	return updateable

def script_version(script_name):
	with open(script_path(script_name, config)) as f:
		for line in f:
			if line.startswith('VERSION='):
				return line[8:].strip()

def load_installed_versions(config):
	with open(config['VERSION_LIST']) as f:
		lines = f.readlines()
	versions = dict()
	for line in lines:
		parts = line.split(':')
		try:
			versions[parts[0]] = parts[1].strip()
		except KeyError:
			pass
	return versions

def load_installed_pkgs(config):
	with open(config['INSTALLED_LIST']) as f:
		lines = f.readlines()
	pkgs = dict()
	for line in lines:
		parts = line.split('=')
		try:
			pkgs[parts[0]] = parts[1][1:].strip()
		except KeyError:
			pass
	return pkgs

def update(config):
	pass

def generate_package_list():
	packages_list_file = '/var/cache/alps/packages.json'
	packages = list()
	try:
		with open(packages_list_file, 'r') as fp
			packages = json.load(fp)
	except IOError:
		pass

	scripts_dir = '/var/cache/alps/scripts'
	scripts = os.listdir(scripts_dir)
	for script in scripts:
		with open(scripts_dir + '/' + script) as fp:
			package = parse_package(fp)
			update_package_details(package, packages)
	with open(packages_list_file, 'w') as fp:
		fp.write(json.dumps(packages))

def update_package_details(package, packages):
	pass

def parse_package(package_file):
	return None

def run_cmd(cmd, params_and_opts, config):
	if cmd == 'install':
		if len(params_and_opts[0]) < 3:
			console.install_not_enough_args_err_msg()
			abnormal_exit()
		install_pkgs(params_and_opts[0][2:], params_and_opts[1], config)
	elif cmd == 'updatescripts':
		update_scripts(config)
	elif cmd == 'selfupdate':
		self_update(config)
	elif cmd == 'listinstalled':
		list_installed(config)


