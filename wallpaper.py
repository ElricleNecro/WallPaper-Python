#! /usr/bin/env python3
# -*- coding:Utf8 -*-


import argparse as ag

from WallPaperd.wallpaper import WallPaper


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
