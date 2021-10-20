##1234567890223456789033345678904444567890555556789066666678907777777890
##72 caracteres de ancho. Tratar de mostrar todo este texto si podemos,
##como se sugiere en la guía de estilos de Python.
##Un prototipo para tener en claro como funciona definir cosas.
##def noimportaelnombre(argumentos):
##  indentación
##  return explícito
##  ESTO NO ES RUBY. RETURN TIENE QUE SER EXPLÍCITO.



##Esto acorta la definición de las funciones a 2 líneas, en vez de 4.
def new_function(ICON, NOMBRE, TECLA, DESC, OBJ, MENU):
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QAction
    NEW = QAction(QIcon(ICON), NOMBRE, OBJ)
    NEW.setShortcut(TECLA)
    NEW.setStatusTip(DESC)
    MENU.addAction(NEW)
    return NEW

##Esto procesa los límites de los gráficos.
def graph_limits(graph):
    import PIL
    import numpy
    columns = graph.shape[1]
    rows = graph.shape[0]
    clpsd_columns   = numpy.full((columns),0)
    clpsd_rows      = numpy.full((rows),0)
    
    for a in range (0, columns):
        for b in range (0, rows):
            clpsd_columns[a] = clpsd_columns[a]+max(graph[b][a][:])

    for a in range (0, rows):
        for b in range (0, columns):
            clpsd_rows[a] = clpsd_rows[a]+max(graph[a][b][:])
            
    half_cols = int(columns/2)
    half_rows = int(rows/2)

    ##Buscamos las posiciones.    
    minimum_top = min(clpsd_rows[0:half_rows])
    minimum_left = min(clpsd_columns[0:half_cols])
    minimum_right = min(clpsd_columns[half_cols:columns])
    minimum_bottom = min(clpsd_rows[half_rows:rows])

    #Límites declarados.
    left_pos = -1
    top_pos = -1
    right_pos = -1
    bottom_pos = -1
    cont_left = True
    cont_right = True
    cont_top = True
    cont_bottom = True

    ##Buscar la columna mas oscura, que indudablemente será el borde.
    for a in range (0, half_cols):
        left_col = a
        right_col = columns - a - 1
        percentage_left = abs(minimum_left/clpsd_columns[left_col])
        percentage_right = abs(minimum_right/clpsd_columns[right_col])
        if percentage_left<1.05 and percentage_left>0.95 and cont_left:
            left_pos = left_col
            cont_left = False
        if percentage_right<1.05 and percentage_right>0.95 and cont_right:
            right_pos = right_col
            cont_right = False
        if not (cont_left or cont_right):
            break

    ##Repetir para las filas.
    for a in range (0, half_rows):
        top_row = a
        bottom_row = rows - a - 1
        percentage_top = abs(minimum_top/clpsd_rows[top_row])
        percentage_bottom = abs(minimum_bottom/clpsd_rows[bottom_row])
        if percentage_top<1.05 and percentage_top>0.95 and cont_top:
            top_pos = top_row
            cont_top = False
        if percentage_bottom<1.05 and percentage_bottom>0.95 and cont_bottom:
            bottom_pos = bottom_row
            cont_bottom = False
        if not (cont_top or cont_bottom):
            break

    ##Devolver los límites.
    limits=[left_pos, top_pos, right_pos, bottom_pos]

    return limits

def dame():
    from scipy import misc
    import PIL
    return misc.imread("C:/Users/Nicolás/Documents/Python/cap1.bmp")

##1234567890223456789033345678904444567890555556789066666678907777777890
##1234567890223456789033345678904444567890555556789066666678907777777890
##1234567890223456789033345678904444567890555556789066666678907777777890
def find_ticks (graph, limits):
    import PIL
    import numpy as np
    
    lf_lm   =   limits[0]
    tp_lm   =   limits[1]
    rg_lm   =   limits[2]
    bt_lm   =   limits[3]

    rows    =   graph.shape[0]
    columns =   graph.shape[1]
    margin  =   5
    
    lf_lm   =   max(lf_lm-margin, 0)
    rg_lm   =   min(rg_lm+margin, columns)
    tp_lm   =   max(tp_lm-margin, 0)
    bt_lm   =   min(bt_lm+margin, rows)

    #Estamos confundiendo columnas y filas.

    bt_ln   =   graph[bt_lm-2*margin:bt_lm, lf_lm:rg_lm, :]
    columns =   rg_lm-lf_lm
    bt_hist =   np.zeros((columns))

    
    lf_ln   =   graph[ tp_lm:bt_lm, lf_lm:lf_lm+2*margin, :]
    rows    =   bt_lm-tp_lm
    lf_hist =   np.zeros((rows))

    ##Medir marquitas de la izquierda y del fondo. Son distintas.
    for a in range (0, columns):
        for b in range (0, 10):
            bt_hist[a] = bt_hist[a] + max(bt_ln[b][a][:])

    for a in range (0, rows):
        for b in range (0, 10):
            lf_hist[a] = lf_hist[a] + max(lf_ln[a][b][:])
            
    ##Ahora buscamos las marquitas. 3 CONDICIONES:
    ##Deberían ser no únicas, negras, y de carácter regular.
    ##Para medir el negro solo, la mejor manera es usando max[:].
    ##Eso elimina todos los colores con al menos un canal luminoso.
    ##Ahora, para medir si son únicas o no, debemos usar un hash.
    ##bt_dc tiene intensidades, mide las frecuencias d cada intensidad.
    ##Finalmente, regularidad.
    ##Los singuletes son inevitables.
    ##La mayoría tiene la línea negra base pasante en el medio.
    ##Todo lo que sea más oscuro que el medio es una marquita.
    left_ticks = ticks_only(lf_hist, margin) ##, lf_lm)
    bottom_ticks = ticks_only(bt_hist, margin) ##, tp_lm)
    ticks_map = {'left': left_ticks, 'bottom': bottom_ticks}
    return(ticks_map)

##1234567890223456789033345678904444567890555556789066666678907777777890
##1234567890223456789033345678904444567890555556789066666678907777777890
##1234567890223456789033345678904444567890555556789066666678907777777890
def ticks_only(aa_hist, margin, skip=0, invert = False):
    import numpy as np
    limit = len(aa_hist)

    bt_dc = dict()
    for a in range(0, limit):
        if aa_hist[a] in bt_dc:
            bt_dc[aa_hist[a]] += 1
        else:
            bt_dc[aa_hist[a]] = 1

    bt_dcc = bt_dc
    bt_dc = {}

    current_max = 0
    cutoff_key = 0
    
    for key in bt_dcc:
        if bt_dcc[key] > current_max:
            current_max = bt_dcc[key]
            cutoff_key = key
    
    for key in bt_dcc:
        if  key < cutoff_key*0.9:
            bt_dc[key] = bt_dcc[key]

    ##De acá deberíamos tener una regularidad.
    ticks = 0
    for key in bt_dc:
        ticks += bt_dc[key]
    
    marcas = np.zeros((ticks,2))
    current_column = 1
    current_row = 1
    start_of_tick = 0
    end_of_tick = 1
    was_on_a_tick = False
    current_tick = 0

    for a in range(0, limit):
        if aa_hist[a] in bt_dc:
            marcas[current_tick, 0] = a
            marcas[current_tick, 1] = 2*margin*255 - aa_hist[a]
            current_tick += 1

    tick_position = []
    positions_included = 0
    denominator = 0
    first_position = True
    current_add = 0
    denom_add = 0

    for a in range(0, ticks):
        current_add = marcas[a,0] * marcas[a,1]
        denom_add = marcas[a,1]
        if first_position:
            tick_position += [current_add]
            denominator    = denom_add
            first_position = False
        else:
            if marcas[a,0] > (marcas[a-1,0] +1):
                tick_position[-1] = tick_position[-1] / denominator
                tick_position += [current_add]
                denominator = denom_add
            else:
                tick_position[-1] = tick_position[-1] + current_add
                denominator += denom_add
        if a == (ticks-1):
            tick_position[-1] = tick_position[-1] / denominator

    tick_number = len(tick_position)
    tick_span = []
    general_span = []
    real_tick_number = 0

    for a in range(1, tick_number):
        tick_span+=[tick_position[a]-tick_position[a-1]]

    ##elegimos el que más se parezca a la media.
    ##NECESITAMOS QUE SEA LA MEDIANA PARA IGNORAR CRUCES ESPURIOS.
    ##Con esto tenemos que encontrar un ritmo aproximado.
    ##Vamos a hacer la suposición de que la moda de la distribución
    ##es el ritmo.
    ##Medir la separación entre las posiciones.
    ##Luego ir dividiendo la separación entre el primero y el último.

    full_span = tick_position[-1]-tick_position[0]
    from numpy import median as npmedian
    target_span = npmedian(tick_span)
    final_error = -1
    current_error = -1
    last_error = 0
    select_position = 0
    chosen_span = 0
    
    for a in range(1, tick_number):
        general_span = full_span / a
        if (current_error < 0):
            current_error = abs(general_span - target_span)
            final_error = current_error
            chosen_span = general_span
        else:
            current_error = abs(general_span - target_span)
            if (current_error < final_error):
                final_error = current_error
                chosen_span = general_span
    
    ##Habiendo elegido eso, vamos a ignorar toda marquita
    ##que no sea múltipo aproximado del span general.
    ##Vamos a suponer que no falta ninguna: para cada una,
    ##se prueba el último múltiplo, y el siguiente.
    ##Si su error para el último múltiplo es menor que el del anterior,
    ##lo reemplaza. Si no, pasa para el siguiente.

    base_value = 0

    ticks_col = 0
    error_col = 1
    multi_col = 2

    cur_tick = tick_position[0]
    cur_err = 0
    cur_mult = 0

    tick_number = len(tick_position)
    final_tick_values=np.zeros((tick_number,3))
    
    for a in range(0, tick_number):
        if a == 0:
            final_tick_values[cur_mult, ticks_col]=cur_tick
            final_tick_values[cur_mult, error_col]=cur_err
            final_tick_values[cur_mult, multi_col]=cur_mult
            cur_mult += 1
        else:
            cur_tick = tick_position[a]
            cur_err  = abs(tick_position[a] - tick_position[0])
            cur_err  = abs(cur_err - cur_mult*chosen_span)
            if not (final_tick_values[cur_mult, multi_col] == 0):
                if (cur_err > final_tick_values[cur_mult,error_col]):
                    cur_mult+=1
                    cur_err = abs(tick_position[a] - tick_position[0])
                    cur_err = abs(cur_err - cur_mult*chosen_span)
            final_tick_values[cur_mult, error_col] = cur_err
            final_tick_values[cur_mult, ticks_col] = cur_tick
            final_tick_values[cur_mult, multi_col] = cur_mult

    total = len(final_tick_values)

    if invert:
        skip = -skip
    
    for a in range(0, total):
        b = final_tick_values[a, ticks_col]
        final_tick_values[a, ticks_col] = b + skip - margin
    
    return_tick_positions = final_tick_values[:, 0]    
    return return_tick_positions

##1234567890223456789033345678904444567890555556789066666678907777777890
##1234567890223456789033345678904444567890555556789066666678907777777890
##1234567890223456789033345678904444567890555556789066666678907777777890
def read_bottom(image_path, bb):
    from PIL import Image
    from pytesseract_part import tesseract_get
    wg = Image.open(image_path)
    bb_left = bb[0]
    bb_top = bb[3]
    bb_right = bb[2]
    bb_bottom = wg.size[1]
    bottom_slice = wg.crop((bb_left, bb_top, bb_right, bb_bottom))
    get = tesseract_get(bottom_slice)
    get = string_a_tabla(get)
    return get
    #pasamos a pytesseract_part lo que tiene abajo de la línea.

def read_left(image_path,bb):
    from PIL import Image
    from pytesseract_part import tesseract_get, reduced_array
    wg = Image.open(image_path)
    bb_left = 46    
    bb_top = bb[1]
    bb_right = bb[0]
    bb_bottom = bb[3]
    left_slice = wg.crop((bb_left, bb_top, bb_right, bb_bottom))
    get = tesseract_get(left_slice)
    get = reduced_array(get)
    get = puntos_medios(get, {"height":0.5, "top":1})
    return get
    #pasamos a pytesseract_part lo que tiene abajo de la línea.

def puntos_medios(arr,direccion):
    definiciones = arr[0]
    mult = {}
    puntos = {}
    for kk in range(len(definiciones)):
        if definiciones[kk] in direccion:
            mult[kk] = direccion[definiciones[kk]]
        if definiciones[kk] == "text":
            mult["text"] = kk
    for kk in range(1,len(arr)):
        valor = 0
        for jj in range(len(definiciones)):
            if jj in mult:
                valor += int(arr[kk][jj]) * float(mult[jj])
        texto = arr[kk][mult["text"]]
        if texto.isdigit():
            puntos[valor] = arr[kk][mult["text"]]
    return puntos

def string_a_tabla(string_a_tabla):
    import numpy as np
    rows = string_a_tabla.count('\n') + 1
    cols = string_a_tabla.count('\t')
    cols = int((cols / rows))+1
    rows -= 1
    row = 0
    col = 0
    tabla = np.zeros((rows,cols))
    line = ''
    char = ''
    header = {}
    linepusher = {}
    last = len(string_a_tabla)
    for a in range(0,last):
        char = string_a_tabla[a]
        if (char == '\n' or char == '\t'):
            if row == 0:
                header[col] = line
            else:
                if (char == '\n'):
                    linepusher[row-1] = line
                else:
                    if not line == '':
                        line2 = int(float(line))
                        tabla[row-1,col] = line2
            if (char == '\n'):
                row += 1
                col = 0
            if (char == '\t'):
                col += 1
            line = ''
        else:
            line += char
            char = ''
    linepusher[row-1] = line
    ##print(header)
    ##print(linepusher)
    posiciones = reducir_tabla(tabla, linepusher)
    return posiciones

def reducir_tabla(tabla, lineas):
    import numpy as np
    first = True
    total = len(lineas)
    for a in range(0, total):
        if first:
            first = False
            claves  = [False]
        else:
            claves += [False]
    
    for key in lineas:
        claves[key] = lineas[key]

    for a in range(0, total):
        b = total-a-1
        if (not (claves[b].isnumeric())):
            del claves[b]
            tabla = np.delete(tabla, b, 0)

    total = len(claves)
    posiciones = {}
    for a in range(0, total):
        posicion = tabla[a, 6] + tabla[a, 8]/2
        posiciones[posicion] = claves[a]
    return posiciones

def fix_ticks(tick_list,correction):
    left_correction = correction[1]
    top_correction  = correction[0]
    corrected_ticks = {}
    corrected_ticks['left'] = tick_list['left']
    corrected_ticks['bottom']  = tick_list['bottom']
    for each in range(len(corrected_ticks['left'])):
        corrected_ticks['left'][each] += left_correction
    for each in range(len(corrected_ticks['bottom'])):
        corrected_ticks['bottom'][each] += top_correction
    return corrected_ticks

def fix_box(bt_box,lf_box,correction):
    left_correction = correction[0]
    top_correction  = correction[1]
    bt_box_corrected = {}
    lf_box_corrected = {}
    for each in bt_box:
        bt_box_corrected[each + left_correction] = bt_box[each]
    for each in lf_box:
        lf_box_corrected[each +  top_correction] = lf_box[each]
    return bt_box_corrected, lf_box_corrected

##1234567890223456789033345678904444567890555556789066666678907777777890
##1234567890223456789033345678904444567890555556789066666678907777777890
##1234567890223456789033345678904444567890555556789066666678907777777890
##Acortame esto de clavarle ejemplo() cada vez que lo toco.
if __name__ == '__main__':
    from scipy import misc
    import imageio
    path_ejemplo = "C:/Users/Nicolás/Documents/Python/cap1.png"
    workfile = imageio.imread(path_ejemplo)
    box_limits = graph_limits(workfile)
    ticks = find_ticks(workfile, box_limits)
    bt_box = read_bottom(path_ejemplo, box_limits)
    lf_box = read_left(path_ejemplo, box_limits)

    print(ticks['left'])
    print(lf_box)
    print("")
    print(ticks['bottom'])
    print(bt_box)
    
