#imports



#// VARIABLES GLOBALES //

#REGISTROS, donde se guarda su código y su contenido EN UN ARREGLO
# ejemplo poner NZ = 1, -->banderas_estado["NZ"][1] = "1"
registros = { "A":["000",""], "B":["000",""], "C":["001",""], "D":["010",""], "E":["011",""], "H":["100",""], "L":["101",""]}

#registros 16 bits
registros_16 = {"BC":["00",""],"DE":["01",""],"HL":["10",""],"SP":["11",""]}

#banderas de estado
banderas_estado = {"NZ":["000",""],"Z":["001",""],"NC":["010",""],"C":["011",""],"PO":["100",""],"PE":["101",""],
                   "P":["110",""],"M":["111",""] }

