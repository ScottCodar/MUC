import sqlite3

import PyIntroDados
import PyPesquisa

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label



class Principal(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__()

        self.cont1 = 0
        self.cont2 = 0
        self.cont3 = 0

        self.widintrodados = PyIntroDados.WidIntroDados()
        self.widpesquisa = PyPesquisa.WidPesquisa()
        self.widrespesquisa = PyPesquisa.ResPesquisaWid()

        self.tipo_acao_principal = None


    def acao_principal(self, tipoacao):


        if self.cont1 == 1:

            self.remove_widget(self.widintrodados)
            self.cont1 = 0

        if self.cont2 == 1:

            self.remove_widget(self.widpesquisa)
            self.cont2 = 0

        if self.cont3 == 1:

            self.remove_widget(self.widrespesquisa)
            self.cont3 = 0

        if self.cont1 == 0:

            if tipoacao == 'Novo Registro':
                self.wid_intro_dados(tipoacao)

            else:
                self.wid_pesquisa(tipoacao)

            self.tipo_acao_principal = tipoacao


            # if tipoacao == 'Alterar Registro':
            #     self.wid_pesquisa(tipoacao)

            # if tipoacao == 'Apagar Registro':
            #     self.wid_pesquisa(tipoacao)

            # if tipoacao == 'Pesquisa':
            #     self.wid_pesquisa(tipoacao)


    def wid_intro_dados(self, tipowid):

        self.add_widget(self.widintrodados)
        self.widintrodados.ids.titulo_widintrodados.text = tipowid
        self.widintrodados.limpa_widintrodados()
        self.widintrodados.tipo_acao = tipowid
        self.cont1 = 1



    def wid_pesquisa(self, tipoacao):

        self.add_widget(self.widpesquisa)
        self.widintrodados.limpa_widintrodados()
        self.widpesquisa.limpa_widpesquisa()
        self.widpesquisa.ids.textopesquisa.text = tipoacao
        self.widpesquisa.tipo_acao_pesq = tipoacao
        
        self.cont2 = 1



    def opcoes_pesquisa(self, texto):

        if self.tipo_acao_principal != 'Pesquisa':
            self.open_wid_intro_dados(texto)

        if self.tipo_acao_principal == 'Pesquisa':
            self.open_wid_res_pesquisa(texto)

    

    def open_wid_intro_dados(self, nome):

        if self.cont1 == 1:

            self.widintrodados.limpa_widintrodados()
            self.remove_widget(self.widintrodados)

        self.add_widget(self.widintrodados)
        self.widintrodados.ids.titulo_widintrodados.text = self.widpesquisa.tipo_acao_pesq
        self.widintrodados.tipo_acao = self.widpesquisa.tipo_acao_pesq
        self.widintrodados.ids.btn_limpar.disabled = True
        self.widintrodados.inicio_alterar_dados(nome)

        self.cont1 = 1
        


    def close_wid(self):

        if self.cont1 == 1:
            self.widintrodados.limpa_widintrodados()
            self.remove_widget(self.widintrodados)
            self.cont1 = 0

        if self.cont3 == 1:
            self.remove_widget(self.widrespesquisa)
            self.cont3 = 0



    def open_wid_res_pesquisa(self, texto):

        if self.cont3 == 1:

            self.remove_widget(self.widrespesquisa)
            self.cont3 = 0

        self.add_widget(self.widrespesquisa)
        self.widrespesquisa.resultado_pesq(texto)

        self.cont3 = 1



    def apagar_registro(self):

        self.widintrodados.apagar_registro_f()
        self.remove_widget(self.widpesquisa)
        self.remove_widget(self.widintrodados)


class PopupSalvar(Popup):
    pass


class PopupFaltaDados(Popup):
    pass


class PopupConfirmacao(Popup):

    texto = 'Não'


class WidLabelTexto(Label):

    ist = 'ist:'
    diabete = 'diabete:'
    posicao = 'Posição:'


class WidLabelResultados(Label):
    pass
