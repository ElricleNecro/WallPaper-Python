# -*- coding: utf-8 -*-

"""Wallpaper class.
"""

import shlex

import os
import re
import sys
import random as rd
import subprocess as sb

from .Daemon import Daemon
from .utils import search_file, get_output


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

        self._motif = motif
        self._recurse = recurse

        if directory is not None:
            self._directory = directory
            self._prog = "feh"

        self._opt = "--bg-scale"
        self._time = Time
        self._dual = False
        self._environment = os.environ.copy()
        self._list_file = None

    @property
    def cmd(self):
        """Programme à utiliser pour afficher l'image en fond d'écran."""
        return self._prog

    @cmd.setter
    def cmd(self, prog):
        self._prog = prog

    @cmd.deleter
    def cmd(self):
        self._prog = "feh"

    @property
    def directory(self):
        """Répertoire où trouver les images."""
        return self._directory

    @directory.setter
    def directory(self, directory):
        self._directory = directory

    @directory.deleter
    def directory(self):
        self._directory = None

    @property
    def opt(self):
        """Option du programme."""
        return self._opt

    @opt.setter
    def opt(self, opt):
        self._opt = opt

    @opt.deleter
    def opt(self):
        self._opt = "--bg-scale"

    @property
    def time(self):
        """Temps entre chaque changement de fond d'écran (mode démon uniquement)."""
        return self._time

    @time.setter
    def time(self, time):
        self._time = time

    @time.deleter
    def time(self):
        self._time = None

    @property
    def dual(self):
        """Multi-écran ou non."""
        return self._dual

    @dual.setter
    def dual(self, val):
        if isinstance(val, bool):
            self._dual = len(
                re.findall(
                    r"(\d):",
                    get_output("xrandr --listmonitors")[0].decode("utf-8")
                )
            )
        elif isinstance(val, int):
            self._dual = val

    @dual.deleter
    def dual(self):
        self._dual = False

    @property
    def file(self):
        """Return a list of files inside the directory self.directory.
        """
        return self._search_file()

    def _gen_wall(self):
        tmp = self.file
        res = list()

        for _ in range(self.dual):
            res.append(tmp[rd.randint(0, len(tmp) - 1)])

        return res

    def __call__(self):
        cmd = "{prog} {options} {files}".format(
            prog=self._prog,
            options=self._opt,
            files=" ".join([str(i) for i in self._gen_wall()])
        )

        print("Commande : ", cmd)
        make = sb.Popen(
            shlex.split(cmd),
            stdout=sb.PIPE,
            stderr=sb.PIPE,
            env=self._environment,
        )

        #  out, err = make.communicate()
        #  out = out.decode("utf-8").split('\n')
        #  err = err.decode("utf-8").split('\n')
        #  sys.stderr.write(err)
        #  sys.stdout.write(out)
        #  print(err)

    def _search_file(self):
        if self.directory is not None:
            return search_file(
                self._motif,
                pdir=self.directory,
                recurse=self._recurse)
        return [""]

    def run(self):
        from time import sleep
        while True:
            self()
            sleep(self.time)
