
import kivy
kivy.require('1.11.1')

from kivy import Config
import os
import platform

if platform.system() == 'Windows':

    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
    Config.set('graphics', 'multisamples', '0')

if platform.system() == 'Linux':

    os.environ['KIVY_VIDEO'] = 'ffpyplayer'

#Config.set('graphics', 'window_state', 'maximized')
#Config.set('graphics', 'resizable', True)
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 600)

import sqlite3
import PyPrincipal
from kivy.app import App

try:
    os.mkdir(os.path.expanduser(
        "~/Sistema Gestao Escolar"))
    os.mkdir(os.path.expanduser(
        "~/Sistema Gestao Escolar/Arquivo Passivo"))
except:
    pass

def cria_basedados(path):

    conexao = sqlite3.connect(path)
    cursor = conexao.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS ARQUIVOPASS(
        IDARQPASS   INTEGER PRIMARY KEY,
        NOME        TEXT    COLLATE NOCASE,
        DURACAO     TEXT    COLLATE NOCASE,
        MEDICAMENTO TEXT    COLLATE NOCASE,
        DOSAGEM     TEXT    COLLATE NOCASE,
        MG          TEXT    COLLATE NOCASE,
        IST         TEXT    COLLATE NOCASE,
        DIABETE     TEXT    COLLATE NOCASE,
        GRUPO       TEXT    COLLATE NOCASE,
        NUMGRUPO    INTEGER,
        NUM_NO_GRUPO INTEGER
        )
        ''')

    conexao.close()

db_path = os.path.expanduser(
    "~/Sistema Gestao Escolar/Arquivo Passivo/BDArquivoPassivo.db")

cria_basedados(db_path)

class Main(App):

    title = 'Arquivo Passivo'
    icon = 'Images/IconPng.png'

    def build(self):
        return PyPrincipal.Principal()


Main().run()
