import json

import time

general = {}

"""
cipher = {}
rInfo = []
aControl = {}
"""

dns = {}
protocols = {}
scalling = {}

def startEvaluation():
    start_time = time.time()

    path = "data/elb/sce"
    
    test = input("Selccione un escenario de prueba (Numero del 1 al 4)")
    path = path + test +"/"

    type = input("¿Sobre cual recurso quiere evaluar el backup?\n 1.Bucket de S3\n2.Tabla de base de datos DynamoDB\n")
    if type=="1":
        with open(path+"bucket_location.json") as l:
            loc = json.load(l)

        

        with open(path+"s3_backup_rules.json") as s:
            s3 = json.load(s)
        s3 = s3["Rules"]
        for i in range(0,len(s3)):
