#! /usr/bin/env python3
# -*- coding:Utf8 -*-

import shlex

import os
import re
import sys
import random as rd
import argparse as ag
import subprocess as sb

from WallPaperd.Daemon import Daemon


def SearchFile(motif, pdir=".", recurse=False, exclude=None):
    """Cherche dans le répertoire courant (et dans les sous-répertoires, si
    recurse = True (False par défaut)) si un motif ou un dossier contient la
    chaîne "motif".

    motif           :: motif recherché.
    pdir    = "."   :: Répertoire parent à partir duquel rechercher.
    recurse = False :: récursif ou non (défaut : non récursif).
    """

    res = []

    for i in os.listdir(pdir):
        i = os.path.join(pdir, i)
        if recurse and os.path.isdir(i):
            # res.append(SearchFile(motif, pdir=i, recurse=recurse))
            res = res + SearchFile(motif, pdir=i, recurse=recurse)
            while [] in res:
                res.remove([])
        elif re.search(motif, i) is not None:
            if exclude is None or re.search(exclude, i) is None:
                res.append(i)
    return res


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
        self.List_File = self._search_file()
        file = self.List_File[rd.randint(0, len(self.List_File)-1)]
        cmd = self.prog + " " + self.opt + " " + '"' + file + '"'
        if self.dual:
            cmd += " " + '"' + \
                self.List_File[rd.randint(0, len(self.List_File)-1)] + '"'
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
            return SearchFile(
                self.motif,
                pdir=self.directory,
                recurse=self.recurse)
        return [""]

    def run(self):
        from time import sleep
        while True:
            self.List_File = self._search_file()
            file = self.List_File[rd.randint(0, len(self.List_File)-1)]
            cmd = self.prog + " " + self.opt + " " + '"' + file + '"'
            if self.dual:
                cmd += " " + '"' + \
                    self.List_File[rd.randint(0, len(self.List_File)-1)] + '"'
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


def main(args):
    if args.kill:
        import sys
        wall = WallPaper(None, pidfile=args.pidfile)
        wall.stop()
        sys.exit(0)
    if args.Directory is None:
        import sys
        print("Vous devez indiquez un dossier ou l'option -k")
        sys.exit(1)

    wall = WallPaper(args.Directory, args.expr, pidfile=args.pidfile)
    wall.Cmd = args.prog
    wall.Opt = args.opt

    if args.dual:
        wall.Dual = True

    if args.daemon:
        wall.Time = args.time
        if args.time is None:
            raise ValueError("Le temps de pause est invalide : None")

        wall.start()
    else:
        wall()

if __name__ == '__main__':
    parser = ag.ArgumentParser(
        formatter_class=ag.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "Directory",
        nargs='?',
        help="Répertoire contenant les images à mettre en fond d'écran.")
    parser.add_argument(
        "-E",
        "--expr",
        type=str,
        help="Motif (expression régulière) de sélection des images.",
        default=".*\.(png|jpg)$")
    parser.add_argument(
        "--opt",
        type=str,
        help="Options à passer au programme chargé de mettre le fond "
        "d'écran en place.",
        default="--bg-scale")
    parser.add_argument(
        "--prog",
        type=str,
        help="Programme mettant le place un fond d'écran.",
        default="feh")
    parser.add_argument(
        "--pidfile",
        type=str,
        help="Pidfile",
        default="/tmp/wallpaper.pid")
    parser.add_argument(
        "-d",
        "--daemon",
        help="Lancer le programme en tant que démon.",
        action='store_true')
    parser.add_argument(
        "-t",
        "--time",
        type=float,
        help="Temps entre chaque changement de fond d'écran.",
        default=120.0 *
        60.0)
    parser.add_argument(
        "-k",
        "--kill",
        help="Tue le daemon",
        action='store_true')
    parser.add_argument(
        "-m",
        "--dual",
        help="Multi-écran : un fond d'écran différent sur chaque écran.",
        action='store_true')

    main(parser.parse_args())
