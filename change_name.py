import os
 
def changeName(path):
    cName = ''
    for filename in os.listdir(path):
        cName = filename.replace("https:", '')
        cName = cName.replace("http:", '')
        cName = cName.replace("/", '')
        cName = cName.replace("\n", '')

        os.rename(path+filename, path+str(cName))
 

changeName('traffic/')