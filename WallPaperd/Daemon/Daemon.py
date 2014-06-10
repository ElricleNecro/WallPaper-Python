#! /usr/bin/env python3
# -*- coding:Utf8 -*-

import os, sys, atexit, time, signal

class Daemon:
	def __init__(self, pidfile):
		e, f = os.path.split(pidfile)
		if not (os.access(e, os.R_OK) and os.access(e, os.W_OK)):
			sys.stderr.write("Vous n'avez pas les droits sur : " + e + "\n")
			sys.exit(1)

		self.pidfile = pidfile

	def daemonize(self):
		"""Méthode du double fork"""
		try:
			pid = os.fork()
			# Si c'est le père, on quitte
			if pid > 0:
				sys.exit(0)
		except OSError as err:
			sys.stderr.write("Le fork #1 a échoué :{0}\n".format(err))
			sys.exit(1)

		# On se découpe de l'environnement du parent
		os.chdir('/')
		# setsid crée une nouvelle session pour rendre le processus fils indépendant
		os.setsid()
		os.umask(0)

		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError as err:
			sys.stderr.write("Le fork #2 a échoué :{0}\n".format(err))
			sys.exit(1)

		# On vide les tampons
		sys.stdout.flush()
		sys.stderr.flush()

		si = open(os.devnull, 'r')
		so = open(os.devnull, 'a+')
		se = open(os.devnull, 'a+')

		# Redirection des file descriptor standard
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())

		# On enregistre la méthode delpid() qui sera exécutée à la fermeture du programme
		atexit.register(self.delpid)

		# On récupère le PID du processus
		pid = str(os.getpid())
		# On écrit le PID dans le fichier définit dans pidfile
		with open(self.pidfile,'w+') as f:
			f.write(pid + '\n')

	# Méthode qui permet de supprimer le fichier dans lequel on écrit le PID
	def delpid(self):
		os.remove(self.pidfile)

	# Méthode qui permet de démarrer le daemon
	def start(self):
		"""Démarrage du daemon."""

		# On chercher si le fichier pidfile existe afin de savoir si un daemon s'exécute déjà
		try:
			with open(self.pidfile,'r') as pf:
				pid = int(pf.read().strip())
		except IOError:
			pid = None

		# Si un processus existe déjà
		if pid:
			message = "pidfile {0} existe déjà. Y a-t-il un daemon qui fonctionne ?\n"
			sys.stderr.write(message.format(self.pidfile))
			sys.exit(1)

		# On lance le double fork
		self.daemonize()
		# On démarre la boucle principale
		self.run()

	def stop(self):
		"""Arrêter le daemon."""

		# On récupère le PID du daemon
		try:
			with open(self.pidfile,'r') as pf:
				pid = int(pf.read().strip())
		except IOError:
			pid = None

		# Si le PID n'est pas défini
		if not pid:
			message = "pidfile {0} n'existe pas. Le daemon ne fonctionne pas ?\n"
			sys.stderr.write(message.format(self.pidfile))
			return # not an error in a restart

		# On essaie de d'arrêter le daemon
		try:
			# Tant que le processus n'est pas tuer, on boucle
			while 1:
				os.kill(pid, signal.SIGTERM)
				# On attend pour éviter trop de consommation du CPU
				time.sleep(0.1)
		except OSError as err:
			e = str(err.args)
			if e.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print(str(err.args))
				sys.exit(1)

	def restart(self):
		"""Redémarrage du daemon."""
		self.stop()
		self.start()

	def run(self):
		raise NotImplementedError
