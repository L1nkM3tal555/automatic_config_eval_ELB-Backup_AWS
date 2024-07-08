import json

import time

PRINTUSA = "1.Correspondencia con clientes y proveedores\t2.Recibos de depósito\n3.Órdenes de compra\t4.Hojas de recepción\n5.Adquisiciones\t6.Cuadernos de taquígrafos\n7.Formularios de retirada de existencias\t8.Expedientes personales de los empleados\n9.Solicitudes de empleo\t10.Pólizas de seguro caducadas\n11.Informes de auditoría interna\t12.Comprobantes de caja chica\n13.Etiquetas de inventario físico\t14.Registro de bonos de ahorro\n15.Tarjetas horarias de empleados por horas\t16.Informes de accidentes y reclamaciones\n17.Libros de contabilidad de acreedores/deudores y calendarios\t18.Extractos y conciliaciones bancarias\n19.Cheques cancelados\t20.Certificados de acciones y bonos cancelados\n21.Registros de impuestos sobre la nómina\t22.Análisis de gastos y calendarios de distribución de gastos\n23.Contratos y arrendamientos vencidos\t24.Inventarios (productos, materiales, suministros)\n25.Facturas\t26.Registros y resumen de nóminas (incluidos los pagos de pensiones)\n27.Registros de ventas\t28.Libros auxiliares\n29.Registros de viajes y representación\t30.Comprobantes de pago a proveedores, empleados, etc.\n"

general = []

lifecycle = []

LOCALIZATION = {'us-east-2': 'US East (Ohio)',
                'us-east-1':'US East (N. Virginia)', 
                'us-west-1':'US West (N. California)',
                'us-west-2':'US West (Oregon)',
                'af-south-1':'Africa (Cape Town)',
                'ap-east-1':'Asia Pacific (Hong Kong)',
                'ap-south-2':'Asia Pacific (Hyderabad)',
                'ap-southeast-3':'Asia Pacific (Jakarta)',
                'ap-southeast-4':'Asia Pacific (Melbourne)',
                'ap-south-1':'Asia Pacific (Mumbai)',
                'ap-northeast-3':'Asia Pacific (Osaka)',
                'ap-northeast-2':'Asia Pacific (Seoul)',
                'ap-southeast-1':'Asia Pacific (Singapore)',
                'ap-southeast-2':'Asia Pacific (Sydney)',
                'ap-northeast-1':'Asia Pacific (Tokyo)',
                'ca-central-1':'Canada (Central)',
                'ca-west-1':'Canada West (Calgary)',
                'eu-central-1':'Europe (Frankfurt)',
                'eu-west-1':'Europe (Ireland)',
                'eu-west-2':'Europe (London)',
                'eu-south-1':'Europe (Milan)',
                'eu-west-3':'Europe (Paris)',
                'eu-south-2':'Europe (Spain)',
                'eu-north-1':'Europe (Stockholm)',
                'eu-central-2':'Europe (Zurich)',
                'il-central-1':'Israel (Tel Aviv)',
                'me-south-1':'Middle East (Bahrain)',
                'me-central-1':'Middle East (UAE)',
                }

RETUSA = {1: (365,"Correspondencia con clientes y proveedores"),
          2: (365,"Recibos de depósito"),
          3: (365,"Órdenes de compra"),
          4: (365,"Hojas de recepción"), 
          5: (365,"Adquisiciones"),
          6: (365,"Cuadernos de taquígrafos"),
          7: (365,"Formularios de retirada de existencias"),
          8: (1095,"Expedientes personales de los empleados"),
          9: (1095,"Solicitudes de empleo"),
          10: (1095,"Pólizas de seguro caducadas"),
          11: (1095,"Informes de auditoría interna"),
          12: (1095,"Comprobantes de caja chica"),
          13: (1095,"Etiquetas de inventario físico"),
          14: (1095,"Registro de bonos de ahorro"),
          15: (1095,"Tarjetas horarias de empleados por horas"),
          16: (2555,"Informes de accidentes y reclamaciones"),
          17: (2555,"Libros de contabilidad de acreedores/deudores y calendarios"),
          18: (2555,"Extractos y conciliaciones bancarias"),
          19: (2555,"Cheques cancelados"),
          20: (2555,"Certificados de acciones y bonos cancelados"),
          21: (2555,"Registros de impuestos sobre la nómina"),
          22: (2555,"Análisis de gastos y calendarios de distribución de gastos"),
          23: (2555,"Contratos y arrendamientos vencidos"),
          24: (2555,"Inventarios (productos, materiales, suministros)"),
          25: (2555,"Facturas"),
          26: (2555,"Registros y resumen de nóminas (incluidos los pagos de pensiones)"),
          27: (2555,"Registros de ventas"),
          28: (2555,"Libros auxiliares"),
          29: (2555,"Registros de viajes y representación"),
          30: (2555,"Comprobantes de pago a proveedores, empleados, etc")}


def startEvaluation():
    #start_time = time.time()

    path = "data/elb/sce"
    
    test = input("Selccione un escenario de prueba (Numero del 1 al 4)")
    path = path + test +"/"

    type = input("¿Sobre cual recurso quiere evaluar el backup?\n 1.Bucket de S3\n2.Tabla de base de datos DynamoDB\n")
    
    if type=="1":
        with open(path+"list_buckets.json") as b:
            buckets = json.load(b)
            buckets = loc["Buckets"]

        print("Seleccione el bucket que tiene el backup a analizar")
        selectedBucket = selectBucket(buckets)

        bucketName = buckets[selectedBucket]["Name"]  #Nombre del bucket 
        bucketARN = "arn:aws:s3:::"+bucketName  #Identificador ARN del bucket

        typeBucketBackup = input("El backup del bucket fue realizado con:\n1.Otro bucket de S3\n2.AWS Backup")
        if typeBucketBackup == "1":
            buckets.pop(selectedBucket)
            print("Seleccione el bucket donde esta almacenado el backup")
            selectedBBucket = selectBucket(buckets)

            backupBucketName = buckets[selectedBBucket]["Name"]  #Nombre del bucket que tiene el backuo
            backupBucketARN = "arn:aws:s3:::"+bucketName  #Identificador ARN del bucket que tiene el backup

            with open(path+"bucket_location.json") as l:
                loc = json.load(l)
                loc = loc["LocationConstraint"]

            bucketLifecycle(path,loc)
            
        elif typeBucketBackup == "2":
            awsBackupLifecycle(path)
        else:
            print("Ingrese una opción valida")
    elif type == "2":
            awsBackupLifecycle(path)
    else:
        print("Ingrese una opción valida")

def selectBucket(buckets):
    for i in range(0,len(buckets)):
        print(str(i)+'.'+buckets[i]["Name"])
        
    selectedBucket = int(input())

    return selectedBucket

def generalAwsBackup(mode):
    if mode == 1:
        pass
    
    

        
def bucketLifecycle(path,loc):

    prefixExp:dict = {}

    locS = loc.split('-')[0]

    with open(path+"s3_backup_rules.json") as s:
        s3 = json.load(s)
        s3 = s3["Rules"]
    
    for i in range(0,len(s3)):
        rule = s3[i]
        status = rule["Status"]
        if status == "Enabled":

            if "Expiration" in rule:
                prefixExp[rule["Prefix"]] = rule["Expiration"]["Days"]
            else:
                prefixExp[rule["Prefix"]] = float('inf')

    folders = list(prefixExp.keys)
    
    if locS == "us":
        tDocs = input("¿Que información esta contenida en el bucket? (escriba el numero de la opción y separelas por comas)\n"+PRINTUSA).split(',')
        
        for k in range(0, len(folders)):
            folder = folders[k]
            alert = ""
            expD = prefixExp[folder]
            nDocs= ""
            for j in range(0, len(tDocs)):
                doc = tDocs[j]
                if expD > RETUSA[int(doc)][1]:
                    nDocs += doc
            
            if len(nDocs)>0:
                if folder == "":
                    alert = "ALLFILES:US"
                else:
                    alert = "FOLDER:US:"+folder

                lifecycle.append(alert+nDocs)

    elif locS == "eu":
        
        for k in range(0, len(folders)):
            folder = folders[k]
            alert = ""
            expD = prefixExp[folder]
            retPeriodUser = 0

            if folder == "":
                retPeriodUser = int(input("Indique el numero de dias en los que se necesita la información contenida en el bucket en general (todos los archivos) para tareas de la organización, si no hay un numero de dias definido escriba -1"))
                if expD > retPeriodUser:
                    alert = "ALLFILES:EU"
                    lifecycle.append(alert)
            else:
                retPeriodUser = int(input("Indique el numero de dias en los que se necesita la información contenida en el bucket en la carpeta "+folder+" para tareas de la organización, si no hay un numero de dias definido escriba -1"))
                if expD > retPeriodUser:
                    alert = "FOLDER:EU:"+folder
                    lifecycle.append(alert)         

    else:
        print("El periodo de retención para la localizacion " + LOCALIZATION[loc] + " aun no se encuentra definida, revise la normativa que estableca el periodo de retención del pais en cuestion para la información contenida en su backup ")


def awsBackupLifecycle(path):
    
    with open(path+"list_backup_jobs.json") as s: #En realidad aqui se usaria el comando aws backup list-backup-jobs --by-resource-arn <ARN del bucket> –by-state COMPLETED, se espera obtener el backup job mas reciente
        s3 = json.load(s)
        s3 = s3["BackupJobs"][0]

    backupJobId = s3["BackupJobId"]  #EL id del backup job es necesario para poder detallar la información
    loc = s3["BackupVaultArn"].split(':')[3]  #Se obtiene la información de donde esta almacenado el backup a traves de la zona del vault
    locS = loc.split('-')[0]

    with open(path+"backup_job.json") as bj: #En realidad aqui se usaria el comando aws backup list-backup-jobs --by-resource-arn <ARN del bucket> –by-state COMPLETED
        backupJob = json.load(bj)
    
    backupPlanId = backupJob["CreatedBy"]["BackupPlanId"] #EL id del backup plan es necesario para poder detallar la información
    backupPlanVersion = backupJob["CreatedBy"]["BackupPlanVersion"] #La version del backup plan es necesaria para poder detallar la información

    with open(path+"backup_plan.json") as bp: #En realidad aqui se usaria el comando aws backup get-backup-plan --backup-plan-id <Id del plan de backup> --version-id <id de la version>
        backupPlan = json.load(bp)
        backupPlan = backupPlan["BackupPlan"]["Rules"]

    if locS == "us":
        tDocs = input("¿Que información esta contenida en el backup? (escriba el numero de la opción y separelas por comas)\n"+PRINTUSA).split(',')
        
        for k in range(0, len(backupPlan)):
            rule = backupPlan[k]
            ruleName = rule["RuleName"]
            alert = ""
            expD = rule["Lifecycle"]["DeleteAfterDays"]
            nDocs= ""
            for j in range(0, len(tDocs)):
                doc = tDocs[j]
                if expD > RETUSA[int(doc)][1]:
                    nDocs += doc
            
            if len(nDocs > 0):
                alert = "RULE:US:"+ruleName
                lifecycle.append(alert+nDocs)

    elif locS == "eu":
        
        for k in range(0, len(backupPlan)):
            rule = backupPlan[k]
            ruleName = rule["RuleName"]
            alert = ""
            expD = rule["Lifecycle"]["DeleteAfterDays"]
            retPeriodUser = int(input("Indique el numero de dias en los que se necesita la información contenida en el bucket en general (todos los archivos) para tareas de la organización, si no hay un numero de dias definido escriba -1"))
            if expD > retPeriodUser:
                alert = "RULE:EU"+ruleName
                lifecycle.append(alert)       
                       

    else:
        print("El periodo de retención para la localizacion " + LOCALIZATION[loc] + " aun no se encuentra definida, revise la normativa que estableca el periodo de retención del pais en cuestion para la información contenida en su backup ")

    return (backupJobId,backupPlanId,backupPlanVersion)
