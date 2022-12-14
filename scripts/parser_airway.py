# import io
import sys
import tabula
import sqlite3
import pandas as pd
import math
import re
from os import path
 
# from pdfminer.converter import TextConverter
# from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.pdfpage import PDFPage

# def extract_text_from_pdf(pdf_path):
#     resource_manager = PDFResourceManager()
#     fake_file_handle = io.StringIO()
#     converter = TextConverter(resource_manager, fake_file_handle)
#     page_interpreter = PDFPageInterpreter(resource_manager, converter)
 
#     with open(pdf_path, 'rb') as fh:
#         for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
#             page_interpreter.process_page(page)
#             break
#         text = fake_file_handle.getvalue()
 
#     # close open handles
#     converter.close()
#     fake_file_handle.close()
 
#     if text:
#         return text

def airway_insert(connect, code_ru, code_en, distance):
	cursor = connect.cursor()
	cursor.execute("INSERT OR IGNORE INTO airway VALUES(:code_ru, :code_en, :distance)", 
        {"code_ru": code_ru, "code_en": code_en, "distance": distance})
	# id = cursor.lastrowid
	connect.commit()
	return code_ru

def point_insert(connect, point):
    cursor = connect.cursor()
    cursor.execute("INSERT OR IGNORE INTO point(name_ru, name_en, lat, lon) VALUES(:name_ru, :name_en, :lat, :lon)", 
		{"name_ru": point['name_ru'], "name_en": point['name_en'], "lat": point['lat'], "lon": point['lon']})
    id = cursor.lastrowid
    connect.commit()
    return point['name_ru']

def airway_point_insert(connect, point):
    cursor = connect.cursor()
    cursor.execute("INSERT OR IGNORE INTO airway_point(code_airway, code_point, minimum_altitude, width, "
        "direction_trains_forward, direction_trains_back, upper_limit, lower_limit, magnetic_track_angle_forward, "
        "magnetic_track_angle_back, \"order\") VALUES(:code_airway, :code_point, :minimum_altitude, :width, "
        ":direction_trains_forward, :direction_trains_back, :upper_limit, :lower_limit, :magnetic_track_angle_forward, "
        ":magnetic_track_angle_back, :order)", 
    {"code_airway": point['code_airway'], "code_point": point['code_point'], "minimum_altitude": point['minimum_altitude'], "width": point['width'],
        "direction_trains_forward": point['direction_trains_forward'], "direction_trains_back": point['direction_trains_back'], 
        "upper_limit": point['upper_limit'], "lower_limit": point['lower_limit'], "magnetic_track_angle_forward": point['magnetic_track_angle_forward'],
        "magnetic_track_angle_back": point['magnetic_track_angle_back'], "order": point['order']})
    connect.commit()

def airway_point_last_insert(connect, point):
    cursor = connect.cursor()
    cursor.execute("INSERT OR IGNORE INTO airway_point(code_airway, code_point, \"order\") VALUES(:code_airway, :code_point, :order)", 
    {"code_airway": point['code_airway'], "code_point": point['code_point'], "order": point['order']})
    connect.commit()
 
def parse_airway(conn, line):
    if not isinstance(line[0], str):
        return -1

    airway_line = re.match( r'^\uf020(.*)\/(.*)\s(\d*\.\d*)\s????', ' '.join(str(x) for x in line))

    if airway_line:
        name_ru = airway_line.group(1)
        name_en = airway_line.group(2)
        distance = float(airway_line.group(3))
        # airway_distance = float(line[1].split(' ')[0])
        print(name_ru, name_en, distance)
        id_airway = airway_insert(conn, name_ru, name_en, distance)
        return id_airway

    return -1

def parse_airway_point(conn, line):
    if not isinstance(line[0], str):
        return -1

    point_airway_line = re.match( r'^[\uf072|\uf070]\uf020(.*)\/(.*)\s(\d*[NS])\s(\d*[EW])', ' '.join(str(x) for x in line))
    point = {}
    if point_airway_line:
        point['name_ru'] = point_airway_line.group(1)
        point['name_en'] = point_airway_line.group(2)
        point['lat'] = point_airway_line.group(3)
        point['lon'] = point_airway_line.group(4)
        print(point)
        id_point = point_insert(conn, point)
        return id_point

    return -1

def parse_airway_point_detail(conn, lines, id_airway, id_point, order):
    attr_airway = re.search(r'\s(\d*\.?\d*)\D\s(\d*\.?\d*)\s(\w+\d*)\s(\d*\.?\d*)\s(\d*\.?\d*)\s?(\S*)?\s?(\S*)?', ' '.join(str(x) for x in lines[0]))
    attr_airway2 = re.search(r'\s(\d*\.?\d*)\D\s(\w+\d*)', ' '.join(str(x) for x in lines[1]))
    point = {}
    if attr_airway and attr_airway2:
        point['code_airway'] = id_airway
        point['code_point'] = id_point
        point['magnetic_track_angle_forward'] = attr_airway.group(1)
        point['distance'] = attr_airway.group(2)
        point['upper_limit'] = attr_airway.group(3)
        point['minimum_altitude'] = attr_airway.group(4)
        point['width'] = attr_airway.group(5)
        point['direction_trains_forward'] = attr_airway.group(6)
        point['direction_trains_back'] = attr_airway.group(7)
        point['magnetic_track_angle_back']  = attr_airway2.group(1) 
        point['lower_limit'] = attr_airway2.group(2)
        point['order'] = order
        print(point)
        airway_point_insert(conn, point)
        return True

    return False

def check_nan(line):
    new_line = []
    
    for l in line:
        if isinstance(l, str):
            new_line.append(l)
            continue

        if not math.isnan(float(l)):
            new_line.append(l)

    return new_line


if __name__ == '__main__':
    # print(extract_text_from_pdf('cbcng2008.pdf'))
    conn = sqlite3.connect('airway.db')

    if conn != None and len(sys.argv) > 1:
        file = sys.argv[1]

        if path.exists(file):
            print('Read data...')
            # df = tabula.read_pdf(file, pages="all", stream=True)
            df = tabula.read_pdf(file, pages='12-271', stream=True)
            # df = tabula.read_pdf(file, pages='12-13', stream=True)
            order = 0

            # pages
            for p in range(len(df)):
            	# rows in DataFrame
                # print(df[p].values)

                read_columns = False
                lines = []
                i = 0
                order = 0
                code_airway = 0
                code_point = 0

                while i < len(df[p]):
                    print('{0}/{1}'.format(p, i))                    

                    # Read data from header
                    line = df[p].columns
                    
                    if not read_columns:
                        code = parse_airway(conn, line)
                        read_columns = True
                        if code_airway != -1:
                            code_airway = code
                            order = 0

                    line = df[p].values[i]
                    i = i + 1

                    line = check_nan(line)
                    
                    if len(line) == 0:
                        continue

                    code = parse_airway(conn, line)
                    if code != -1:
                        code_airway = code
                        order = 0
                        continue

                    code = parse_airway_point(conn, line)
                    if code != -1:
                        code_point = code
                        lines = []
                        continue

                    if not isinstance(line[0], str):
                        continue

                    point_detail_begin_line = re.match( r'^\uf020', line[0])

                    if point_detail_begin_line:
                        lines.append(line)

                    if len(lines) == 2:
                        if parse_airway_point_detail(conn, lines, code_airway, code_point, order):
                            order = order + 1
                            code_point = 0
                        lines = []

                if code_point != 0:
                    point = {}
                    point['code_airway'] = code_airway
                    point['code_point'] = code_point
                    point['order'] = order
                    airway_point_last_insert(conn, point)

                    # isNanCodeAirway = False
                    # try:
                    #     isNanCodeAirway = math.isnan(float(df[p].loc[i][0]))
                    # except:
                    #     isNanCodeAirway = False

                    # if not isNanCodeAirway:	
                    #     code_airway = df[p].loc[i][0]
                    #     airway_insert(conn, code_airway)
                    #     order = 0

                    # isNanCodePoint = False
                    # try:
                    #     isNanCodePoint = math.isnan(float(df[p].loc[i][3]))
                    # except:
                    #     isNanCodePoint = False

                    # n = 3
                    # if isNanCodePoint:
                    #     n = 4

                    # code_state = df[p].loc[i][1]
                    # name_point = df[p].loc[i][2]    
                    # code_point = df[p].loc[i][n]
                    # lat = df[p].loc[i][n + 1]
                    # lon = df[p].loc[i][n + 2]

                    # point = {'code_state': code_state, 'name_point': name_point, 'code_point': code_point, 'lat': lat, 'lon': lon}
                    # point_insert(conn, code_airway, point, order)
                    # order = order + 1
                    # print(code_airway, code_state, name_point, code_point, lat, lon)
                # print('Insert data ot DB progress: {} %'.format(round(((p + 1) * 100) / len(df))))
                # break;
        else:
            print('File not exist!')
    conn.close()