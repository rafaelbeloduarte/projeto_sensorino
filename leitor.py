# -*- coding: utf-8 -*-
import tkinter
import serial
import serial.tools.list_ports
import threading
from tkinter.filedialog import asksaveasfilename
from tkinter import *
import sys
import os
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# funções-------------------------------------------------------------------------------------

def sel():
    # LISTA AS PORTAS DISPONÍVEIS
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    selecao = "Porta selecionada: \n" + str(var.get())
    label = Label(top)
    label.grid(row=2, column=1)
    label.configure(background='#000000', foreground='white', borderwidth=3, relief='groove')
    label.config(text=selecao)

def graficoinst():
    plt.close()
    fig = plt.figure()
    grafico = open('grafico.dat', 'r').read()
    vetores = grafico.split('\n')
    vetores = filter(None, vetores)
    vetores = list(vetores)
    for i in range(len(vetores)):
        aux = vetores[i].split(",")
        for j in range(len(aux)):
            aux[j] = float(aux[j])
        vetores[i] = aux
    matriz_graf = vetores
    plt.clf()
    eixo = fig.add_subplot(1, 1, 1)
    eixo.plot(matriz_graf)
   # eixo.legend()
    fig.show()

def grafico():
    plt.close()
    fig = plt.figure()
    def animar(i):
        grafico = open('grafico.dat', 'r').read()
        vetores = grafico.split('\n')
        vetores = filter(None, vetores)
        vetores = list(vetores)
        for i in range(len(vetores)):
            aux = vetores[i].split(",")
            for j in range(len(aux)):
                aux[j] = float(aux[j])
            vetores[i] = aux
        matriz_graf = vetores
        plt.clf()
        eixo = fig.add_subplot(1, 1, 1)
        eixo.plot(matriz_graf)
       # eixo.legend()
    ani = animation.FuncAnimation(fig, animar, interval=1000)
    plt.show()

def selbaud():
    selection = "Baudrate: " + str(varbaud.get())
    labelbaud = Label(top)
    labelbaud.grid(row=4, column=1)
    labelbaud.config(background='#000000', foreground='white', borderwidth=3, relief='groove', width=14)
    labelbaud.config(text=selection)

def handle_leitura():
    try:
        ser = serial.Serial(var.get(), baudrate=varbaud.get(), timeout=1, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
        ser.close()
    except Exception as e:
        messagebox.showinfo("Eita!", "Erro: " + str(e) + "\nProvável causa: a porta já está sendo utilizada.",
                            icon='error')
        return None

    if not var.get() or not varbaud.get():
        messagebox.showinfo("Aviso!", "Selecione uma porta/baudrate.")
        return None

    if not n_texto.get():
        messagebox.showinfo("Aviso!", "Por favor, informe o número de entradas.")
        return None

    try:
        salvararquivo = asksaveasfilename(defaultextension=".txt", initialfile="dados")
        arquivousuario = open(salvararquivo, 'w')
        arquivousuario.close()
        arquivo_sinal = open(salvararquivo.replace(".txt", "") + "_sinal.txt", "w")
        arquivo_sinal.close()
    except Exception as e:
        messagebox.showinfo(e)
        return None
    ser = serial.Serial(var.get(), baudrate=varbaud.get(), timeout=1, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

    instr_arquivo = Label(top, text="Para finalizar a leitura apenas feche o programa, seus dados são salvos automaticamente.")
    instr_arquivo.grid(row=2, column=2, columnspan=5)
    instr_arquivo.configure(background='blue', foreground='white', borderwidth=3, relief='groove')

    def iniciar():  # Esta função lê o inpu
        # t da porta selecionada
        i_limpa_texto = 0

        arquivousuario = open(salvararquivo, 'a')
        arquivo_sinal = open(salvararquivo.replace(".txt", "") + "_sinal.txt", 'a')
        rol = IntVar()

        rol_parar = Radiobutton(top, text="Parar rolagem", variable=rol, value=0)
        rol_parar.grid(row=22, column=2, columnspan = 1)
        rol_parar.configure(background='#F2F2F2', indicatoron=0, width=15)

        rol_iniciar = Radiobutton(top, text="Auto rolagem", variable=rol, value=1)
        rol_iniciar.grid(row=22, column=3, columnspan=1)
        rol_iniciar.configure(background='#F2F2F2', indicatoron=0, width=15)
        rol_iniciar.select()

        limpar_graf = IntVar()

        def limpar_graf_estado():
            limpar_graf.set(1)

        limpar_graf_botao = Button(top, text="Limpar gráfico", command=limpar_graf_estado)
        limpar_graf_botao.grid(row=6, column=5, rowspan = 2)
        limpar_graf_botao.configure(activebackground='#000000', activeforeground='#FFFFFF', width=12, height=3)

        graf = open("grafico.dat", 'w')
        graf.close()

        if os.path.isfile("polinomios.txt") == False or os.stat("polinomios.txt").st_size == 0:
            messagebox.showinfo("Atenção!", "Polinômios não encontrados, o sinal será apresentado nu.")
            poli = open("polinomios.txt", 'w')
            n_entradas = int(n_texto.get())
            for i in range(n_entradas):
                poli.write("1 0\n")
        if abre_poli.get():
            poli = open(abre_poli.get()).readlines()
            with open(abre_poli.get()) as arquivo:
                for i, arquivo in enumerate(arquivo):
                    pass
            linhas = i + 1
            if linhas != int(n_texto.get()):
                messagebox.showinfo("Atenção!", "Número de equações diferente do número de entradas. Os sinais das entradas restantes serão exibidos inalterados.")
                escrever_polinomios = open(abre_poli.get(), 'a')
                restantes = int(n_texto.get()) - len(poli)
                for i in range(restantes):
                    escrever_polinomios.write("1 0\n")
                escrever_polinomios.close()
        else:
            poli = open("polinomios.txt").readlines()
            with open("polinomios.txt") as arquivo:
                for i, arquivo in enumerate(arquivo):
                    pass
            linhas = i + 1
            if linhas < int(n_texto.get()):
                messagebox.showinfo("Atenção!", "Número de equações diferente do número de entradas. Os sinais das entradas restantes serão exibidos inalterados.")
                escrever_polinomios = open("polinomios.txt", 'a')
                restantes = int(n_texto.get()) - len(poli)
                for i in range(restantes):
                    escrever_polinomios.write("1 0\n")
                escrever_polinomios.close()

        for i in range(len(poli)):
            poli[i] = poli[i].replace("\n", "").split(" ")
        for i in range(len(poli)):
            for j in range(len(poli[i])):
                poli[i][j] = float(poli[i][j])
        text.insert(END, str(poli))
        text.see(END)

        try:
            # LOOP DE LEITURA
            while True:
                serial_bytes = ser.readline()
                serial_texto = serial_bytes.decode('utf-8')
                a = serial_texto.split(' ')
                graf = open("grafico.dat", 'a')
                dados = []
                lista_dados = []
                if a:
                    dados = '[%s]' % ', '.join(map(str, a))
                    # map serve para aplicarmos uma função a cada elemento de uma lista,
                    # retornando uma nova lista contendo os elementos resultantes da aplicação da função.
                    # The %s token allows to insert (and potentially format) a string.
                    # Notice that the %s token is replaced by whatever I pass to the string after the % symbol.
                    dados = dados.replace('\n', '').replace('\r', '').replace('[', '').replace(']', '').replace(" ", "").replace("'", "")
                    lista_dados = dados.split(",")
                    lista_dados = filter(None, lista_dados)
                    lista_dados = list(lista_dados)
                    for i in range(len(lista_dados)):
                        lista_dados[i] = float(lista_dados[i])
                if lista_dados:
                    for i in range(len(poli)):
                        lista_dados[i] = poli[i][0]*lista_dados[i] + poli[i][1]
                    arquivousuario.write(str(lista_dados).replace('[', '').replace(']', '') + '\n')
                    arquivousuario.flush()
                    arquivo_sinal.write(dados + '\n')
                    arquivo_sinal.flush()
                    graf.write(str(lista_dados).replace('[', '').replace(']', '') + '\n')
                    graf.flush()
                    text.insert(END, str(lista_dados).replace('[', '').replace(']', '') + '\n')
                    if rol.get() == 1:
                        text.see(END)
                    i_limpa_texto += 1
                if i_limpa_texto > 1000:
                    text.delete(1.0, END)

                    graf = open('grafico.dat', 'r+')
                    graf.truncate(0)

                    i_limpa_texto = 0
                if limpar_graf.get() == 1:
                    graf = open('grafico.dat', 'w')
                    graf.truncate(0)

                    limpar_graf.set(0)

                # time.sleep(1)
        except Exception as e:
            messagebox.showinfo("Erro!", "Erro: " + str(e), icon='error')
            pass
        ser.close()
        graf.close()
        arquivousuario.close()
        arquivo_sinal.close()

    t = threading.Thread(target=iniciar)
    t.daemon = True
    t.start()

def atualizarporta():
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    if not connected:
        messagebox.showinfo("Aviso!", "Nenhuma porta disponível, verifique se seu dispositivo está conectado.")
    # exibe as portas disponíveis
    ports = list(serial.tools.list_ports.comports())
    for i in range(len(ports)):
        ports[i] = str(ports[i])
    for i in range(len(connected)):
        R = Radiobutton(top, text=connected[i], variable=var, value=str(connected[i]), command=sel)
        R.grid(row=1, column=2 + i)
        R.configure(background='#F2F2F2', indicatoron=0, width=12)
        if "Arduino" in ports[i]:
            R.select()
            selecao = "Porta selecionada:\n" + ports[i]
            label = Label(top)
            label.grid(row=2, column=1)
            label.configure(background='#000000', foreground='white', borderwidth=3, relief='groove')
            label.config(text=selecao)

def reiniciar():
    if messagebox.askokcancel("Reiniciando...", "Tem certeza?"):
        python = sys.executable
        os.execl(python, python, *sys.argv)
    else:
        return None

def fechando():
    if messagebox.askokcancel("Fechando...", "Tem certeza?"):
        plt.close('all')
        top.destroy()

# fim das funções-----------------------------------------------------------------------------

# Código para os widgets vai aqui.------------------------------------------------------------

# define a janela principal----------------------------------
top = tkinter.Tk()
top.wm_title("Leitor de dados - portas serial - DEQ - UEM")
top.minsize(800, 650)
top.geometry("950x650")
top.configure(background='#000000')
# -----------------------------------------------------------

comlist = serial.tools.list_ports.comports()
connected = []
for element in comlist:
    connected.append(element.device)
if not connected:
    messagebox.showinfo("Aviso!", "Nenhuma porta disponível, verifique se seu dispositivo está conectado.")

# var1 é uma label ("Selecione a porta:")
var1 = StringVar()
label1 = Label(top, textvariable=var1, relief=RAISED, bd=0)
var1.set("Selecione a porta:")
label1.grid(row=1, column=1)
label1.configure(background='#000000', foreground='white')

# exibe as portas disponíveis
ports = list(serial.tools.list_ports.comports())
for i in range(len(ports)):
    ports[i] = str(ports[i])
var = StringVar()  # var armazena a porta que o usuário informa
for i in range(len(connected)):
    R = Radiobutton(top, text=connected[i], variable=var, value=str(connected[i]), command=sel)
    R.grid(row=1, column=2 + i)
    R.configure(indicatoron=0, width=12, activebackground='white', activeforeground='black')
    if "Arduino" or "Serial USB" in ports[i]:
        R.select()
        selecao = "Porta selecionada:\n" + str(var.get())
        label = Label(top)
        label.grid(row=2, column=1)
        label.configure(background='#000000', foreground='white', borderwidth=3, relief='groove')
        label.config(text=selecao)
# pega o baud rate, varbaud é o baudrate e var2 é uma label============================
var2 = StringVar()
label2 = Label(top, textvariable=var2, bd=0)
var2.set("Selecione a taxa \n de transferência de \n dados (Baudrate):")
label2.grid(row=3, column=1)
label2.configure(background='#000000', foreground='white')
varbaud = IntVar()
R1 = Radiobutton(top, text="4800", variable=varbaud, value=4800, command=selbaud)
R1.grid(row=3, column=2)
R1.configure(indicatoron=0, width=12)
R2 = Radiobutton(top, text="9600", variable=varbaud, value=9600, command=selbaud)
R2.grid(row=3, column=3)
R2.configure(indicatoron=0, width=12)
R2.select()
R3 = Radiobutton(top, text="38400", variable=varbaud, value=38400, command=selbaud)
R3.grid(row=3, column=4)
R3.configure(indicatoron=0, width=12)
R4 = Radiobutton(top, text="57600", variable=varbaud, value=57600, command=selbaud)
R4.grid(row=3, column=5)
R4.configure(indicatoron=0, width=12)
R5 = Radiobutton(top, text="115200", variable=varbaud, value=115200, command=selbaud)
R5.grid(row=3, column=6)
R5.configure(indicatoron=0, width=12)
R6 = Radiobutton(top, text="230400", variable=varbaud, value=230400, command=selbaud)
R6.grid(row=3, column=7)
R6.configure(indicatoron=0, width=12)

selection = "Baudrate: " + str(varbaud.get())
labelbaud = Label(top)
labelbaud.grid(row=4, column=1)
labelbaud.config(background='#000000', foreground='white', borderwidth=3, relief='groove', width=14)
labelbaud.config(text=selection)
# =====================================================================================

label_n = Label(top, text = "Número de entradas:")
label_n.grid(row = 11, column = 6)
label_n.configure(background='#000000', foreground='white')

label_eqs = Label(top, text = "Equação da reta: y = a*x+b, padrão: y=x")
label_eqs.grid(row = 13, column = 5, columnspan = 3)
label_eqs.configure(background='#000000', foreground='white')

n_texto = StringVar()
n = Entry(top, textvariable = n_texto)
n.grid(row=12, column=6)

label_a = Label(top, text = "a:")
label_a.grid(row = 14, column = 5)
label_a.configure(background='#000000', foreground='white')

arquivo_coef = open("polinomios.txt", 'w')
arquivo_coef.close()

abre_poli = StringVar()

def abre_polinomio():
    try:
        abre_poli.set(filedialog.askopenfilename(initialdir = "/",title = "Selecione seu arquivo",filetypes = (("Arquivo de texto","*.txt"),("Todos os arquivos","*.*"))))
    except Exception as e:
        messagebox.showinfo(e)
        return None

button_abre_poli = Button(top, text = "Carregar equações", command = abre_polinomio)
button_abre_poli.grid(row=17, column=7)
button_abre_poli.configure(activebackground='#000000', activeforeground='#FFFFFF')

def pega_coef():
    if not n_texto.get():
        messagebox.showinfo("Aviso!", "Por favor, informe o número de entradas.")
        return None
    coef_a = a.get()
    coef_b = b.get()
    text.insert(END, "y = " + coef_a + "*x" + " + " + coef_b + '\n')
    text.see(END)
    arquivo_coef = open("polinomios.txt", 'a')
    arquivo_coef.write(coef_a + " ")
    arquivo_coef.write(coef_b + "\n")
    arquivo_coef.close()
    a.delete(0, END)
    b.delete(0, END)
    arquivo_coef.close()

def salva_polinomio():
    try:
        salvar_poli = asksaveasfilename(defaultextension=".txt", initialfile="meus_polinomios")
        arquivo_poli = open(salvar_poli, 'w')
        texto = open("polinomios.txt").read()
        texto = texto.replace('\r', '').replace('[', '').replace(']', '').replace(",", "").replace("'", "")
        arquivo_poli.write(texto)
        arquivo_poli.close()
    except Exception as e:
        messagebox.showinfo(e)
        return None

button_salva_poli = Button(top, text = "Salvar equações", command = salva_polinomio)
button_salva_poli.grid(row=16, column=7)
button_salva_poli.configure(activebackground='#000000', activeforeground='#FFFFFF')

a_texto = StringVar()
a = Entry(top, textvariable = a_texto)
a.grid(row=14, column=6)

label_b = Label(top, text = "b:")
label_b.grid(row = 15, column = 5)
label_b.configure(background='#000000', foreground='white')

b_texto = StringVar()
b = Entry(top, textvariable = b_texto)
b.grid(row=15, column=6)

button_entrar = Button(top, text = "Inserir", command = pega_coef)
button_entrar.grid(row=16, column=6)
button_entrar.configure(activebackground='#000000', activeforeground='#FFFFFF')

espaco = Label(top, text=" ")  # apenas coloca um espaço vazio no grid
espaco.grid(row=5, column=1)
espaco.configure(background='#000000', foreground='white')
# botão que chama o gráfico dos dados
botaograf = tkinter.Button(top, text="Exibir gráfico em tempo real", command=grafico)
botaograf.grid(row=7, column=3, columnspan = 2)
botaograf.configure(activebackground='#000000', activeforeground='#FFFFFF', width = 25)

botaograf_inst = tkinter.Button(top, text="Exibir gráfico", command=graficoinst)
botaograf_inst.grid(row=6, column=3, columnspan = 2)
botaograf_inst.configure(activebackground='#000000', activeforeground='#FFFFFF', width = 25)


inicia = tkinter.Button(top, text="Iniciar leitura", command=handle_leitura)
inicia.grid(row=6, column=1)
inicia.configure(activebackground='#000000', activeforeground='#FFFFFF', width=12)

reinicia = tkinter.Button(top, text="Reiniciar", command=reiniciar, width=12)
reinicia.grid(row=6, column=7)
reinicia.configure(activebackground='#000000', activeforeground='#FFFFFF', width=12)

atporta = tkinter.Button(top, text="Atualizar portas", command=atualizarporta)  # botão atualizar portas
atporta.grid(row=6, column=6)
atporta.configure(activebackground='#000000', activeforeground='#FFFFFF', width=12)

espaco2 = Label(top, text=" ")  # apenas coloca um espaço vazio no grid
espaco2.grid(row=8, column=1)
espaco2.configure(background='#000000', foreground='white')

text = ScrolledText(top, width=50, height=20)
text.grid(row=11, column=1, columnspan=5, rowspan=10)

text.insert(END, "          INSTRUÇÕES\n")
text.insert(END, "\n")
text.insert(END, ">O loop de seu controlador deve\nretornar os dados da seguinte forma:\n")
text.insert(END, "a b c ...\n")
text.insert(END, "Ex: 1 2 3 4 5\n")
text.insert(END, "\n>Declare o número de entradas\nantes de iniciar a leitura.\n")
text.insert(END, "\n")
text.see(END)
# chama o mainloop -> abre a janela com os itens anteriores
top.protocol("WM_DELETE_WINDOW", fechando)
top.mainloop()
