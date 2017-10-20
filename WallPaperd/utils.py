# -*- coding: utf-8 -*-

"""Utilitary module for utilitary function.
"""

import os
import re
import shlex
import subprocess as sb


def search_file(motif, pdir=".", recurse=False, exclude=None):
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
            res = res + search_file(motif, pdir=i, recurse=recurse)
            while [] in res:
                res.remove([])
        elif re.search(motif, i) is not None:
            if exclude is None or re.search(exclude, i) is None:
                res.append(i)
    return res


def get_output(cmd, env=None):
    """Execute a command and return it's stdout and stderr.
    """
    make = sb.Popen(shlex.split(cmd), stdout=sb.PIPE, stderr=sb.PIPE, env=env)
    return make.communicate()
