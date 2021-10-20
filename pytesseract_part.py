##1234567890113456789022245678903333567890444446789055555578906666666890
##1234567890113456789022245678903333567890444446789055555578906666666890
##1234567890113456789022245678903333567890444446789055555578906666666890
def reduced_array(tesseract_string):
    short_array = []
    split_string = tesseract_string.split("\n")
    work_array = []
    whitelist = ["left","top","width","height","text"]
    schema = {}
    for jj in range(len(split_string)):
        work_array = split_string[jj].split("\t")
        final_array = []
        if jj == 0:
            for kk in range(len(work_array)):
                if work_array[kk] in whitelist:
                    schema[work_array[kk]]=kk
            short_array += [whitelist]
        else:
            reduced_array = []
            if not work_array[-1] == "":
                for kk in range(len(whitelist)):
                    reduced_array += [work_array[schema[whitelist[kk]]]]
                short_array += [reduced_array]
    return short_array

##1234567890113456789022245678903333567890444446789055555578906666666890
##1234567890113456789022245678903333567890444446789055555578906666666890
##1234567890113456789022245678903333567890444446789055555578906666666890
def tesseract_get(picture):
    from PIL import Image
    import pytesseract

    tesseract_path = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    imc = picture
    imc = imc.convert("L")

    data_grid = pytesseract.image_to_data(imc)
    return data_grid

##1234567890113456789022245678903333567890444446789055555578906666666890
##1234567890113456789022245678903333567890444446789055555578906666666890
##1234567890113456789022245678903333567890444446789055555578906666666890
