def handle_uploaded_file(f):
    ofile='/home/pothiers/.tada/mars.xml'
    print('EXECUTING: handle_uploaded_file({}) => {}'.format(f,ofile))
    with open(ofile, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
