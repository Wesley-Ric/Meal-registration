#importa bibliotecas da gui
import tkinter.messagebox
from tkinter import *
from tkinter import ttk

#importa as bibliotecas de tempo
from datetime import date
import datetime
import time

#importa as bibliotecas de comandos no S.O
import shutil
import os
import subprocess
import getpass

#importa a bibliote para teste de conexão
import urllib.request
def teste_conexao():
    try:
        urllib.request.urlopen('http://google.com') #testa a conexão e retorna um valor verdadeiro ou falso
        return True
    except:
        return False

if teste_conexao() == False:
    tkinter.messagebox.showinfo('Erro!' , 'O computador está sem internet!\n'
                                              'Conecte-se a internet ou entre em contato com um técnico para resolver.')
else:
    #importa os modulos de email e google drive
    import modulo_email_lc
    import modulo_google_drive
    #importa biblioteca do tkinter que precisa de internet
    from _tkinter import TclError


    Raiz = Tk ()
    Raiz.title('Cadastro café-lanche')
    Raiz.geometry('529x675+500+200')
    Raiz['bg'] = "#d9d9d9"
    icone = PhotoImage(file='img/iconee.png')
    Raiz.resizable(width=False, height=False)   #cria a janela principal
    Raiz.iconphoto(False , icone)

    def cadastrar():
        if teste_conexao() == False :
            tkinter.messagebox.showinfo('Erro!' , 'O computador está sem internet!\n'
                                                  'Conecte-se a internet ou entre em contato com um técnico para resolver.')
        else :  #testa conexao com internet
            with open('Relatorio-cafe-lanche.wes', 'a') as dados: #cria o arquivo
                header = "cod,qtd,tipo,dt,hr" #atribui o valor a header
                arq = open('Relatorio-cafe-lanche.wes' , 'r')   #atribui o arquivo no modo leitura para variavel
                for line in arq :
                    if header in line :
                        break #se tiver header em alguma linha: break
                else :
                    with open('Relatorio-cafe-lanche.wes' , 'a') as f :
                        f.write(header + "\n")  #se não tiver header coloca
                tipo = combobox.get()   #pega o tipo do combo box
                qtdc = qtd.get().isnumeric()    #testa se o valor do text box é um valor numerico e retorna um valor boleano para variavel
                if qtdc == True:
                    cod = '9999999999' #valor fixo
                    data = str(date.today())#pega a data atual do pc
                    hora = str(time.strftime("%H:%M:%S")) #pega o horario atual como string
                    cods = cod + ','
                    qtdcs = str(qtd.get()) + ','
                    tipos = tipo + ','
                    datas = data + ','
                    dados.writelines(cods)  #escreve no arquivo txt
                    dados.writelines(qtdcs)
                    dados.writelines(tipos)
                    dados.writelines(datas)
                    dados.writelines(hora + '\n')
                    #cria uma janela de texto que se fecha sozinha depois de x tempo
                    Menssagem = '''O Cadastro foi realizado\n
                                    com sucesso!'''
                    espera = 500
                    top = Toplevel()
                    top.title('Sucesso!')
                    Message(top , text=Menssagem ,bg='#eef0f2', padx=50 , pady=50).pack()
                    top.geometry('250x150+630+400')
                    top ['bg'] = "#eef0f2"
                    top.after(espera , top.destroy)
                else:
                    tkinter.messagebox.showinfo('erro','O valor digitado no campo "quantidade" é invalido!\n'
                                                'Por favor digite um número valido.')
            qtd.delete(0 , END) #limpa txt box

    def relatoriobackupCL():
        if teste_conexao() == False :   #testa internet
            tkinter.messagebox.showinfo('Erro!' , 'O computador está sem internet!\n'
                                                  'Conecte-se a internet ou entre em contato com um técnico para resolver.')
        else :
            pergunta = tkinter.messagebox.askyesno(title='Confirmar' , message='Tem certeza de que deseja gerar o relatório?') #RETORNA VALOR BOLEANO
            if pergunta == True:
                relatorio =r'Relatorio-cafe-lanche.wes'
                existir = os.path.exists(relatorio)
                if not existir: #testa se o diretorio existe e trata os erros
                    tkinter.messagebox.showinfo('Erro!' , 'O arquivo Relatorio-cafe-lanche.wes não existe!\n'
                                                         'Cadastre algum valor antes de gerar o relatorio.')
                else:
                    user = getpass.getuser()    #pega o user do pc
                    now=str(datetime.datetime.now())[:19]   #pega a data e o horario do pc
                    now=now.replace(':','_')    #separa data e tempo com ':' e '_'

                    pastaatual =r'Relatorio-cafe-lanche.wes'
                    if not os.path.exists('backup-cafe-lanche'):    #tratamento de erro
                        subprocess.call(r'mkdir backup-cafe-lanche', shell=True)    #cria  a pasta
                    destino=r'backup-cafe-lanche/RelatorioBackupCL_'+str(now)+'.wes'
                    pasta='C:/Users/'+user+'/Desktop/RelatoriosCL'
                    existe=os.path.exists(pasta)
                    if not existe:
                        subprocess.call(r'mkdir RelatoriosCL', shell=True)
                        diretoriomover = r'RelatoriosCL'
                        destinomover = 'C:/Users/' + user + '/Desktop/'
                        shutil.move(diretoriomover , destinomover)  #move a pasta de um destino para o outro
                    destino2='C:/Users/'+user+r'/Desktop/RelatoriosCL/RelatorioBackupCL_'+str(now)+'.wes'
                    shutil.copy(pastaatual, destino)    #copia as pastas
                    shutil.copy(pastaatual,destino2)    #copia as pastas
                    modulo_email_lc.email()     #invoca o modulo e da função
                    modulo_google_drive.google()    #invoca o modulo e da função
                    os.remove('Relatorio-cafe-lanche.wes')  #apaga o arquivo

                    Menssagem2 = '''Relatório realizado\n
                    com sucesso!'''
                    espera2 = 750
                    top2 = Toplevel()
                    top2.title('Sucesso!')
                    Message(top2 , text=Menssagem2 ,bg='#eef0f2', padx=50 , pady=50).pack()
                    top2['bg'] = '#eef0f2'
                    top2.geometry('250x150+630+400')
                    top2.after(espera2 , top2.destroy)  #caixa de texto que se auto destroí

    def Sair():
        pergunta = tkinter.messagebox.askyesno(title='Sair' , message='Tem certeza de que deseja fechar o programa?')
        if pergunta == True:
            Raiz.destroy()  #fecha o programa

    frametitulo = Frame(Raiz, bg='red') #frame do titulo que usa pack
    frametitulo.pack(side=TOP, fill=X)
    framecorpo = Frame(Raiz, bg='#d9dee8')
    framecorpo.pack(fill=BOTH, expand=True)

    lblTitulo = Label(frametitulo, text='Leitor de ponto de almoço e jantar', width=100, height=3)  #lbl titulo
    lblTitulo ['bg'] = '#00a0f5'
    lblTitulo ['font'] = 'Calibri 18'
    lblTitulo ['fg'] = '#ffffff'
    lblTitulo.pack(side=TOP, fill=X, ipady=18)

    lblCads = Label(framecorpo, text='*')   #frame onde fica todo o programa
    lblCads['bg']='#d9dee8'
    lblCads['font']='Calibri 20'
    lblCads['fg']='red'
    lblCads.place(x=43,y=25)

    lblCad = Label(framecorpo, text='Tipo de ítem:')    #label tipo de iten
    lblCad['bg']='#d9dee8'
    lblCad['font']='Calibri 20'
    lblCad['fg']='#0055be'
    lblCad.place(x=63,y=25)

    listalc=['cafe','lanche_refeicao','lanche_hora_extra '] #lista das opções da combo box

    combobox = ttk.Combobox(framecorpo, values=listalc,  width=27) #combo box
    combobox['font']='Calibri 20'
    combobox['state'] = 'readonly'
    combobox.current(0)
    combobox.place(x=63,y=80, height=40)



    lblCads = Label(framecorpo, text='*')   #atributos visuais
    lblCads['bg']='#d9dee8'
    lblCads['font']='Calibri 20'
    lblCads['fg']='red'
    lblCads.place(x=43,y=160)

    lblCad = Label(framecorpo, text='Quantidade:')
    lblCad['bg']='#d9dee8'
    lblCad['font']='Calibri 20'
    lblCad['fg']='#0055be'
    lblCad.place(x=63,y=160)

    qtd= Entry(framecorpo, width=28, relief='flat', highlightthickness=2)   #entry onde entrará o valor da quantidade
    qtd.config(highlightbackground='#0055be', highlightcolor='#0055be')
    qtd['font']='Calibri 20'
    qtd['fg']='#0055be'
    qtd.focus_set()
    qtd.place(x=63,y=210, height=40)


    imgbtn = PhotoImage(file='img/button_cadastrar.png')    #botão para cadastrar
    btn1 = Button(framecorpo, image=imgbtn, borderwidth=0, bg='#d9dee8', activebackground='#d9dee8', command=cadastrar)
    btn1.place(x=70,y=300)

    imgbtn2 = PhotoImage(file='img/button_gerar-relatorio.png') #botão para cadastrar gerar o arquivo
    btn2 = Button(framecorpo, image=imgbtn2, borderwidth=0, bg='#d9dee8', activebackground='#d9dee8', command=relatoriobackupCL)
    btn2.place(x=70,y=380)

    imgbtn3 = PhotoImage(file='img/button_sair.png')    #botão para sair
    btn3 = Button(framecorpo, image=imgbtn3, borderwidth=0, bg='#d9dee8', activebackground='#d9dee8', command=Sair)
    btn3.place(x=70,y=460)
    Raiz.mainloop()