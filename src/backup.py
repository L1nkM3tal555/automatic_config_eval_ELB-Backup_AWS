import json

import time

printUSA = "1.Correspondencia con clientes y proveedores\t2.Recibos de depósito\n3.Órdenes de compra\t4.Hojas de recepción\n5.Adquisiciones\t6.Cuadernos de taquígrafos\n7.Formularios de retirada de existencias\t8.Expedientes personales de los empleados\n9.Solicitudes de empleo\t10.Pólizas de seguro caducadas\n11.Informes de auditoría interna\t12.Comprobantes de caja chica\n13.Etiquetas de inventario físico\t14.Registro de bonos de ahorro\n15.Tarjetas horarias de empleados por horas\t16.Informes de accidentes y reclamaciones\n17.Libros de contabilidad de acreedores/deudores y calendarios\t18.Extractos y conciliaciones bancarias\n19.Cheques cancelados\t20.Certificados de acciones y bonos cancelados\n21.Registros de impuestos sobre la nómina\t22.Análisis de gastos y calendarios de distribución de gastos\n23.Contratos y arrendamientos vencidos\t24.Inventarios (productos, materiales, suministros)\n25.Facturas\t26.Registros y resumen de nóminas (incluidos los pagos de pensiones)\n27.Registros de ventas\t28.Libros auxiliares\n29.Registros de viajes y representación\t30.Comprobantes de pago a proveedores, empleados, etc.\n"

general = {}

dns = {}
protocols = {}
scalling = {}

retUSA = {1: 365,
          2: 365,
          3: 365,
          4: 365, 
          5: 365,
          6: 365,
          7: 365,
          8: 1095,
          9: 1095,
          10: 1095,
          11: 1095,
          12: 1095,
          13: 1095,
          14: 1095,
          15: 1095,
          16: 2555,
          17: 2555,
          18: 2555,
          19: 2555,
          20: 2555,
          21: 2555,
          22: 2555,
          23: 2555,
          24: 2555,
          25: 2555,
          26: 2555,
          27: 2555,
          28: 2555,
          29: 2555,
          30: 2555}

def startEvaluation():
    #start_time = time.time()

    path = "data/elb/sce"
    
    test = input("Selccione un escenario de prueba (Numero del 1 al 4)")
    path = path + test +"/"

    type = input("¿Sobre cual recurso quiere evaluar el backup?\n 1.Bucket de S3\n2.Tabla de base de datos DynamoDB\n")
    tDocsText = "¿Que información esta contenida en "
    if type=="1":
        with open(path+"bucket_location.json") as l:
            loc = json.load(l)
            loc = loc["LocationConstraint"]

        tDocs: list = []

        tDocsText += "el bucket?\n"
        if loc.split('-')[0] == "us":

            tDocs = input(tDocsText+printUSA).split(',')

        startS3(path, tDocs)


        

def startS3(path, tDocs):
    

    with open(path+"s3_backup_rules.json") as s:
        s3 = json.load(s)

    s3 = s3["Rules"]
    for i in range(0,len(s3)):
        status = s3[i]["Status"]
        if status == "Enabled":
            transitions = s3[i]["Transitions"]
            for j in range(0, len(transitions)):
                tansition = transitions[j]
                
