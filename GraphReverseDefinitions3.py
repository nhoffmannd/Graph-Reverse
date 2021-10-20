##determina el espacio máximo de ciclos extraíbles del array provisto.
def ciclos_presentes_en_cada_serie(dict_de_series):
    limites_de_series = {}
    for each in dict_de_series.keys():
        len_de_series = len(dict_de_series[each])
        principio = False
        final = False
        for ii in range(len_de_series):
            iii = len_de_series-1-ii
            if not (dict_de_series[each][ii] == 0) and (principio == False):
                principio = ii
            if not dict_de_series[each][iii] == 0 and (final == False):
                final = iii
            if not (principio == False) and not (final == False):
                break
        print(str(principio)+" hasta "+str(final))
        
def extrapolar_final(posicion,ticks_horizontales):
    return 1
    
##1234567890123456789012345678901234567890123456789012345678901234567890
##1234567890123456789012345678901234567890123456789012345678901234567890
##1234567890123456789012345678901234567890123456789012345678901234567890
