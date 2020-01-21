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
    plt.show()

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
    text.insert(END, "\nBaudrate: " + str(varbaud.get()) + "\n")
    text.see(END)

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
    instr_arquivo.grid(row = 1, column=1, columnspan=5)
    instr_arquivo.configure(background='blue', foreground='white', borderwidth=3, relief='groove')

    def iniciar():  # Esta função lê o inpu
        # t da porta selecionada
        i_limpa_texto = 0

        arquivousuario = open(salvararquivo, 'a')
        arquivo_sinal = open(salvararquivo.replace(".txt", "") + "_sinal.txt", 'a')
        rol = IntVar()

        rol_parar = Radiobutton(top, text="Parar rolagem", variable=rol, value=0)
        rol_parar.grid(row=20, column=2, columnspan = 1)
        rol_parar.configure(background='#F2F2F2', indicatoron=0, width=15)

        rol_iniciar = Radiobutton(top, text="Auto rolagem", variable=rol, value=1)
        rol_iniciar.grid(row=20, column=3, columnspan=1)
        rol_iniciar.configure(background='#F2F2F2', indicatoron=0, width=15)
        rol_iniciar.select()

        graf = open("grafico.dat", 'w')
        graf.close()

        if os.path.isfile(abre_poli.get()) == False and os.path.isfile("polinomios.txt") == False:
            messagebox.showinfo("Atenção!", "Arquivo não encontrado, o sinal será apresentado nu.")
            poli = open("polinomios.txt", 'w')
            n_entradas = int(n_texto.get())
            for i in range(n_entradas):
                poli.write("1 0\n")
        if abre_poli.get():
            if os.stat(abre_poli.get()).st_size == 0:
                messagebox.showinfo("Atenção!", "Arquivo vazio, será preenchido com y=x.")
                poli = open(abre_poli.get(), 'w')
                n_entradas = int(n_texto.get())
                for i in range(n_entradas):
                    poli.write("1 0\n")
                poli.close()
            poli = open(abre_poli.get()).readlines()
            i = 0
            linhas = i + 1
            if linhas < int(n_texto.get()):
                messagebox.showinfo("Atenção!", "Número de equações menor que o número de entradas. Os sinais das entradas restantes serão exibidos inalterados.")
                escrever_polinomios = open(abre_poli.get(), 'a')
                restantes = int(n_texto.get()) - len(poli)
                for i in range(restantes):
                    escrever_polinomios.write("1 0\n")
                escrever_polinomios.close()
        else:
            poli = open("polinomios.txt").readlines()
            i = 0
            with open("polinomios.txt") as arquivo:
                for i, arquivo in enumerate(arquivo):
                    pass
            linhas = i + 1
            if linhas < int(n_texto.get()):
                messagebox.showinfo("Atenção!", "Número de equações menor que o número de entradas. Os sinais das entradas restantes serão exibidos inalterados.")
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
        text.insert(END, "\n" + str(poli) + "\n\n")
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
        poli.close()

    t = threading.Thread(target=iniciar)
    t.daemon = True
    t.start()

def atualizarporta():
    portas_sub_menu.delete(0, 'end')
    var.set("")
    ports = list(serial.tools.list_ports.comports())
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    for i in range(len(ports)):
        ports[i] = str(ports[i])
    for k in range(len(connected)):
        portas_sub_menu.add_radiobutton(label = connected[k], variable=var, value=str(connected[k]), command=sel)
        if "Arduino" or "Serial USB" in ports[k]:
            var.set(str(connected[k]))
            portas_sub_menu.activate(k)
    text.insert(END, "\nPorta selecionada: " + str(var.get()) + "\n")
    text.see(END)

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
top.wm_title("Sensorino Salva!")
top.minsize(500, 500)
top.geometry("950x600")
top.configure(background='#000000')
# -----------------------------------------------------------

comlist = serial.tools.list_ports.comports()
connected = []
for element in comlist:
    connected.append(element.device)
if not connected:
    messagebox.showinfo("Aviso!", "Nenhuma porta disponível, verifique se seu dispositivo está conectado.")

label_n = Label(top, text = "Número de entradas:")
label_n.grid(row = 2, column = 1, columnspan = 2, padx = 10, pady = 10)
label_n.configure(background='#000000', foreground='white', width = 20)

n_texto = StringVar()
n = Entry(top, textvariable = n_texto)
n.grid(row = 2, column=3, padx = 10, pady = 10)
n.configure(width = 10)

label_eqs = Label(top, text = "Equação da reta: y = a*x+b, padrão: y=x")
label_eqs.grid(row = 2, column = 6, columnspan = 3)
label_eqs.configure(background='#000000', foreground='white')

label_a = Label(top, text = "a:")
label_a.grid(row = 3, column = 6)
label_a.configure(background='#000000', foreground='white')

arquivo_coef = open("polinomios.txt", 'w')
arquivo_coef.close()

abre_poli = StringVar()

def abre_polinomio():
    try:
        abre_poli.set(filedialog.askopenfilename(initialdir = "/",title = "Selecione seu arquivo",filetypes = (("Arquivo de texto","*.txt"),("Todos os arquivos","*.*"))))
        if abre_poli.get():
            text.insert(END, "\nCarregado com sucesso.\n")
            text.see(END)
    except Exception as e:
        messagebox.showinfo(e)
        return None

button_abre_poli = Button(top, text = "Carregar equações", command = abre_polinomio)
button_abre_poli.grid(row=6, column=7)
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

limpar_graf = IntVar()

def limpar_graf_estado():
    limpar_graf.set(1)

button_salva_poli = Button(top, text = "Salvar equações", command = salva_polinomio)
button_salva_poli.grid(row=5, column=7)
button_salva_poli.configure(activebackground='#000000', activeforeground='#FFFFFF')

a_texto = StringVar()
a = Entry(top, textvariable = a_texto)
a.grid(row=3, column=7)

label_b = Label(top, text = "b:")
label_b.grid(row = 4, column = 6)
label_b.configure(background='#000000', foreground='white')

b_texto = StringVar()
b = Entry(top, textvariable = b_texto)
b.grid(row=4, column=7)

button_entrar = Button(top, text = "Inserir", command = pega_coef)
button_entrar.grid(row=3, column=8, rowspan = 2, padx = 15)
button_entrar.configure(activebackground='#000000', activeforeground='#FFFFFF')

text = ScrolledText(top, width=50, height=20)
text.grid(row=3, column=1, columnspan=5, rowspan=10, padx = 10, pady = 10)

text.insert(END, "          INSTRUÇÕES\n")
text.insert(END, "\n")
text.insert(END, ">O loop de seu controlador deve\nretornar os dados da seguinte forma:\n")
text.insert(END, "a b c ...\n")
text.insert(END, "Ex: 1 2 3 4 5\n")
text.insert(END, "\n>Declare o número de entradas\nantes de iniciar a leitura.\n")
text.insert(END, "\n")
text.see(END)

# criar menu
menubar = Menu(top)

menubar.add_command(label="Iniciar leitura", command=handle_leitura)

graf_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Gráficos", menu=graf_menu)
graf_menu.add_command(label="Exibir gráfico em tempo real", command=grafico)
graf_menu.add_command(label="Exibir gráfico", command=graficoinst)
graf_menu.add_separator()
graf_menu.add_command(label="Limpar gráfico", command=limpar_graf_estado)

controlador_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Controlador", menu=controlador_menu)
portas_sub_menu = Menu(controlador_menu, tearoff = 0)
controlador_menu.add_cascade(label="Portas", menu=portas_sub_menu)

var = StringVar()
atualizarporta()

baud_sub_menu = Menu(controlador_menu, tearoff = 0)
controlador_menu.add_cascade(label = "Baudrate", menu = baud_sub_menu)

# pega o baud rate, varbaud é o baudrate===============================================
#4800, 9600, 38400, 57600, 115200, 230400
varbaud = IntVar()
baud_sub_menu.add_radiobutton(label = "4800", variable = varbaud, value = 4800, command = selbaud)
baud_sub_menu.add_radiobutton(label = "9600", variable = varbaud, value = 9600, command = selbaud)
baud_sub_menu.add_radiobutton(label = "38400", variable = varbaud, value = 38400, command = selbaud)
baud_sub_menu.add_radiobutton(label = "57600", variable = varbaud, value = 57600, command = selbaud)
baud_sub_menu.add_radiobutton(label = "115200", variable = varbaud, value = 115200, command = selbaud)
baud_sub_menu.add_radiobutton(label = "230400", variable = varbaud, value = 230400, command = selbaud)
baud_sub_menu.invoke(1)
# =====================================================================================

controlador_menu.add_separator()
controlador_menu.add_command(label = "Atualizar portas", command = atualizarporta)

sair_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Sair/Reiniciar", menu=sair_menu)
sair_menu.add_command(label = "Reiniciar", command = reiniciar)
sair_menu.add_command(label="Sair", command=fechando)

# mostrar o menu
top.config(menu=menubar)

# chama o mainloop -> abre a janela com os itens anteriores
top.protocol("WM_DELETE_WINDOW", fechando)
top.mainloop()
