from configparser import ConfigParser

def config(archivo="PyFinnance.ini", seccion="postgresql"):
    parser = ConfigParser()
    parser.read(archivo)

    db = {}
    if parser.has_section(seccion):
        params = parser.items(seccion)
        for param in params:
            db[param[0]] = param[1]
        return db
    else:
        raise Exception("Seccion {0} no encontada en el archivo '{1}'".format(seccion, archivo))