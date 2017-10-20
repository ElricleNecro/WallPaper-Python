# -*- coding: utf-8 -*-

"""Utilitary module for utilitary function.
"""

import os
import re


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
