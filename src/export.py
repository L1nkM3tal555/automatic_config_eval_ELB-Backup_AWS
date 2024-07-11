def export(text):
    path = 'results/'
    name = input("Escriba el nombre con el que quiere guardar el archivo\n")
    f = open(path+name+'.txt', "w")
    f.write(text)
    f.close()