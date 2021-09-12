#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import fileinput
import platform

if platform.system()== "Windows":
	py="py"
else:
	py="python3"
arguments = len(sys.argv) - 1

if arguments >= 1 :
	project_path=os.path.join(os.getcwd(), sys.argv[1])


def create_project(name_project):
	cProject= subprocess.run(["django-admin", "startproject", name_project])
	if cProject.returncode != 0:
		quit()
	os.chdir(project_path)
	

def create_app(name_app):
	cApp=subprocess.run([py, "manage.py", "startapp", name_app])
	if cApp.returncode != 0:
		quit()
	os.chdir(os.path.join(project_path, name_app))
	with open("urls.py","w", encoding="utf-8") as url:
		data=f"from django.urls import path\nfrom . import views\n\nurlpatterns = [\n\t#path('', views.index, name='index'),\n]"
		url.write(data)
	url.close()
	os.mkdir('templates')
	os.chdir(project_path)
	

def setup_settings(name_project):
	data=""
	apps=False
	if arguments >=2:
		apps=True
	with fileinput.FileInput(os.path.join(name_project, "settings.py"),inplace=True) as settings:
		for line in settings:
			if line.startswith("SECRET_KEY = "):
				data=line.split("'")[1]
				line=f"with open('sk') as f:\n\tSECRET_KEY=f.read().strip()\n"
			if line.startswith("LANGUAGE_CODE = "):
				line="LANGUAGE_CODE = 'es'\n"
			if line.startswith("TIME_ZONE = "):
				line="TIME_ZONE = 'America/Santiago'\n"
			if apps and line.startswith("INSTALLED_APPS = ["):
				position=2
				line=f"INSTALLED_APPS = [\n"
				while arguments >= position:
					line+=f"\t'{sys.argv[position]}',\n"
					position+=1
				apps=False
			print(line, end="")
	settings.close()
	with open("sk","w", encoding="utf-8") as sk:
		sk.write(data)
	sk.close()
	with open(".gitignore", "w", encoding="utf-8") as git:
		git.write(f"**/__pycache__/\n**/migrations/\n*.sqlite3\nsk")
	git.close()


if arguments >= 2 :
	create_project(sys.argv[1])
	position=2
	while arguments >= position:
		create_app(sys.argv[position])
		position+=1
	setup_settings(sys.argv[1])
elif arguments==1 :
	create_project(sys.argv[1])
	setup_settings(sys.argv[1])

