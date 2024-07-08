def export(text):
    path = 'results'
    name = input("Escriba el nombre con el que quiere guardar el archivo")
    f = open(path+name+'.txt', "w")
    f.write(text)
    f.close()