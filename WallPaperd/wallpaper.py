# -*- coding: utf-8 -*-

"""Wallpaper class.
"""

import shlex

import os
import sys
import random as rd
import subprocess as sb

from .Daemon import Daemon
from .utils import search_file


class WallPaper(Daemon):
    """Gère les fond d'écran.
    """

    def __init__(
            self,
            directory,
            motif=".*",
            recurse=True,
            Time=None,
            pidfile="/tmp/pid.wallpaper"):
        super().__init__(pidfile)
        self.motif = motif
        self.recurse = True
        if directory is not None:
            self.directory = directory
            self.prog = "feh"
        self.opt = "--bg-scale"
        self.time = Time
        self.dual = False
        self.environment = os.environ.copy()
        self._list_file = None

    def Set_cmd(self, prog):
        self.prog = prog

    def Get_cmd(self):
        return self.prog

    def Del_cmd(self):
        self.prog = "feh"

    def Set_directory(self, directory):
        self.directory = directory

    def Get_directory(self):
        return self.directory

    def Del_directory(self):
        self.directory = None

    def Set_opt(self, opt):
        self.opt = opt

    def Get_opt(self):
        return self.opt

    def Del_opt(self):
        self.opt = "--bg-scale"

    def Get_Time(self):
        return self.time

    def Set_Time(self, Time):
        self.time = Time

    def Del_Time(self):
        self.time = None

    def Get_Dual(self):
        return self.dual

    def Set_Dual(self, val):
        if isinstance(val, bool):
            self.dual = val
        else:
            raise TypeError(
                "Mauvais type donnée. Attendu : " +
                type(
                    self.dual) +
                ", Reçu : " +
                type(val))

    def Del_Dual(self):
        self.dual = False

    def __call__(self):
        self._list_file = self._search_file()
        file = self._list_file[rd.randint(0, len(self._list_file)-1)]
        cmd = self.prog + " " + self.opt + " " + '"' + file + '"'
        if self.dual:
            cmd += " " + '"' + \
                self._list_file[rd.randint(0, len(self._list_file)-1)] + '"'
        print("Commande : ", cmd)
        make = sb.Popen(
            shlex.split(cmd),
            stdout=sb.PIPE,
            stderr=sb.PIPE,
            env=self.environment,
        )
        out, err = make.communicate()
        out = out.decode("utf-8").split('\n')
        err = err.decode("utf-8").split('\n')
        sys.stderr.write(err)
        sys.stdout.write(out)
        print(err)

    def _search_file(self):
        if self.directory is not None:
            return search_file(
                self.motif,
                pdir=self.directory,
                recurse=self.recurse)
        return [""]

    def run(self):
        from time import sleep
        while True:
            self._list_file = self._search_file()
            file = self._list_file[rd.randint(0, len(self._list_file)-1)]
            cmd = self.prog + " " + self.opt + " " + '"' + file + '"'
            if self.dual:
                cmd += " " + '"' + \
                    self._list_file[rd.randint(0, len(self._list_file)-1)] + '"'
            sb.Popen(shlex.split(cmd), stdout=sb.PIPE, stderr=sb.PIPE)
            sleep(self.Time)

    Directory = property(
        Get_directory,
        Set_directory,
        Del_directory,
        doc="Répertoire où trouver les images.")
    Cmd = property(
        Get_cmd,
        Set_cmd,
        Del_cmd,
        doc="Programme à utiliser pour afficher l'image en fond d'écran.")
    Opt = property(Get_opt, Set_opt, Del_opt, doc="Option du programme.")
    Time = property(
        Get_Time,
        Set_Time,
        Del_Time,
        doc="Temps entre chaque changement de fond d'écran "
        "(mode démon uniquement).")
    Dual = property(Get_Dual, Set_Dual, Del_Dual, doc="Multi-écran ou non.")
