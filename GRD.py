from GraphReverseDefinitions2 import graph_limits, find_ticks, read_bottom, read_left
from GraphReverseImageDefinitions import make_schema_and_histogram, make_list_of_hues, make_data_weight_list, select_threshold, extract_reversed_series

if __name__ == '__main__':
    from scipy import misc
    import imageio
    from PIL import Image
    import numpy as np
    path_ejemplo = "C:/Users/Nicolás/Documents/Python/cap1.bmp"
    workfile = imageio.imread(path_ejemplo)
    box_limits = graph_limits(workfile)
    ticks = find_ticks(workfile, box_limits)
    bt_box = read_bottom(path_ejemplo, box_limits)
    lf_box = read_left(path_ejemplo, box_limits)

    img = Image.open("C:/Users/Nicolás/Documents/Python/cap1.png")
    aa = np.array(img)
    schema, histogram = make_schema_and_histogram(aa)
    data_order, data_series = make_list_of_hues(histogram)
    data_weight, data_weight_list = make_data_weight_list(histogram, data_order, data_series)
    threshold = select_threshold(data_weight_list)
    ff = extract_reversed_series(aa,data_series,threshold,schema, data_weight, data_weight_list)
    print(ticks['left'])
    print(lf_box)
    print(ticks['bottom'])
    print(bt_box)

##De aca, necesitas empezar a interpolar.
