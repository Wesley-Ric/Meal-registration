# imports para o envio de emails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# imports para colocar anexo nos emails
from email.mime.base import MIMEBase
from email import encoders

# imports para atribuir data nos arquivos
from datetime import datetime

def email():
    host = 'smtp.office365.com' #host da conta que vai mandar o email
    porta = '000'  #porta da senha que vai mandar o email
    login = 'samile8126@teasya.com'  #login da conta que vai mandar o email
    senha = '123321'  #senha da conta que vai mandar o email

    enviar = 'destinatario@email.com'     #destinatário1
    login2 = 'samile8126@teasya.com'#no meu caso irá enviar o email para dois destinatários por isso o login2
    enviar2 = 'email@email.com'     #destinatário2
    server = smtplib.SMTP(host, porta) #atribui a variavel os valores da porta e do host

    #abre a conexão e insere as credenciais
    server.ehlo()
    server.starttls()
    server.login(login, senha)
    #corpo em formato html
    corpo = f"""<p></p>
    <h2>ESSE E-MAIL É UMA MENSSAGEM AUTOMÁTICA, NÃO RESPONDA!</h2>
    <h3>Arquivo codificado do relatório de refeições</h3>
    Aqui está o anexo do arquivo de registro das refeições,
    <br>
    Use o programa de leitor para o decodificar
    <br>
    <br>
    <b>ESSE E-MAIL É UMA MENSSAGEM AUTOMÁTICA, NÃO RESPONDA!</b><br>
    """
    #corpo do email e a mensagem que você deseja enviar
    email_msg = MIMEMultipart()
    email_msg['From'] = login #remetente
    email_msg['To'] = enviar    #destinatário
    email_msg['Subject'] = "Relatório refeições"    #anexo
    email_msg.attach(MIMEText(corpo, 'html'))   #mensagem no formato html

    email_msg2 = MIMEMultipart()
    email_msg2['From'] = login2
    email_msg2['To'] = enviar2  #destinatário2
    email_msg2['Subject'] = "Relatório refeições"
    email_msg2.attach(MIMEText(corpo, 'html'))

    now = str(datetime.now())[:19]  #esquema para pegar a data e hora atual e atribuir a now
    now = now.replace(':' , '_')    #esquema para separar com : e _ a data e hora
    cam_arq = "Relatorio.wes"       #atribui o arquivo a uma variavel
    anexo = open(cam_arq, 'rb')     #o anexo abre o arquivo

    #codifica o anexo em base 64
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(anexo.read())
    encoders.encode_base64(att)

    att.add_header('Content-Disposition', f'axexo; filename=Relatorio_'+str(now)+'.wes') #abre o arquivo e o renomeia com a data e hora atual
    anexo.close()
    email_msg.attach(att)   #atribui o anexo ao email
    email_msg2.attach(att)

    server.sendmail(email_msg['From'],email_msg['To'],email_msg.as_string()) #envia o email
    server.sendmail(email_msg2['From'] , email_msg2['To'] , email_msg2.as_string())
    server.quit() #fecha a conexão
