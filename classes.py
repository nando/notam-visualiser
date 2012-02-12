import math


NAUTICAL_MILE_TO_METRE = 1852
FOOT_TO_METRE = 0.3048


class NOTAM():

#   str q_line
#   str f_line
#   str g_line

    def __init__(self):
        self.q_line = ''
        self.f_line = ''
        self.g_line = ''


    def set_q_line(self, q_line):
        self.q_line = q_line.strip()


    def set_f_line(self, f_line):
        self.f_line = f_line.strip()


    def set_g_line(self, g_line):
        self.g_line = g_line.strip()


    def get_q_line(self):
        return self.q_line


    def get_f_line(self):
        return self.f_line


    def get_g_line(self):
        return self.g_line


    def check_q_line(self, notam_line):
        if notam_line.startswith('Q) '):
            return True
        else:
            return False


    def check_f_line(self, notam_line):
        if notam_line.startswith('LOWER: '):
            return True
        else:
            return False


    def check_g_line(self, notam_line):
        if notam_line.startswith('UPPER: '):
            return True
        else:
            return False


    def set_notam_lines(self, notam_lines):
        notam_lines_list = notam_lines.split('\n')
        for line in notam_lines_list:
            if self.check_q_line(line):
                self.set_q_line(line)
            elif self.check_f_line(line):
                self.set_f_line(line)
            elif self.check_g_line(line):
                self.set_g_line(line)


    def extract_lower_height_limit(self):
        end = self.q_line.rfind('/')
        end = self.q_line.rfind('/', 0, end)
        start = self.q_line.rfind('/', 0, end) + 1
        return int(self.q_line[start:end])


    def extract_upper_height_limit(self):
        end = self.q_line.rfind('/')
        start = self.q_line.rfind('/', 0, end) + 1
        return int(self.q_line[start:end])


    def extract_coordinates_string(self):
        index = self.q_line.rfind('/') + 1
        return self.q_line[index:]


    def extract_coordinate(self, coordinates_string, index, increment):
        coordinates_substring = coordinates_string[index[0]:index[0] + increment]
        coordinate = int(coordinates_substring)
        index[0] += increment
        return coordinate


    def extract_direction(self, coordinates_string, index):
        direction = coordinates_string[index[0]]
        index[0] += 1
        return direction


    def extract_radius(self, coordinates_string, index):
        coordinates_substring = coordinates_string[index[0]:]
        radius = int(coordinates_substring)
        return radius


    def extract_q_line_info(self, latitude, longitude, radius):
        index = [0]
        coordinates_string = self.extract_coordinates_string()
        latitude.set_degrees(self.extract_coordinate(coordinates_string, index, 2))
        latitude.set_minutes(self.extract_coordinate(coordinates_string, index, 2))
        latitude.set_direction(self.extract_direction(coordinates_string, index))
        longitude.set_degrees(self.extract_coordinate(coordinates_string, index, 3))
        longitude.set_minutes(self.extract_coordinate(coordinates_string, index, 2))
        longitude.set_direction(self.extract_direction(coordinates_string, index))
        radius[0] = self.extract_radius(coordinates_string, index)


    def extract_f_line_info(self, lower_limit, lower_height_limit):
        if self.f_line.find('SFC') != -1 or self.f_line.find('GND') != -1 or self.f_line.find('GRD') != -1:
            lower_limit[0] = 0
        elif self.f_line.find('AMSL') != -1:
            index = self.f_line.find(' ') + 1
            length = self.f_line.find('F') - index
            line_substring = self.f_line[index:index + length]
            metres = int(line_substring) * FOOT_TO_METRE
            lower_limit[0] = metres
        elif self.f_line.find('FL') != -1:
            index = self.f_line.find('FL') + 2
            length = len(self.f_line) - index + 1
            line_substring = self.f_line[index:index + length]
            flight_level = int(line_substring) * FOOT_TO_METRE * 100
            lower_limit[0] = flight_level
        elif self.f_line == '':
            altitude = lower_height_limit * FOOT_TO_METRE * 100
            lower_limit[0] = altitude


    def extract_g_line_info(self, deg_dec, upper_height_limit):
        if self.g_line.find('UNL') != -1:
            deg_dec.set_altitude(99999)
        elif self.g_line.find('AMSL') != -1:
            index = self.g_line.find(' ') + 1
            length = self.g_line.find('F') - index
            line_substring = self.g_line[index:index + length]
            metres = int(line_substring) * FOOT_TO_METRE
            deg_dec.set_altitude(metres)
        elif self.g_line.find('FL') != -1:
            index = self.g_line.find('FL') + 2
            length = len(self.g_line) - index + 1
            line_substring = self.g_line[index:index + length]
            flight_level = int(line_substring) * FOOT_TO_METRE * 100
            deg_dec.set_altitude(flight_level)
        elif self.g_line == '':
            if upper_height_limit == 999:
                altitude = 99999
            else:
                altitude = upper_height_limit * FOOT_TO_METRE * 100
            deg_dec.set_altitude(altitude)


class DMS():

#   int degrees
#   int minutes
#   char direction

    def set_degrees(self, degrees):
        self.degrees = degrees


    def set_minutes(self, minutes):
        self.minutes = minutes


    def set_direction(self, direction):
        self.direction = direction


    def get_degrees(self):
        return self.degrees


    def get_minutes(self):
        return self.minutes


    def get_direction(self):
        return self.direction


    def convert_coordinate(self):
        deg_dec_coordinate = self.degrees + (self.minutes * 60.0) / 3600.0
        if self.direction == 'N' or self.direction == 'E':
            return deg_dec_coordinate
        else:
            return -deg_dec_coordinate


class Placemark():

#   str name
#   str description
#   bool visibility

    def set_name(self, name):
        self.name = name


    def set_description(self, description):
        self.description = description


    def set_visibility(self, visibility):
        self.visibility = visibility


    def get_name(self):
        return self.name


    def get_description(self):
        return self.description


    def get_visibility(self, kml_file):
        return kml_file.get_boolean_value(self.visibility)


class Document(Placemark):

#   bool open

    def set_open(self, open):
        self.open = open


    def get_open(self, kml_file):
        return kml_file.get_boolean_value(self.open)


class PolyStyle():

#   str id
#   str color
#   bool fill
#   bool outline

    def set_id(self, id):
        self.id = id


    def set_color(self, color):
        self.color = color


    def set_fill(self, fill):
        self.fill = fill


    def set_outline(self, outline):
        self.outline = outline


    def get_id(self):
        return self.id


    def get_color(self):
        return self.color


    def get_fill(self, kml_file):
        return kml_file.get_boolean_value(self.fill)


    def get_outline(self, kml_file):
        return kml_file.get_boolean_value(self.outline)


class DegDec():

#   double latitude
#   double longitude
#   double altitude
#   double radius

    def set_latitude(self, latitude):
        self.latitude = latitude


    def set_longitude(self, longitude):
        self.longitude = longitude


    def set_altitude(self, altitude):
        self.altitude = altitude


    def set_radius(self, radius):
        self.radius = radius


    def get_latitude(self):
        return self.latitude


    def get_longitude(self):
        return self.longitude


    def get_altitude(self):
        return self.altitude


    def get_radius(self):
        return self.radius


    def convert_radius(self, radius):
        return radius[0] * NAUTICAL_MILE_TO_METRE


    def calculate_coordinates(self, kml_file):

        # Vincenty's Direct formula
        #
        # Given phi1, lambda1, alpha1 and s,
        # find phi2, lambda2 and alpha2,
        #
        # where:
        #
        # a = length of major axis of ellipsoid (radius at equator)
        #     (6,378,137.0 metres in WGS-84)
        # b = length of minor axis of ellipsoid (radius at the poles)
        #     (6,356,752.314 metres in WGS-84)
        # f = (a - b)/a = flattening of ellipsoid (1/298.257223563 in WGS-84)
        # phi1, phi2 = latitude of points
        # U1 = arctan[(1 − f) tan phi1] = reduced latitude
        # lambda1, lambda2 = longitude of points
        # L = lambda2 − lambda1	= difference in longitude
        # alpha1 = forward azimuth
        # alpha = azimuth at equator (arc path the points are on)
        # s = ellipsoidal distance between the points

        angle = math.radians(360 / 20)
        a = 6378137.0
        b = 6356752.314
        f = 1 / 298.257223563
        phi1 = self.get_latitude()
        lambda1 = self.get_longitude()
        alpha1 = 0.0
        s = self.get_radius()
        tan_U1 = (1 - f) * math.tan(math.radians(phi1))
        sin_U1 = math.sqrt(tan_U1 ** 2 / (tan_U1 ** 2 + 1))
        cos_U1 = 1 / math.sqrt(1 + tan_U1 ** 2)
        while alpha1 <= math.radians(360):
            sin_alpha1 = math.sin(alpha1)
            cos_alpha1 = math.cos(alpha1)
            sigma1 = math.atan2(tan_U1, cos_alpha1)
            sin_alpha = cos_U1 * sin_alpha1
            cos2_alpha = 1 - sin_alpha ** 2
            u2 = cos2_alpha * ((a ** 2 - b ** 2) / b ** 2)
            A = 1 + (u2 / 16384) * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
            B = (u2 / 1024) * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
            sigma = s / (b * A)
            sigma_p = math.radians(360)
            sigma_m_2 = 0.0
            while math.fabs(sigma - sigma_p) > 1e-12:
                sigma_m_2 = sigma1 * 2 + sigma
                cos_sigma_m_2 = math.cos(sigma_m_2)
                sin_sigma = math.sin(sigma)
                cos_sigma = math.cos(sigma)
                delta_sigma = B * sin_sigma * (cos_sigma_m_2 + (1 / 4) * B * (cos_sigma * (-1 + 2 * cos_sigma_m_2 ** 2) - (1 / 6) * B * cos_sigma_m_2 * (-3 + 4 * sin_sigma ** 2) * (-3 + 4 * cos_sigma_m_2 ** 2)))
                sigma_p = sigma
                sigma = (s / (b * A)) + delta_sigma
            cos_sigma_m_2 = math.cos(sigma_m_2)
            sin_sigma = math.sin(sigma)
            cos_sigma = math.cos(sigma)
            phi2 = math.atan2(sin_U1 * cos_sigma + cos_U1 * sin_sigma * cos_alpha1, (1 - f) * math.sqrt(sin_alpha ** 2 + (sin_U1 * sin_sigma - cos_U1 * cos_sigma * cos_alpha1) ** 2))
            phi2 = math.degrees(phi2)
            lambda0 = math.atan2(sin_sigma * sin_alpha1, cos_U1 * cos_sigma - sin_U1 * sin_sigma * cos_alpha1)
            C = (f / 16) * cos2_alpha * (4 + f * (4 - 3 * cos2_alpha))
            L = lambda0 - (1 - C) * f * sin_alpha * (sigma + C * sin_alpha * (cos_sigma_m_2 + C * cos_sigma * (-1 + 2 * cos_sigma_m_2 ** 2)))
            lambda2 = lambda1 + math.degrees(L)
            kml_file.print_normal("%s,%s,%s" % (lambda2, phi2, int(round(self.get_altitude()))))
            alpha1 += angle


class LookAt(DegDec):

#   int heading
#   int tilt
#   int range
#   str altitude_mode

    def set_heading(self, heading):
        self.heading = heading


    def set_tilt(self, tilt):
        self.tilt = tilt


    def set_range(self, range):
        self.range = range


    def set_altitude_mode(self, altitude_mode):
        self.altitude_mode = altitude_mode


    def get_heading(self):
        return self.heading


    def get_tilt(self):
        return self.tilt


    def get_range(self):
        return self.range


    def get_altitude_mode(self):
        return self.altitude_mode


    def convert_to_range(self, radius):
        return radius * 3


class PointPolygon(DegDec):

#   bool extrude
#   str altitude_mode

    def set_extrude(self, extrude):
        self.extrude = extrude


    def set_altitude_mode(self, altitude_mode):
        self.altitude_mode = altitude_mode


    def get_extrude(self, kml_file):
        return kml_file.get_boolean_value(self.extrude)


    def get_altitude_mode(self):
        return self.altitude_mode


class KMLFile():

#   file file
#   int width_constant
#   int indent_width

    def set_file_location(self, file_location):
        self.file = open(file_location, 'w')


    def set_width_constant(self, width_constant):
        self.width_constant = width_constant


    def set_indent_width(self, indent_width):
        self.indent_width = indent_width


    def get_width_constant(self):
        return self.width_constant


    def get_indent_width(self):
        return self.indent_width


    def get_boolean_value(self, boolean_variable):
        if boolean_variable:
            return 1
        else:
            return 0


    def increase_indent(self):
        self.indent_width += self.width_constant


    def decrease_indent(self):
        self.indent_width -= self.width_constant


    def print_normal(self, string_line):
        i = 0
        while i < self.indent_width:
            self.file.write(' ')
            i += 1
        self.file.write(string_line + '\n')


    def indent(self, string_line):
        self.increase_indent()
        self.print_normal(string_line)


    def unindent(self, string_line):
        self.decrease_indent()
        self.print_normal(string_line)


    def create_kml_source(self, document, poly_style, placemark, latitude, longitude, look_at, point_polygon, deg_dec):
        self.print_normal('<kml>')
        self.indent('<Document>')
        self.indent('<name>%s</name>' % document.get_name())
        self.print_normal('<visibility>%s</visibility>' % document.get_visibility(self))
        self.print_normal('<open>%s</open>' % document.get_open(self))
        self.print_normal('<description>')
        self.indent(document.get_description())
        self.unindent('</description>')
        self.print_normal('<Style id="%s">' % poly_style.get_id())
        self.indent('<PolyStyle>')
        self.indent('<color>%s</color>' % poly_style.get_color())
        self.print_normal('<fill>%s</fill>' % poly_style.get_fill(self))
        self.print_normal('<outline>%s</outline>' % poly_style.get_outline(self))
        self.unindent('</PolyStyle>')
        self.unindent('</Style>')
        self.print_normal('<Placemark>')
        self.indent('<name>%s</name>' % placemark.get_name())
        self.print_normal('<visibility>%s</visibility>' % placemark.get_visibility(self))
        self.print_normal('<description>')
        self.indent(placemark.get_description())
        self.print_normal('')
        self.print_normal('latitude: %s%s%s (%s)' % (latitude.get_degrees(), latitude.get_minutes(), latitude.get_direction(), deg_dec.get_latitude()))
        self.print_normal('longitude: %s%s%s (%s)' % (longitude.get_degrees(), longitude.get_minutes(), longitude.get_direction(), deg_dec.get_longitude()))
        self.print_normal('altitude: %s m' % int(round(deg_dec.get_altitude())))
        self.print_normal('radius: %s m' % deg_dec.get_radius())
        self.unindent('</description>')
        self.print_normal('<styleUrl>#%s</styleUrl>' % poly_style.get_id())
        self.print_normal('<LookAt>')
        self.indent('<longitude>%s</longitude>' % look_at.get_longitude())
        self.print_normal('<latitude>%s</latitude>' % look_at.get_latitude())
        self.print_normal('<altitude>%s</altitude>' % int(round(look_at.get_altitude())))
        self.print_normal('<heading>%s</heading>' % look_at.get_heading())
        self.print_normal('<tilt>%s</tilt>' % look_at.get_tilt())
        self.print_normal('<range>%s</range>' % look_at.get_range())
        self.print_normal('<altitudeMode>%s</altitudeMode>' % int(round(look_at.get_altitude())))
        self.unindent('</LookAt>')
        self.print_normal('<MultiGeometry>')
        self.indent('<Point>')
        self.indent('<extrude>%s</extrude>' % point_polygon.get_extrude(self))
        self.print_normal('<altitudeMode>%s</altitudeMode>' % point_polygon.get_altitude_mode())
        self.print_normal('<coordinates>%s,%s,%s</coordinates>' % (point_polygon.get_longitude(), point_polygon.get_latitude(), int(round(point_polygon.get_altitude()))))
        self.unindent('</Point>')
        self.print_normal('<Polygon>')
        self.indent('<extrude>%s</extrude>' % point_polygon.get_extrude(self))
        self.print_normal('<altitudeMode>%s</altitudeMode>' % point_polygon.get_altitude_mode())
        self.print_normal('<outerBoundaryIs>')
        self.indent('<LinearRing>')
        self.indent('<coordinates>')
        self.increase_indent()
        deg_dec.calculate_coordinates(self)
        self.unindent('</coordinates>')
        self.unindent('</LinearRing>')
        self.unindent('</outerBoundaryIs>')
        self.unindent('</Polygon>')
        self.unindent('</MultiGeometry>')
        self.unindent('</Placemark>')
        self.unindent('</Document>')
        self.unindent('</kml>')
        self.file.close()
