#imports
import sys


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
    while len(num)<bits:
        num = "0" + num
    return num

def leer_cod_assembler():
    print("Leyendo")
    global codigo_assemblre
    while True:
        entrada = sys.stdin.readline().replace(",","").strip().split(' ')
        if entrada[0] == "":
            break
        codigo_assemblre.append([entrada,assembre_a_maquina(entrada)])

    print(codigo_assemblre)

def assembre_a_maquina(instruccion):
    global registros
    binario = ""
    if instruccion[0]=="LD":
        if registros.get(instruccion[1]) != None and registros.get(instruccion[2]) != None :
            binario = "01"+registros[instruccion[1]][0]+registros[instruccion[2]][0],1
        elif registros.get(instruccion[1]) != None  and instruccion[2].find("(")!=None:
            a = "{0:b}".format(int(instruccion[2]))
            binario = "00"+registros[instruccion[1]][0]+"110"+ceros_a_la_izq(a,8),2

    return binario
leer_cod_assembler()