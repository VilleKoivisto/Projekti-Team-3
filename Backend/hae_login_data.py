""" Hakee kirjautumisdatan """

import os

def hae_data():
    koti = os.path.expanduser('~')

    with open(f"{koti}/backendfolder/.emailsalaisuuksia","r") as f:
        lines2 = []
        lines = f.readlines()

        for i in range(len(lines)):
            lines2.append(lines[i].strip('\n'))

        return lines2[0], lines2[1], lines2[2], lines[3]