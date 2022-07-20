# Cadastro de lanches e cafés.
## Sistema para cadastro de recebimento de refeições.
Obs: esse projeto foi feito para cadastrar refeições e faz parte de um conjunto de sistemas que irão fornecer dados para um mesmo banco de dados, 
para que pudessem estar numa mesma tabela colocamos os mesmos atributos neles _cod,qtd,tipo,data e hora_, sendo o atributo cod fixado sempre em 9999999999.

O código feito tem como objetivo:
* Cadastrar o refeições em um arquivo .txt para ser enviado para um db posteriormente.
* Gerar um relatório .txt com as seguintes informações.
    1. Código sempre fixado no mesmo valor de 9999999999
    2. Qunatidade de refeições que são obtidos por uma entry.
    3. Tipo:
        * Café.
        * Lanche refeição.
        * Lanche hora extra.
    4. Data.
    5. Hora.
* Enviar o arquivo para o google drive e para o email.

### Código.
O código nesse caso sempre será um valor fixo ou seja uma constrante apenas com o objetivo de preencher a tabela do db.

### Quantidade.
A quantidade é captada por meio da entry e armazenada na variavél qtd, logo após testa-se o tipo da variavél com o metodo isnumeric() retornando um valor boleano para a variavél qtdc, se o valor for verdadeiro o código entra no if.

~~~python
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
qtd.delete(0 , END) 
~~~

Após a execução do código limpa o valor do entry.

### Tipo.
O tipo é pego pelo combobox e armazenado na variavél "tipo" através do linha `tipo = combobox.get()`,
qee depois é gravado no "Relatorio.wes".

~~~python
tipo = combobox.get()

tipos = tipo + ','

dados.writelines(tipos)
~~~
### Data e hora.

#### Data.
Para pegar a data usamos a biblioteca datetime, onde se pega a data atual do computador e atribui em forma de string a variavél data invocando o metodo today()
~~~python
from datetime import date
data = str(date.today())
~~~
Depois é adicionada uma ',' a variavél: `datas = data + ',' `, e então é gravada no arquivo .txt: `dados.writelines(datas)`
#### Hora.
A hora é pega pela biblioteca time em formato de string, formatada e atribuida a uma variavél.

~~~python
import time
hora = str(time.strftime("%H:%M:%S"))
~~~

Após isto é gravada no arquivo .txt: `dados.writelines(hora + '\n')`.

## Relatórios.

A segunda funcionalidade pega os arquivos txt gerados pelo programa, e gera um relatório com um command em um objeto button.
Podemos separar a funcionalidade dessa função em 5 etapas:
1. Cria a pasta de backup _se não existir_ e envia uma cópia do relatório para lá.
2. Cria uma pasta na área de trabalho chamada ´Relatórios´ _se não existir_ e envia uma cópia do arquivo para lá.
3. Envia o arquivo para a pasta do google drive com o modulo do google drive.
4. Envia o arquivo por email com o modulo email.
5. Apaga o arquivo que ficou na pasta inícial.

#### Código:

~~~python
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
~~~


# Em suma é isso, obrigado por ler sobre meu código, se possivel me siga e favorite meus commits <3
