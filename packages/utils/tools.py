import random
import glob

def get_filepath(directory, file_name):
    files = glob.glob(f"./{directory}/*")
    if file_name is None:
        file_path = random.choice(files)
    else:
        file_path = f"./{directory}/{file_name}.glb"
    if file_path in files:
        return file_path
    else:
        raise Exception('Wrong file name!')

def get_int_from_string(string):
    value = int(''.join(i for i in string if i.isdigit()))
    return value

def get_page_width(page):
    value = page.evaluate('() => document.documentElement.clientWidth')
    return value
