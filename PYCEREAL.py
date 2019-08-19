#-----------------------------------------------------------imports-------------------------------------------------------------
import serial
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#-------------------------------------------------------criar os arquivos-------------------------------------------------------
file = open("info.txt", "a+") 
file.close()

#-----------------------------------------------------------varisveis-----------------------------------------------------------
op = 0
x = 0
COM = 16
log = 0
ccard = ''
cuser=''
lcard= ''
usuario = {}
lpin = ''
pemail= ''


#-------------------------------------------------------------erros-------------------------------------------------------------

def erro():
    global op
    print('opção inválida')
    op= int(input('Deseja registrar(1), entrar(2) ou sair(3)?: \n'))

def erro2():
    global carsen
    print('opção inválida')
    carsen=int(input('Quer entrar com cartão(1) ou senha(2)? \n'))


#------------------------------------------------------------opções-------------------------------------------------------------

carsen=int(input('Deseja entrar com cartão(1) ou senha(2)? \n'))

while  carsen != 1 and carsen != 2:
  erro2()

if carsen == 1:
    op= int(input('Deseja registrar(1), entrar(2) ou sair(3)?: \n'))
    while op != 1 and op != 2 and op != 3:
        erro()
    log = 1


if carsen == 2:
    op= int(input('Deseja registrar(1), entrar(2) ou sair(3)?: \n'))
    while op != 1 and op != 2 and op != 3:
        erro()
    log = 2



#--------------------------------------------------------------card-------------------------------------------------------------
def criasenha():
        global op
        while op == 1:
            cuser=input('digite o novo usuário: \n')
            ccard=input('digite a id do cartão: \n')
            cemail=input('digite o seu email: \n')
            csenha =str(cuser)+','+str(ccard)+','+str(cemail)
            c = open("info.txt", "a+") 
            c.write(str(csenha +'\n'))
            c.close()
            print('cartão registrado')
            op= int(input('Deseja registrar(1), entrar(2) ou sair(3)?: \n'))
            while op != 1 and op != 2 and op != 3:
                erro()						

def lesenha():
    global x
    global lcard
    lcard= input('digite o usuário: \n')

    L= open('info.txt', 'r')
    Le= L.read()
    L.close()

    if lcard in str(Le):
         x = 1
    else:
        print('usuário incorreto')
        lesenha()

def pyreal():
    ser = serial.Serial('COM'+str(COM), 9600)
    p = 0
    time.sleep(3)
    textoSaida = (str(usuario[str(lcard)]))
    ser.write(textoSaida.encode())
    textoEntrada = "" 
    while p == 0:
        textoEntrada = ser.readline()
        p += 1
    ser.close()

def criadicard():
    global pemail
    global usuario
    with open ('info.txt') as arq:
        for pessoa in arq:
            pessoa = pessoa.strip().split(',')
            nome = pessoa[0]
            noome = pessoa[0]
            senha= pessoa[1]
            mail= pessoa[2]
            usuario[nome] = senha
            usuario[noome]= mail
        pemail = str(usuario[noome])



#-------------------------------------------------------------pin---------------------------------------------------------------
def criapin():
    global op
    while op == 1:
            cuser=input('digite o novo usuário: \n')
            
            cpin=input('digite o pin: \n')
            
            cspin =str(cuser)+','+str(cpin)
            c = open("info.txt", "a+") 
            c.write(str(cspin +'\n'))
            c.close()
            print('pin registrado')
            op= int(input('Deseja registrar(1), entrar(2) ou sair(3)?: \n'))
            while op != 1 and op != 2 and op != 3:
                erro()              
   
def lepin():
	global x
	global lpin
	lpin= input('digite o usuário: \n')

	L= open('info.txt', 'r')
	Le= L.read()
	L.close()

	if lpin in str(Le):
		x = 2
	else:
		print('usuário incorreto')
		lesenha()

def criadipin():
    global usuario
    with open ('info.txt') as arq:
        for pessoa in arq:
            pessoa = pessoa.strip().split(',')
            nome = pessoa[0]
            pin= pessoa[1]
            usuario[nome] = pin

def pyrealpin():
	ser = serial.Serial('COM'+str(COM), 9600)
	p = 0
	time.sleep(3)
	textoSaida = (str(usuario[str(lpin)]))
	ser.write(textoSaida.encode())
	textoEntrada = "" 
	while p == 0:
		textoEntrada = ser.readline()
		p += 1
	ser.close()

#--------------------------------------------------------------email-------------------------------------------------------------

def pyemail():
    sender_email = "cesarespacetest@gmail.com"
    receiver_email = pemail
    password = "deus123456789"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirmação De Reserva"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
      <body>
        <p>Olá,<br>
           Acompanhe sua reserva clicando:<br>
           <a href="google.com">aqui</a> 
           aproveite a sala otário.
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


#-------------------------------------------------------------faz acontecer------------------------------------------------------
if op == 1:
    if log == 1:
        criasenha()
    if log ==2:
        criapin()

if op == 2:
    if log ==1:
        lesenha()
        criadicard()
        if x == 1:
            #pyreal()
            pyemail()
                
    if log ==2:
        lepin()
        criadipin()
        if x ==2:
            pyrealpin()
            pyemail()
    		
                
        
if op == 3:
    print(pemail)
    print('saindo...')
