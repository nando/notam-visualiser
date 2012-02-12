import classes
import os
import re

def validate(source):
    regex = re.compile('<.*>Q\) EG(PX|TT)/Q(A[^0-9a-zBGIJKMQSWY]|' + \
    'C[AEGLMPRST]|F[^0-9a-zEIJKNQRVXY]|I[DGILMOSTUWXY]|L[^0-9a-zGNOQU]|' + \
    'M[^0-9a-zEFIJLOQVYZ]|N[ABCDFLMNOTVX]|O[ABELR]|P[^0-9a-zBCEGJKNQSVWY]|' + \
    'R[ADOPRT]|S[ABCEFLOPSTUVY]|W[^0-9a-zHIKNOQRUWXY])' + \
    '(A[^0-9a-zABEIJLQTVYZ]|C[^0-9a-zBJKNQUVWXYZ]|H[A-Z]|' + \
    'L[^0-9a-zJMOQUYZ]|XX)/IV/(N?BO|B|M)/(A(E|W)?|E|W)/[0-9]{3}/[0-9]{3}/' + \
    '[0-9]{4}(N|S)[0-9]{5}(E|W)[0-9]{3}</.*>')
    if regex.search(source) != None:
        return True
    else:
        return False

def extract(source):
    notam_list = []
    temp_file0 = open('~temp0.txt', 'w+')
    temp_file1 = open('~temp1.txt', 'w+')
    temp_file0.write(re.sub('<.*?>', '', source))
    temp_file0.seek(0)
    line0 = temp_file0.readline()
    regex = re.compile('[QABCDEFG]\) ')
    while line0 != '':
        if regex.match(line0):
            temp_file1.write(line0.strip() + '\n')
            if line0.startswith('E) '):
                line1 = temp_file0.readline()
                while line1 != '\n':
                    temp_file1.write(line1.strip() + '\n')
                    line1 = temp_file0.readline()
                temp_file1.write('\n')
        line0 = temp_file0.readline()
    temp_file1.seek(0)
    notam = ''
    line = temp_file1.readline()
    if temp_file1.readline() == '':
        notam_list.append(line)
    if os.name == 'posix':
        while line != '':
            if line != '\n':
                notam += line
            else:
                notam_list.append(notam)
                notam = ''
            line = temp_file1.readline()
    elif os.name == 'nt':
        while line != '':
            if line.startswith('Q) '):
                notam_list.append(line)
            line = temp_file1.readline()
    temp_file0.close()
    temp_file1.close()
    os.remove('~temp0.txt')
    os.remove('~temp1.txt')
    return notam_list

def name(path, wild_card):
    if path[-4 : ] == wild_card[1 : ]:
        return path[ : -4] + wild_card[1 : ]
    else:
        return path + wild_card[1 : ]
    
def normalize(file_path):
    raw_path = raw(file_path)
    directories = re.sub(r'\\\\', r'\\', raw_path).split('\\')
    index = 0
    for index in range(len(directories)):
        if directories[index].find(' ') != -1:
            directories[index] = '\"' + directories[index] + '\"'
    path = '\\'.join(directories)
    return path

def raw(text):
    escape_characters = {'\a' : r'\a', '\b' : r'\b', '\c' : r'\c', \
    '\f' : r'\f', '\n' : r'\n', '\r' : r'\r', '\t' : r'\t', '\v' : r'\v', \
    '\\' : r'\\', '\?' : r'\?', '\'' : r'\'', '\"' : r'\"', '\0' : r'\0'}
    raw_text = ''
    index = 0
    for index in range(len(text)):
        if text[index] in escape_characters:
            raw_text += escape_characters[text[index]]
        else:
            raw_text += text[index]
    return raw_text

def generate(information_list):
    notam_lines = information_list[0]
    
    radius = [0]
    lower_limit = [0]
    
    document_name = information_list[1]
    document_description = information_list[2]
    document_visibility = True
    document_open = True
    
    placemark_name = information_list[3]
    placemark_description = information_list[4]
    placemark_visibility = True
    
    poly_style_id = 'Restricted_Aerodrome'
    poly_style_color = '80ffff00'
    poly_style_fill = True
    poly_style_outline = True
    
    look_at_heading = 0
    look_at_tilt = 60
    look_at_altitude_mode = 'absolute'
    
    point_polygon_extrude = True
    point_polygon_altitude_mode = 'absolute'
    
    file_location = information_list[5]
    width_constant = 4
    indent_width = 0
    
    notam = classes.NOTAM()
    latitude = classes.DMS()
    longitude = classes.DMS()
    deg_dec = classes.DegDec()
    document = classes.Document()
    placemark = classes.Placemark()
    poly_style = classes.PolyStyle()
    look_at = classes.LookAt()
    point_polygon = classes.PointPolygon()
    kml_file = classes.KMLFile()
    
    notam.set_notam_lines(notam_lines)
    notam.extract_q_line_info(latitude, longitude, radius)
    notam.extract_f_line_info(lower_limit, notam.extract_lower_height_limit())
    notam.extract_g_line_info(deg_dec, notam.extract_upper_height_limit())
    
    deg_dec.set_latitude(latitude.convert_coordinate())
    deg_dec.set_longitude(longitude.convert_coordinate())
    deg_dec.set_radius(deg_dec.convert_radius(radius))
    
    document.set_name(document_name)
    document.set_description(document_description)
    document.set_visibility(document_visibility)
    document.set_open(document_open)
    
    placemark.set_name(placemark_name)
    placemark.set_description(placemark_description)
    placemark.set_visibility(placemark_visibility)
    
    poly_style.set_id(poly_style_id)
    poly_style.set_color(poly_style_color)
    poly_style.set_fill(poly_style_fill)
    poly_style.set_outline(poly_style_outline)
    
    look_at.set_latitude(deg_dec.get_latitude())
    look_at.set_longitude(deg_dec.get_longitude())
    look_at.set_altitude(deg_dec.get_altitude())
    look_at.set_heading(look_at_heading)
    look_at.set_tilt(look_at_tilt)
    look_at.set_range(look_at.convert_to_range(deg_dec.get_radius()))
    look_at.set_altitude_mode(look_at_altitude_mode)
    
    point_polygon.set_latitude(deg_dec.get_latitude())
    point_polygon.set_longitude(deg_dec.get_longitude())
    point_polygon.set_altitude(deg_dec.get_altitude())
    point_polygon.set_extrude(point_polygon_extrude)
    point_polygon.set_altitude_mode(point_polygon_altitude_mode)
    
    kml_file.set_file_location(file_location)
    kml_file.set_width_constant(width_constant)
    kml_file.set_indent_width(indent_width)
    kml_file.create_kml_source(document, poly_style, placemark, latitude, \
    longitude, look_at, point_polygon, deg_dec)
    