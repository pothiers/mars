find . -name '*.js' ! -path './node_modules/*' ! -path './marssite/bower_components/*' ! -path './marssite/static/*' ! -path './venv/*' > gtaglist.txt

find . -name '*.py' ! -path './node_modules/*' ! -path '**/migrations/*' >> gtaglist.txt

gtags -f gtaglist.txt
