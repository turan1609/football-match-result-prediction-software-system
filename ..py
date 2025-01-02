from PyQt5 import uic

with open('football.py', 'w', encoding="utf-8") as fout:
    uic.compileUi('football.ui', fout)