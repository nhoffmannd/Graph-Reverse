##1234567890223456789033345678904444567890555556789066666678907777777890
##72 caracteres de ancho. Tratar de mostrar todo este texto si podemos,
##como se sugiere en la guía de estilos de Python.

def avadakedabra(argh):
    coso = 2*argh
    return coso
##Un prototipo para tener en claro como funciona definir cosas.
##def noimportaelnombre(argumentos):
##  indentación
##  return explícito
##  ESTO NO ES RUBY. RETURN TIENE QUE SER EXPLÍCITO.

##Esto acorta la definición de las funciones a 2 líneas, en vez de 4.
def new_function(ICON, NOMBRE, TECL, DESC, OBJ, MENU):
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QAction
    NEW = QAction(QIcon(ICON), NOMBRE, OBJ)
    NEW.setShortcut(TECL)
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

def find_ticks (graph, limits):

    lf_lm   =   limits[1]
    tp_lm   =   limits[2]
    rg_lm   =   limits[3]
    bt_lm   =   limits[4]

    rows    =   graph.shape[0]
    columns =   graph.shape[1]
    margin  =   5
    
    lf_lm   =   max(lf_lm-margin, 0)
    rg_lm   =   min(rg_lm+margin, columns)
    tp_lm   =   max(tp_lm-margin, 0)
    bt_lm   =   min(bt_lm+margin, rows)

    bt_ln   =   graph[lf_lm:rg_lm][bt_lm-2*margin:bt_lm][:]
    lf_ln   =   graph[lf_lm:lf_lm+2*margin][tp_lm:bt_lm][:]

    columns =   rg_lm-lf_lm
    rows    =   bt_lm-tp_lm
    
    for a in columns:
        for b in range (0:10):
            bt_hist[a] = bt_hist[a] + min(bt_ln[a][b][:])

    for a in rows:
        for b in range (0:10):
            lf_hist[a] = lf_hist[a] + min(lf_ln[b][a][:])

    ##Ahora buscamos las marquitas. Las marquitas deberian cumplir 3 condiciones:
    ##Deberían ser no únicas, negras, y de carácter regular.
    ##Para medir el negro solo, la mejor manera es usando min[:].
    ##Eso elimina todos los colores con al menos un canal luminoso.
    ##Ahora, para medir si son únicas o no, debemos usar un hash.
    bt_dc = dict()
    for a in columns:
        if bt_hist[a] in bt_dc():
            bt_dc[bt_hist[a]] += 1
        else:
            bt_dc[bt_hist[a]] = 1

    lf_dc = dict()
    for a in rows:
        if lf_hist[a] in lf_dc():
            lf_dc[lf_hist[a]] += 1
        else:
            lf_dc[lf_hist[a]] = 1

    ##Finalmente, regularidad.
    ##Ignorando singuletes y mayorías, tomamos sólo el 50% más bajo,
    ##Con cuatro estoy seguro. Armamos array de 4x2 para posicionarlas.

    marcas = np.array((4,2),0)
    current_column = 1
    current_row = 1
    start_of_tick = 1
    end_of_tick = 2
    was_on_a_tick = False

    for a in rows:
        if not (lf_dc[lf_hist[a]] == max(lf_dc)
        or lf_dc[lf_hist[a]] < 2
        or lf_hist[a] < 640):
            if was_on_a_tick == False:
                was_on_a_tick = True
                marcas[current_tick,start_of_tick] = a
        else:
            if was_on_a_tick == True:
                was_on_a_tick = False
                marcas[current_tick,end_of_tick] = a
                current_tick += 1
        if current_tick < 4:
            break

    for a in columns:
        if not (bt_dc[bt_hist[a]] == max(bt_dc)
        or bt_dc[bt_hist[a]] < 2
        or bt_hist[a] < 640
        or new_column == True):
            marcas[current_row] = a
            
