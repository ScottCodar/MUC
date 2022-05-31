import sqlite3
import os

import PyPrincipal
import PyPesquisa

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

db_path = os.path.expanduser(
    "~/Sistema Gestao Escolar/Arquivo Passivo/BDArquivoPassivo.db")

class WidIntroDados(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__()

        self.cont1 = 0
        self.tipo_acao = None

        self.widresultado1 = WidResultado1()

        self.ids.lbl_05.text = 'IST'
        self.ids.lbl_06.text = 'Diabete'
        self.ids.lbl_08.text = 'Não'
        self.ids.lbl_10.text = 'Não'

    def limpa_widintrodados(self):

        self.ids.txt_input01.focus = True
        self.ids.txt_input01.text = ''
        self.ids.txt_input02.text = ''
        self.ids.txt_input03.text = ''
        self.ids.txt_input04.text = ''
        self.ids.txt_input11.text = ''
        self.ids.check01.active = False
        self.ids.check02.active = False
        self.ids.check03.active = False
        self.ids.check04.active = False

        self.ids.btn_salvar.disabled = False
        self.ids.btn_limpar.disabled = False

        self.ids.btn_salvar.text = '  Salvar'
        self.ids.btn_salvar.color = (0.831, 0.941, 1, 1)

        self.remove_widget(self.widresultado1)

    def acao_btn_salvar(self):

        paciente = self.ids.txt_input01.text
        duracao = self.ids.txt_input11.text
        medicamento = self.ids.txt_input02.text
        dosagem = self.ids.txt_input03.text
        mg = self.ids.txt_input04.text
        result_checkboxes = [
            self.ids.check01.active,
            self.ids.check02.active,
            self.ids.check03.active,
            self.ids.check04.active]

        if self.tipo_acao == 'Novo Registro':
            self.salvar_dados(paciente, duracao, medicamento, dosagem, mg, result_checkboxes)

        if self.tipo_acao == 'Alterar Registro':
            self.alterar_dados(paciente, duracao, medicamento, dosagem, mg, result_checkboxes)

        if self.tipo_acao == 'Apagar Registro':
            PyPrincipal.PopupConfirmacao().open()


    def salvar_dados(self, paciente, duracao, medicamento, dosagem, mg, result_checkboxes):

        if paciente != '' \
                and True in result_checkboxes[0:2] \
                and True in result_checkboxes[2:]:

            conexao = sqlite3.connect(db_path)
            cursor = conexao.cursor()

            cursor.execute(''' SELECT NOME FROM ARQUIVOPASS
                        WHERE NOME = '{}'
                    '''.format(paciente))

            if cursor.fetchone() is not None:

                PyPrincipal.PopupSalvar(
                    title='O Paciente \n já está cadastrado',
                    separator_color=[1, 0, 0, 1]).open()

            else:

                ''' - Os registros são arquivados em grupos de 30 registros
                      com a primeira letra de cada paciente
                    - O resultado é: Grupo, nº do grupo,
                      nº posição no grupo e numero do protocolo (=id)
                '''

                limpa_grupo = paciente.strip()
                grupo = limpa_grupo[0].upper()

                cursor.execute(''' SELECT MAX(IDARQPASS) FROM ARQUIVOPASS ''')

                protocolo_max = cursor.fetchone()

                if protocolo_max[0] == None:

                    protocolo = 1

                else:
                    protocolo = protocolo_max[0] + 1

                cursor.execute(''' SELECT MAX(NUMGRUPO) FROM ARQUIVOPASS
                                    WHERE GRUPO = '{}' '''.format(grupo))

                num_grupo_max = cursor.fetchone()

                cursor.execute(''' SELECT MAX(NUM_NO_GRUPO) FROM ARQUIVOPASS
                                    WHERE NUMGRUPO = '{}' AND GRUPO = '{}' 
                                    '''.format(num_grupo_max[0], grupo))

                posicao_max = cursor.fetchone()

                if posicao_max[0] == None:

                    num_grupo = 1
                    posicao = 1

                elif posicao_max[0] < 30:

                    num_grupo = num_grupo_max[0]
                    posicao = posicao_max[0] + 1

                else:
                    num_grupo = num_grupo_max[0] + 1
                    posicao = 1

                insert = ''' INSERT INTO ARQUIVOPASS
                            (NOME, DURACAO, MEDICAMENTO, DOSAGEM, MG, IST, DIABETE,
                            GRUPO, NUMGRUPO, NUM_NO_GRUPO) '''

                values1 = (paciente.strip(), duracao, medicamento, dosagem, mg,
                           result_checkboxes[0], result_checkboxes[2],
                           grupo, num_grupo, posicao)

                values2 = ''' VALUES
                            ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                            '''.format(*values1)

                cursor.execute(insert + ' ' + values2)
                conexao.commit()
                conexao.close()

                self.add_widget(self.widresultado1)
                self.widresultado1.ids.lbl_titulo.text = 'Cadastrado com sucesso'
                self.widresultado1.ids.lbl_pasta.text = '{} - {}'.format(grupo, num_grupo)
                self.widresultado1.ids.lbl_posicao.text = str(posicao)
                self.widresultado1.ids.lbl_protocolo.text = 'AP.{}'.format(protocolo)

                self.ids.btn_salvar.disabled = True
                self.ids.btn_salvar.background_disabled_normal = 'Images/btn_azulDisable60.png'

        else:
            self.popups_aviso(paciente, result_checkboxes)


    def inicio_alterar_dados(self, nome):

        self.add_widget(self.widresultado1)

        if self.tipo_acao == 'Alterar Registro':
            self.ids.btn_salvar.text = '  Alterar'
            self.ids.btn_salvar.color = (0.831, 0.941, 1, 1)

        if self.tipo_acao == 'Apagar Registro':
            self.ids.btn_salvar.text = '  Apagar'
            self.ids.btn_salvar.color = (1, 0, 0, 1)

        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()

        cursor.execute(''' SELECT IDARQPASS, NOME, DURACAO, MEDICAMENTO, DOSAGEM, MG, IST, DIABETE,
                            GRUPO, NUMGRUPO, NUM_NO_GRUPO
                            FROM ARQUIVOPASS
                            WHERE NOME = '{}' '''.format(nome))


        for res in cursor:

            self.ids.txt_input01.text = str(res[1])
            self.ids.txt_input11.text = str(res[2])
            self.ids.txt_input02.text = str(res[3])
            self.ids.txt_input03.text = str(res[4])
            self.ids.txt_input04.text = str(res[5])


            if res[6] == 'True':
                self.ids.check01.active = True
            if res[6] == 'False':
                self.ids.check02.active = True
            if res[7] == 'True':
                self.ids.check03.active = True
            if res[7] == 'False':
                self.ids.check04.active = True
            
            self.widresultado1.ids.lbl_titulo.text = 'Local do Registro'
            self.widresultado1.ids.lbl_pasta.text = '{} - {}'.format(str(res[8]), str(res[9]))
            self.widresultado1.ids.lbl_posicao.text = str(res[10])
            self.widresultado1.ids.lbl_protocolo.text = 'AP.{}'.format(str(res[0]))


    def alterar_dados(self, paciente, duracao, medicamento, dosagem, mg, result_checkboxes):

        id_reg = self.widresultado1.ids.lbl_protocolo.text[3:]


        if paciente != '' \
                and True in result_checkboxes[0:2] \
                and True in result_checkboxes[2:]:

            conexao = sqlite3.connect(db_path)
            cursor = conexao.cursor()

            cursor.execute('''UPDATE ARQUIVOPASS
                                SET (NOME, DURACAO, MEDICAMENTO, DOSAGEM, MG, IST, DIABETE)
                                = ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
                                WHERE IDARQPASS = '{}'
                                '''.format(paciente, duracao, medicamento, dosagem, mg,\
                                    result_checkboxes[0], result_checkboxes[2], id_reg))

            conexao.commit()
            conexao.close()

            PyPrincipal.PopupSalvar(
                title='Registro alterado \ncom sucesso',
                separator_color=[0, 1, 0, 1]).open()

            self.ids.btn_salvar.disabled = True
            self.ids.btn_salvar.background_disabled_normal = 'Images/btn_azulDisable60.png'

        else:
            self.popups_aviso(paciente, result_checkboxes)


    def apagar_registro_f(self):


        id_reg = self.widresultado1.ids.lbl_protocolo.text[3:]

        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()

        cursor.execute(''' DELETE FROM ARQUIVOPASS
                            WHERE IDARQPASS = '{}' '''.format(id_reg))

        conexao.commit()
        conexao.close()

        PyPrincipal.PopupSalvar(
            title='Protocolo - {} \napagado com sucesso'.format(
                self.widresultado1.ids.lbl_protocolo.text),
            separator_color=[0, 1, 0, 1]).open()


    def popups_aviso(self, paciente, result_checkboxes):

        if paciente == '':
            PyPrincipal.PopupFaltaDados(
                pos_hint={'x': .10, 'y': .755}, size_hint=(1, .02),
                title=(f'? {10 * " "} Nome do Paciente {10 * " "} ?')).open()

        elif not True in result_checkboxes:
            PyPrincipal.PopupFaltaDados(
                pos_hint={'x': .10, 'y': .755}, size_hint=(1, .02),
                title=(f'? {12 * " "} ? {40 * " "} ? {12 * " "} ?')).open()

        elif not True in result_checkboxes[0:2]:
            PyPrincipal.PopupFaltaDados(
                pos_hint={'x': .10, 'y': .755}, size_hint=(1, .02),
                title=(f'? {12 * " "} ?')).open()

        elif not True in result_checkboxes[2:]:
            PyPrincipal.PopupFaltaDados(
                pos_hint={'x': .10, 'y': .755}, size_hint=(1, .02),
                title=(f'? {12 * " "} ?')).open()


class WidResultado1(BoxLayout):

    posicao = 'Posição'
