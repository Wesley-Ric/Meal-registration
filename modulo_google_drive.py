# importa a biblioteca para dar comando ao s.o
import os.path

# importa as bibliotecas do google drive api
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# importa a biblioteca datatime para pegar a data atual
from datetime import datetime

def google():
    now = str(datetime.now())[:19]      #esquema para pegar a data e hora atual e atribuir a now
    now = now.replace(':' , '_')        #esquema para separar com : e _ a data e hora

    SCOPES = ['https://www.googleapis.com/auth/drive'] #escopo para dar permissão total
    nome = 'Relatorio_'+str(now)+'.wes' #renomeia o arquivo com o now
    folderid = '2_C5o7mmm6W1sIjfAgThAatuKvmmABCID' #id da pasta do google dirve(o id que coloquei é apenas ilustrativo)
    filepath = 'Relatorio-cafe-lanche.wes'  #nome do arquivo que esta na mesma pasta (caminho da arquivo)
    mimetype = 'text/plain' #tipo do arquivo em mimetype
    creds = None #faz creds começar sem nada
    if os.path.exists('token.json') : #testa se o token existe
        creds = Credentials.from_authorized_user_file('token.json' , SCOPES) #atribui o token a creds
    if not creds or not creds.valid :
        if creds and creds.expired and creds.refresh_token :
            creds.refresh(Request()) #faz um request do token
        else :
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json' , SCOPES)    #flow recebe credentials
            creds = flow.run_local_server(port=0)
        with open('token.json' , 'w') as token :
            token.write(creds.to_json())


    drive_service = build('drive' , 'v3' , credentials=creds, static_discovery=False)   #staric_discovery=False é usado para o código funcionar em uma interface grafica
    file_metadata = {'name' : nome , "parents" : [folderid]}    #você fornece o nome e o a pasta do google drive
    media = MediaFileUpload(filepath , mimetype=mimetype)       #pega o caminho da arquivo e o mimetype dele
    file = drive_service.files().create(body=file_metadata , media_body=media , fields='id').execute()
    fileidcode = file.get('id')