#imports
import sys
import time
import os

#// VARIABLES GLOBALES //
MEMORIA = []

#REGISTROS, donde se guarda su código y su contenido EN UN ARREGLO
# ejemplo poner NZ = 1, -->banderas_estado["NZ"][1] = "1"
registros = { "A":["111",""], "B":["000",""], "C":["001",""], "D":["010",""], "E":["011",""], "H":["100",""], "L":["101",""]}

#registros 16 bits
registros_16 = {"BC":["00",""],"DE":["01",""],"HL":["10",""],"SP":["11",""]}

#banderas de estado
banderas_estado = {"NZ":["000",""],"Z":["001",""],"NC":["010",""],"C":["011",""],"PO":["100",""],"PE":["101",""],
                   "P":["110",""],"M":["111",""] }


#MOSTRAR
tiempo = 1

#CODIGOS
codigo_assemblre = []

#pequeñas funciones
def ceros_a_la_izq(num,bits):
    salida = num
    while len(salida.replace("-",""))<bits:
        salida = "0" + salida
    if int(num,2)<0: salida = complemento_a_dos(salida.replace("-",""))
    return salida
def complemento_a_dos(n):
    bin = ""
    for i in n:
        if i == "0": bin = bin + "1"
        else: bin = bin + "0"
    return bin

def ERROR(instruccion):
    print("ERROR!!", instruccion)
    time.sleep(1)
    sys.exit()
    print(cv)

def BORRAR():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")

def leer_cod_assembler():
    print("Leyendo")
    global codigo_assemblre
    while True:
        entrada = sys.stdin.readline().replace(",","").strip().split(' ')
        if entrada[0] == "":
            break
        codigo_assemblre.append([entrada,assembre_a_maquina(entrada)])

def LD(instruccion):
    global registros, registros_16
    binario = ""
    if registros.get(instruccion[1]) != None and registros.get(instruccion[2]) != None:
        binario = ["01" + registros[instruccion[1]][0] + registros[instruccion[2]][0], 1,1]
    elif registros.get(instruccion[1]) != None and instruccion[2].find("(") == -1:
        a = "{0:b}".format(int(instruccion[2]))
        binario = "00" + registros[instruccion[1]][0] + "110" + ceros_a_la_izq(a, 8), 2,2
    elif instruccion[1] == "A":
        instruccion[2] = instruccion[2].replace("(", "")
        instruccion[2] = instruccion[2].replace(")", "")
        if registros_16.get(instruccion[2]) != None:
            binario = "00" + registros_16[instruccion[2]][0] + "101", 1,3
        else:
            a = "{0:b}".format(int(instruccion[2]))
            binario = "00111101" + ceros_a_la_izq(a, 16), 3,4
    elif instruccion[2] == "A":
        instruccion[1] = instruccion[1].replace("(", "")
        instruccion[1] = instruccion[1].replace(")", "")
        if registros_16.get(instruccion[1]) != None:
            binario = "00" + registros_16[instruccion[1]][0] + "010", 1,5
        else:
            a = "{0:b}".format(int(instruccion[1]))
            binario = "00110010" + ceros_a_la_izq(a, 16), 3,6
    elif registros_16.get(instruccion[1]) != None and instruccion[2].find("(") == -1:
        a = "{0:b}".format(int(instruccion[2]))
        binario = "00" + registros_16[instruccion[1]][0] + "0001" + ceros_a_la_izq(a, 16), 3,7
    elif registros_16.get(instruccion[1]) != None and instruccion[1] != "HL":
        instruccion[2] = instruccion[2].replace("(", "")
        instruccion[2] = instruccion[2].replace(")", "")
        a = "{0:b}".format(int(instruccion[2]))
        binario = "1110110101" + registros_16[instruccion[1]][0] + "1011" + ceros_a_la_izq(a, 16), 4,8
    elif instruccion[1] == "HL":
        instruccion[2] = instruccion[2].replace("(", "")
        instruccion[2] = instruccion[2].replace(")", "")
        a = "{0:b}".format(int(instruccion[2]))
        binario = "00101010" + ceros_a_la_izq(a, 16), 3,9
    else:
        ERROR(instruccion)
    return binario

def ADD(instruccion):
    global registros, registros_16
    binario = ""

    if  instruccion[1]=="A" and registros.get(instruccion[2]) != None:
         binario = "10000"+registros[instruccion[2]][0],1
    elif instruccion[1]=="A" and instruccion[2].find("(") == -1:
        instruccion[2] = instruccion[2].replace("(", "")
        instruccion[2] = instruccion[2].replace(")", "")
        a = "{0:b}".format(int(instruccion[2]))
        binario = "11000110"+ceros_a_la_izq(a,8),2
    elif instruccion[1]=="A" and instruccion[2]=="(HL)":
        binario = "10000110",1
    elif instruccion[1]=="HL" and registros_16.get(instruccion[2]) != None:
        binario = "00"+registros_16[instruccion[2]][0]+"1001",1
    else:
        ERROR(instruccion)
    return binario

def ADC(instruccion):
    global registros, registros_16
    binario = ""
    if  instruccion[1]=="A" and registros.get(instruccion[2]) != None:
         binario = "10001"+registros[instruccion[2]][0],1
    elif instruccion[1]=="HL" and registros_16.get(instruccion[2]) != None:
        binario = "110110101"+registros_16[instruccion[2]][0]+"1010",2
    else: ERROR(instruccion)
    return binario

def SUB(instruccion):
    global registros, registros_16
    binario = ""
    if registros.get(instruccion[1]) != None:
        binario = "10010" + registros[instruccion[1]][0], 1
    else:ERROR(instruccion)
    return binario

def SBC(instruccion):
    global registros, registros_16
    binario = ""
    if  instruccion[1]=="A" and registros.get(instruccion[2]) != None:
         binario = "10011"+registros[instruccion[2]][0],1
    elif instruccion[1]=="HL" and registros_16.get(instruccion[2]) != None:
        binario = "1101010101"+registros_16[instruccion[2]][0]+"0101",2
    else: ERROR(instruccion)
    return binario

def INC(instruccion):
    global registros, registros_16
    binario = ""
    if registros.get(instruccion[1]) != None:
        binario = "00" + registros[instruccion[1]][0]+"100",1
    elif registros_16.get(instruccion[1]) != None:
        binario = "00" + registros_16[instruccion[1]][0]+"0011",1
    elif instruccion[1]=="(HL)": binario = "00110100",1
    else:ERROR(instruccion)
    return binario

def DEC(instruccion):
    global registros, registros_16
    binario = ""
    if registros.get(instruccion[1]) != None:
        binario = "00" + registros[instruccion[1]][0]+"010",1
    elif registros_16.get(instruccion[1]) != None:
        binario = "00" + registros_16[instruccion[1]][0]+"1011",1
    elif instruccion[1]=="(HL)": binario = "00110010",1
    else:ERROR(instruccion)
    return binario

def JP(instruccion):
    global banderas_estado
    binario = ""
    if banderas_estado.get(instruccion[1]) != None:
        a = "{0:b}".format(int(instruccion[2]))
        binario = "11" + banderas_estado[instruccion[1]][0]+"010"+ceros_a_la_izq(a,16), 3
    else:
        a = "{0:b}".format(int(instruccion[2]))
        binario = "11000011" +  ceros_a_la_izq(a, 16), 3
    return binario

def otras_fun(instruccion):
    global registros, registros_16
    binario = ""
    if instruccion[0]=="NEG":
        binario = "1101010110000100",2
    elif instruccion[0]=="NOP":
        binario = "00000000",1
    elif instruccion[0]=="HALT":
        binario = "10110110",1
    elif instruccion[0]=="AND" and registros.get(instruccion[1]) != None:
        binario = "10100"+registros[instruccion[1]][0],1
    elif instruccion[0]=="OR" and registros.get(instruccion[1]) != None:
        binario = "10110"+registros[instruccion[1]][0],1
    elif instruccion[0]=="XOR" and registros.get(instruccion[1]) != None:
        binario = "10101"+registros[instruccion[1]][0],1
    elif instruccion[0]=="CP" and registros.get(instruccion[1]) != None:
        binario = "10111"+registros[instruccion[1]][0],1
    else:ERROR(instruccion)
    return binario

def assembre_a_maquina(instruccion):
    otras = ["AND","OR","XOR","CP","NEG","NOP","HALT"]
    if instruccion[0]=="LD": return LD(instruccion)
    elif instruccion[0]=="ADD": return ADD(instruccion)
    elif instruccion[0]=="ADC": return ADC(instruccion)
    elif instruccion[0]=="SUB": return SUB(instruccion)
    elif instruccion[0]=="SBC": return SBC(instruccion)
    elif instruccion[0]=="INC": return INC(instruccion)
    elif instruccion[0]=="DEC": return DEC(instruccion)
    elif instruccion[0]=="JP": return JP(instruccion)
    elif otras.index(instruccion[0]) !=-1: return otras_fun(instruccion)
    else:
        ERROR(instruccion)

def maquina_a_memoria():
    global MEMORIA,tiempo
    BORRAR()
    for i in codigo_assemblre:
        a = i[1][1]
        if a == 1:
            MEMORIA.append((i[1][0],i[0]))
            print("instrucción: {}".format(i[0]))
            print("COD: "+i[1][0])
        elif a == 2:
            MEMORIA.append((i[1][0][:8],i[0]))
            MEMORIA.append((i[1][0][8:16],"--"))
            print("instrucción: {}".format(i[0]))
            print("COD: "+i[1][0][:8]+" "+i[1][0][8:16])
        elif a == 3:
            MEMORIA.append((i[1][0][:8],i[0]))
            MEMORIA.append((i[1][0][8:16],"--"))
            MEMORIA.append((i[1][0][16:24],"--"))
            print("instrucción: {}".format(i[0]))
            print("COD: "+i[1][0][:8]+" "+i[1][0][8:16]+" "+i[1][0][16:24])
        elif a == 4:
            MEMORIA.append((i[1][0][:8], i[0]))
            MEMORIA.append((i[1][0][8:16], "--"))
            MEMORIA.append((i[1][0][16:24], "--"))
            MEMORIA.append((i[1][0][24:32], "--"))
            print("instrucción: {}".format(i[0]))
            print("COD: "+i[1][0][:8]+" "+i[1][0][8:16]+" "+i[1][0][16:24],i[1][0][24:32])
        else:ERROR()
        time.sleep(tiempo/2)
        BORRAR()
    j = 0
    for i in MEMORIA:
        print("[{}]--> MEMORIA[{}]  ".format(i[0],j))
        print("[{}]--> MEMORIA[{}]  ".format(j,i[0]))
        j = j +1
        time.sleep(0.1)
        BORRAR()
    j = 0
    BORRAR()
    print("MEMORIA")
    for i in MEMORIA:
        print("[{}]--> [{}]  ".format(j,i[0]))
        j = j +  1

BORRAR()

def eje():
    leer_cod_assembler()
    maquina_a_memoria()

def interfaz():
    pass
eje()
