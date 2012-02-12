import classes

q_line = 'Q) EGTT/QAZCA/IV/NBO/AE/000/030/5212N00137W005'
f_line = ''
g_line = ''

# document_name = raw_input()
document_name = 'Test Document'
# document_description = raw_input()
document_description = 'A file documenting all testing.'
document_visibility = True
document_open = True

# placemark_name = raw_input()
placemark_name = 'Test Placemark'
# placemark_description = raw_input()
placemark_description = 'The placemarks generated during \
the testing on different NOTAMs.'
placemark_visibility = True

poly_style_id = 'Restricted_Aerodrome'
poly_style_color = '80ffff00'
poly_style_fill = True
poly_style_outline = True

# look_at_latitude = deg_dec.get_latitude()
# look_at_longitude = deg_dec.get_longitude()
# look_at_altitude = deg_dec.get_altitude()
look_at_heading = 0
look_at_tilt = 60
# look_at_range = radius[0] * 1852 * 2
look_at_altitude_mode = 'absolute'

# point_polygon_latitude = deg_dec.get_latitude()
# point_polygon_longitude = deg_dec.get_longitude()
# point_polygon_altitude = deg_dec.get_altitude()
point_polygon_extrude = True
point_polygon_altitude_mode = 'absolute'

# print 'enter file_location: ',
# file_location = raw_input()
file_location = 'test01.kml'
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

radius = [0]
lower_limit = [100]

default_altitude = 250.0

notam.set_q_line(q_line)
notam.set_f_line(f_line)
notam.set_g_line(g_line)

coordinates_string = notam.extract_coordinates_string()

notam.extract_q_line_info(latitude, longitude, radius)
notam.extract_f_line_info(lower_limit)
notam.extract_g_line_info(deg_dec, default_altitude)

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

# debug_file = raw_input()
debug_file_name = 'debug.txt'

debug_file = open(debug_file_name, 'w')

debug_file.write('q_line: %s\n' % notam.get_q_line())
debug_file.write('f_line: %s\n' % notam.get_f_line())
debug_file.write('g_line: %s\n' % notam.get_g_line())
debug_file.write('\n')
debug_file.write('validate_q_line: %s\n' % notam.validate_q_line(q_line))
debug_file.write('validate_f_line: %s\n' % notam.validate_f_line(f_line))
debug_file.write('validate_g_line: %s\n' % notam.validate_g_line(g_line))
debug_file.write('\n')
debug_file.write('coordinates_string: %s\n' % coordinates_string)
debug_file.write('\n')
debug_file.write('latitude.degrees: %s\n' % latitude.get_degrees())
debug_file.write('latitude.minutes: %s\n' % latitude.get_minutes())
debug_file.write('latitude.direction: %s\n' % latitude.get_direction())
debug_file.write('\n')
debug_file.write('longitude.degrees: %s\n' % longitude.get_degrees())
debug_file.write('longitude.minutes: %s\n' % longitude.get_minutes())
debug_file.write('longitude.direction: %s\n' % longitude.get_direction())
debug_file.write('\n')
debug_file.write('radius: %s\n' % radius[0])
debug_file.write('\n')
debug_file.write('lower_limit: %s\n' % lower_limit[0])
debug_file.write('\n')
debug_file.write('deg_dec.latitude: %s\n' % deg_dec.get_latitude())
debug_file.write('deg_dec.longitude: %s\n' % deg_dec.get_longitude())
debug_file.write('deg_dec.altitude: %s\n' % deg_dec.get_altitude())
debug_file.write('deg_dec.radius: %s\n' % deg_dec.get_radius())
debug_file.write('\n')
debug_file.write('document.name: %s\n' % document.get_name())
debug_file.write('document.description: %s\n' % document.get_description())
debug_file.write('document.visibility: %s\n' % document.get_visibility(kml_file))
debug_file.write('document.open: %s\n' % document.get_open(kml_file))
debug_file.write('\n')
debug_file.write('placemark.name: %s\n' % placemark.get_name())
debug_file.write('placemark.description: %s\n' % placemark.get_description())
debug_file.write('placemark.visibility: %s\n' % placemark.get_visibility(kml_file))
debug_file.write('\n')
debug_file.write('poly_style.id: %s\n' % poly_style.get_id())
debug_file.write('poly_style.color: %s\n' % poly_style.get_color())
debug_file.write('poly_style.fill: %s\n' % poly_style.get_fill(kml_file))
debug_file.write('poly_style.outline: %s\n' % poly_style.get_outline(kml_file))
debug_file.write('\n')
debug_file.write('look_at.latitude: %s\n' % look_at.get_latitude())
debug_file.write('look_at.longitude: %s\n' % look_at.get_longitude())
debug_file.write('look_at.altitude: %s\n' % look_at.get_altitude())
debug_file.write('look_at.heading: %s\n' % look_at.get_heading())
debug_file.write('look_at.tilt: %s\n' % look_at.get_tilt())
debug_file.write('look_at.range: %s\n' % look_at.get_range())
debug_file.write('look_at.altitude_mode: %s\n' % look_at.get_altitude_mode())
debug_file.write('\n')
debug_file.write('point_polygon.latitude: %s\n' % point_polygon.get_latitude())
debug_file.write('point_polygon.longitude: %s\n' % point_polygon.get_longitude())
debug_file.write('point_polygon.altitude: %s\n' % point_polygon.get_altitude())
debug_file.write('point_polygon.extrude: %s\n' % point_polygon.get_extrude(kml_file))
debug_file.write('point_polygon.altitude_mode: %s\n' % point_polygon.get_altitude_mode())

debug_file.close()
