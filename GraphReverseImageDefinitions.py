from PIL import Image
import numpy as np
#from matplotlib import pyplot as plt

def make_schema_and_histogram(aa):
    height= aa.shape[0]
    width = aa.shape[1]
    schema = np.zeros([height, width])
    histogram = {}
    jj = 0
    for y in range(height):
        for x in range(width):
            px = to_hue(get_rgb(aa,y,x))
            jj = int(px)
            schema[y,x] = jj
            if jj in histogram:
                histogram[jj] += 1
            else:
                histogram[jj] = 1
    return schema, histogram

def get_rgb(arraypic,he,le):
    triad = [arraypic[he,le,0], arraypic[he,le,1], arraypic[he,le,2]]
    return triad

def to_hue(triad):
    R_ = triad[0] / 255.0
    G_ = triad[1] / 255.0
    B_ = triad[2] / 255.0
    M_ = max(R_, G_, B_)
    m_ = min(R_, G_, B_)
    H_ = 0.0
    rr = M_ - m_
    if rr == 0.0:
        H_ = -100.0
        return H_
    if   (R_ == M_):
        H_ = 0.0 + (G_ - B_) / rr
    elif (G_ == M_):
        H_ = 2.0 + (B_ - R_) / rr
    elif (B_ == M_):
        H_ = 4.0 + (R_ - G_) / rr
    if H_ < 0.0:
        H_ = H_ + 6.0
    H_ = H_ * 60.0
    return H_

def successive_hue(hist,ii,vv):
    if ii in hist:
        if hist[ii]<vv:
            return True
    return False

def make_list_of_hues(histogram):
    data_order = list(histogram.keys())
    data_order.sort()
    data_series = {0: [0, 0]}
    data_series_current = 0
    hist_copy = histogram.copy()
    maximum_value = max(list(hist_copy.values()))
    hist_used = set()
    while len(hist_copy) != 0:
        for kk in histogram.keys():
            if not kk in hist_used:
                if histogram[kk] == maximum_value:
                    ii = kk
                    data_series[data_series_current] = [ii, ii]
                    vv = histogram[kk]
                    ii = kk + 1
                    while successive_hue(hist_copy,ii,vv):
                        data_series[data_series_current][1] = ii
                        vv = histogram[ii]
                        hist_used.add(ii)
                        hist_copy.pop(ii)
                        ii = ii + 1
                    vv = hist_copy[kk]
                    ii = kk - 1
                    while successive_hue(hist_copy,ii,vv):
                        data_series[data_series_current][0] = ii
                        vv = histogram[ii]
                        hist_used.add(ii)
                        hist_copy.pop(ii)
                        ii -= 1
                    hist_used.add(kk)
                    hist_copy.pop(kk)
                    data_series_current += 1
                    if len(hist_copy) != 0:
                        maximum_value = max(list(hist_copy.values()))
    return data_order, data_series

def make_data_weight_list(histogram, data_order, data_series):
    data_weight = {}
    for ii in data_order:
        sum_weight = histogram[ii]
        for jj in data_series:
            hue_range = data_series[jj]
            if ii <= hue_range[1] and ii>= hue_range[0]:
                if jj in data_weight:
                    data_weight[jj] += histogram[ii]
                else:
                    data_weight[jj] = histogram[ii]
    data_weight_list = []
    for ii in data_weight:
        if ii != 0:
            data_weight_list.append(data_weight[ii])
    data_weight_list.sort()
    return data_weight, data_weight_list

def select_threshold(data_weight_list):
    threshold = 0
    maximum_range = len(data_weight_list)
    for ii in range(maximum_range):
        if ii != 0:
            jj = maximum_range-ii
            kk = maximum_range-ii-1
            if data_weight_list[jj]/data_weight_list[kk] >= 5:
                threshold = data_weight_list[jj]
                break
    return threshold

def depict_series(aa,data_series,threshold,schema):
    bb = {}
    height= aa.shape[0]
    width = aa.shape[1]
    for series in data_series:
        dws = data_weight[series]
        if (dws >= threshold) and (dws in data_weight_list):
            bb[series] = np.zeros((aa.shape),dtype='uint8')
    for y in range(height):
        for x in range(width):
            px = schema[y,x]
            for series in bb.keys():
                hue_range = data_series[series]
                if (px <= hue_range[1] and px >= hue_range[0]):
                    bb[series][y,x] = [255,255,255,255]
    return bb

def extract_reversed_series(aa,data_series,threshold,schema, data_weight, data_weight_list):
    bb = {}
    cc = {}
    dd = {}
    
    height = aa.shape[0]
    width  = aa.shape[1]
    for series in data_series:
        dws = data_weight[series]
        if (dws >= threshold) and (dws in data_weight_list):
            cc[series] = np.zeros([height,width])
            dd[series] = np.zeros([4,width])
    
    for y in range(height):
        for x in range(width):
            px = schema[y,x]
            for series in cc.keys():
                hue_range = data_series[series]
                if (px <= hue_range[1] and px >= hue_range[0]):
                    cc[series][y,x] = 1
    
    for x in range(width-1,0,-1):
        for series in cc.keys():
            started = False
            finished = False
            for y in range(height-1,0,-1):
                if cc[series][y,x] == 1:
                    if not started:
                        started = True
                    dd[series][1,x] = dd[series][1,x]+1
                    dd[series][2,x] = dd[series][2,x]+y
                    dd[series][3,x] = y-5
                else:
                    if started:
                        if (x == (width - 1)):
                            finished = True
                        if dd[series][3,x+1] == 0:
                            finished = True
                        if y < dd[series][3,x+1]:
                            finished = True
                        if finished:
                            break;
            zz = dd[series][1,x]
            if zz == 0:
                dd[series][0,x] = 0
            else:
                dd[series][0,x] = dd[series][2,x]/zz
                
    ff = {}
    for series in dd.keys():
        ff[series] = dd[series][0,:]
    return ff

def overlay_series(bb,ff):
    for series in ff.keys():
        for x in range(ff[series].shape[0]):
            eey = int(ff[series][x])
            if not eey == 0:
                bb[series][eey,x] = [255, 0, 0, 255]
    return bb

def visualize_threshold(aa, bb):
    cc = aa
    for elem in bb:
        cc = np.concatenate((cc,bb[elem]), axis = 1)
    img = Image.fromarray(cc, 'RGBA')
    img.show()

##MAIN.
if __name__ == '__main__':
    img = Image.open("C:/Users/Nicolás/Documents/Python/cap1.png")
    aa = np.array(img)
    schema, histogram = make_schema_and_histogram(aa)
    data_order, data_series = make_list_of_hues(histogram)
    data_weight, data_weight_list = make_data_weight_list(histogram, data_order, data_series)
    threshold = select_threshold(data_weight_list)
    ff = extract_reversed_series(aa,data_series,threshold,schema, data_weight, data_weight_list)

    ##Esta parte no hace falta ya.
    bb = depict_series(aa,data_series,threshold,schema)
    bb = overlay_series(bb,ff)
    visualize_threshold(aa,bb)
