
def text2short(text):
    words = text.split(' ')
    file_name = words[0]
    try:
        file_name+="_"+words[1]
    except:
        ...
    try:
        file_name+="_"+words[2]
    except:
        ...
    return file_name+"..."