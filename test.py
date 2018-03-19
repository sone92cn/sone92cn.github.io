import os
from jinja2 import Template

try:
	rfile = open("test.tmpl", "r", encoding="utf-8")
	wfile = open("test.html", "w", encoding="utf-8")
except:
        print("Fail to open files.")
else:
	text = rfile.read()
	template = Template(text)
	html = template.render(title='Test Title')
	wfile.write(html)
	rfile.close()
	wfile.close()
	print("Succeed to update file.")

os.system("pause")
