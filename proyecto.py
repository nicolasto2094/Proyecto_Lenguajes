#imports
import sys
import time

#// VARIABLES GLOBALES //

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


def leer_cod_assembler():
    print("Leyendo")
    global codigo_assemblre
    while True:
        entrada = sys.stdin.readline().replace(",","").strip().split(' ')
        if entrada[0] == "":
            break
        codigo_assemblre.append([entrada,assembre_a_maquina(entrada)])

    print(codigo_assemblre)

def LD(instruccion):
    global registros
    binario = ""
    if registros.get(instruccion[1]) != None and registros.get(instruccion[2]) != None:
        binario = "01" + registros[instruccion[1]][0] + registros[instruccion[2]][0], 1
    elif registros.get(instruccion[1]) != None and instruccion[2].find("(") == -1:
        a = "{0:b}".format(int(instruccion[2]))
        binario = "00" + registros[instruccion[1]][0] + "110" + ceros_a_la_izq(a, 8), 2
    elif instruccion[1] == "A":
        instruccion[2] = instruccion[2].replace("(", "")
        instruccion[2] = instruccion[2].replace(")", "")
        if registros_16.get(instruccion[2]) != None:
            binario = "00" + registros_16[instruccion[2]][0] + "101", 1
        else:
            a = "{0:b}".format(int(instruccion[2]))
            binario = "00111101" + ceros_a_la_izq(a, 16), 3
    elif instruccion[2] == "A":
        instruccion[1] = instruccion[1].replace("(", "")
        instruccion[1] = instruccion[1].replace(")", "")
        if registros_16.get(instruccion[1]) != None:
            binario = "00" + registros_16[instruccion[1]][0] + "010", 1
        else:
            a = "{0:b}".format(int(instruccion[1]))
            binario = "00110010" + ceros_a_la_izq(a, 16), 3
    elif registros_16.get(instruccion[1]) != None and instruccion[2].find("(") == -1:
        a = "{0:b}".format(int(instruccion[2]))
        binario = "00" + registros_16[instruccion[1]][0] + "0001" + ceros_a_la_izq(a, 16), 3
    elif registros_16.get(instruccion[1]) != None and instruccion[1] != "HL":
        instruccion[2] = instruccion[2].replace("(", "")
        instruccion[2] = instruccion[2].replace(")", "")
        a = "{0:b}".format(int(instruccion[2]))
        binario = "1110110101" + registros_16[instruccion[1]][0] + "1011" + ceros_a_la_izq(a, 16), 3
    elif instruccion[1] == "HL":
        instruccion[2] = instruccion[2].replace("(", "")
        instruccion[2] = instruccion[2].replace(")", "")
        a = "{0:b}".format(int(instruccion[2]))
        binario = "00101010" + ceros_a_la_izq(a, 16), 4
    else:
        print("ERROR!!", instruccion)
        time.sleep(1000)
    return binario


def assembre_a_maquina(instruccion):

    if instruccion[0]=="LD":
       return LD(instruccion)
    else:
        print("ERROR!!", instruccion)
        time.sleep(1000)


leer_cod_assembler()