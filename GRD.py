from GraphReverseDefinitions2 import graph_limits, find_ticks, read_bottom, read_left, fix_ticks, fix_box
from GraphReverseImageDefinitions import make_schema_and_histogram, make_list_of_hues, make_data_weight_list, select_threshold, extract_reversed_series
from GraphReverseDefinitions3 import ciclos_presentes_en_cada_serie

if __name__ == '__main__':
    from scipy import misc
    import imageio
    from PIL import Image
    import numpy as np
    path_ejemplo = "D:/Python/cap1.bmp"
    procesar_texto = True
    corregir_texto = True
    procesar_imagen = True
    mostrar_datos = True

    if procesar_texto:
        workfile = imageio.imread(path_ejemplo)
        box_limits = graph_limits(workfile)
        ticks = find_ticks(workfile, box_limits)
        bt_box = read_bottom(path_ejemplo, box_limits)
        lf_box = read_left(path_ejemplo, box_limits)
        ##Con esto los tenemos posicionados respecto a la imagen entera.
        if corregir_texto:
            ticks = fix_ticks(ticks,box_limits)
            bt_box, lf_box = fix_box(bt_box,lf_box,box_limits)
        if mostrar_datos:
            ##Hora de construir el pedazo que falta: interpolar.
            print("ticks on the left side: "    + str(ticks['left']))
            print("left box: "                  + str(lf_box))
            print("ticks on the bottom side: "  + str(ticks['bottom']))
            print("bottom box: "                + str(bt_box))

    if procesar_imagen:    
        ##Este segmento trabaja con un png, y se encarga de la parte gráfica.
        img = Image.open("D:/Python/cap1.png")
        aa = np.array(img)
        schema, histogram = make_schema_and_histogram(aa)
        data_order, data_series = make_list_of_hues(histogram)
        data_weight, data_weight_list = make_data_weight_list(histogram, data_order, data_series)
        threshold = select_threshold(data_weight_list)
        ff = extract_reversed_series(aa,data_series,threshold,schema, data_weight, data_weight_list)
        ciclos_presentes_en_cada_serie(ff)
