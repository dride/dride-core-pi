import cgi

form = cgi.FieldStorage()
print form["coord"]