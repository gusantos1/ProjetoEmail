import sys
import json
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ProjetoEmail.janelaemail import *
from ProjetoEmail.about import *
from PyQt5.QtWidgets import QMainWindow,QApplication,QFileDialog,QMessageBox
class MainW(QMainWindow, Ui_MainWindow):
    """Janela principal do programa(MainW)."""
    def __init__(self):
        super().__init__(parent=None)
        super().setupUi(self)
        self.candidados_reprovados = None
        self.btn_op_json_2.clicked.connect(self.abrir_json)#Chama método para abrir json.
        self.rdbtn_gmail.clicked.connect(self.radio_gmail)
        self.rdbtn_hotmail.clicked.connect(self.radio_hotmail)
        self.rdbtn_yahoo.clicked.connect(self.radio_yahoo)
        self.rdbtn_outros.clicked.connect(self.radio_outros)
        self.user_host = None
        self.user_port = None
        #Tela texto
        self.textEdit.setToolTip('Escreva seu email.')
        self.textEdit.setAcceptRichText(False) #Retira formatações de texto colados.
        #Botão enviar
        self.btn_enviar.setToolTip('Enviar para todos os candidatos.')
        self.btn_enviar.clicked.connect(self.enviar)
        #Botão candidatos
        self.btn_candidatos.setToolTip('Mostrar todos os candidatos.')
        #botão configurar.
        self.btn_config.setToolTip('Configurações')
        self.About = About()#Inst. da janela Configurações
        self.btn_config.clicked.connect(self.janela)#Chama método para abrir janela de Configurações
    def janela(self):
        self.About.show()
    def abrir_json(self):
        """Função que abre dados dos candidatos em json."""
        arquivo = QFileDialog.getOpenFileName(self, caption='Abrir arquivo json',
                                              directory=QtCore.QDir.currentPath(),
                                              filter='json (*.json)')
        try:
            dir_arquivo = arquivo[0]
            self.diretorio_json_2.setText(dir_arquivo)
            with open(dir_arquivo,'r') as reprovados:
                self.candidados_reprovados = json.load(reprovados)
        except:
            pass
    #Configuração dos Radio Buttons
    def radio_gmail(self):
        host = self.tx_host.setText('smtp.gmail.com')
        port = self.tx_port.setText('587')
        host = self.tx_host.toPlainText()
        port = self.tx_port.toPlainText()
        self.user_host = host
        self.user_port = port
    def radio_hotmail(self):
        host = self.tx_host.setText('smtp.live.com')
        port = self.tx_port.setText('465')
        host = self.tx_host.toPlainText()
        port = self.tx_port.toPlainText()
        self.user_host = host
        self.user_port = port

    def radio_yahoo(self):
        host = self.tx_host.setText('smtp.mail.yahoo.com')
        port = self.tx_port.setText('465')
        host = self.tx_host.toPlainText()
        port = self.tx_port.toPlainText()
        self.user_host = host
        self.user_port = port

    def radio_outros(self):
        host = self.tx_host.setText('')
        port = self.tx_port.setText('')
        host = self.tx_host.toPlainText()
        port = self.tx_port.toPlainText()
        self.user_host = host
        self.user_port = port

    def enviar(self):
        texto = self.textEdit.toPlainText()
        self.user_email = self.tx_email.toPlainText()
        self.user_senha = self.le_senha.text()

        for candidato,email in self.candidados_reprovados.items():
            with open('main.html','r+',encoding='utf-8') as html:
                template = Template(html.read())
                body = template.substitute(mensagem = texto, nome = candidato)
                #Criando Mensagem
                msg = MIMEMultipart()
                msg['from'] = 'Canal Puxei Comp'
                msg['to'] = email['email']
                msg['subject'] = 'Resultado do processo seletivo.'
                send = MIMEText(body, 'html', 'utf-8')
                msg.attach(send)
                with smtplib.SMTP(host=self.user_host, port=self.user_port) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(self.user_email, self.user_senha)
                    smtp.send_message(msg)
class About(QMainWindow,Ui_Agradecimentos):
    def __init__(self):
        super().__init__(parent=None)
        super().setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tela = MainW()
    tela.show()
    sys.exit(app.exec_())