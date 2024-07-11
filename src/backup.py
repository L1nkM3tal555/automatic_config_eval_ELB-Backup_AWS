import json

import export

PRINTUSA = "1.Correspondencia con clientes y proveedores\n2.Recibos de depósito\n3.Órdenes de compra\n4.Hojas de recepción\n5.Adquisiciones\n6.Cuadernos de taquígrafos\n7.Formularios de retirada de existencias\n8.Expedientes personales de los empleados\n9.Solicitudes de empleo\n10.Pólizas de seguro caducadas\n11.Informes de auditoría interna\n12.Comprobantes de caja chica\n13.Etiquetas de inventario físico\n14.Registro de bonos de ahorro\n15.Tarjetas horarias de empleados por horas\n16.Informes de accidentes y reclamaciones\n17.Libros de contabilidad de acreedores/deudores y calendarios\n18.Extractos y conciliaciones bancarias\n19.Cheques cancelados\n20.Certificados de acciones y bonos cancelados\n21.Registros de impuestos sobre la nómina\n22.Análisis de gastos y calendarios de distribución de gastos\n23.Contratos y arrendamientos vencidos\n24.Inventarios (productos, materiales, suministros)\n25.Facturas\n26.Registros y resumen de nóminas (incluidos los pagos de pensiones)\n27.Registros de ventas\n28.Libros auxiliares\n29.Registros de viajes y representación\n30.Comprobantes de pago a proveedores, empleados, etc.\n"

general = []

lifecycle = []

REGPERMISSIONS = {"CreateBackupPlan",
                "CreateBackupSelection",
                "CreateBackupVault",
                "CreateFramework",
                "CreateLegalHold",
                "CreateLogically-air-gappedBackupVault",
                "CreateReportPlan",
                "CreateRestoreTestingPlan",
                "CreateRestoreTestingSelection",
                }

WARNPERMISSIONS = { "*",
                    "CancelLegalHold",
                    "DeleteBackupPlan",
                    "DeleteBackupSelection",
                    "DeleteBackupVault",
                    "DeleteBackupVault-accessPolicy",
                    "DeleteBackupVaultLock-configuration",
                    "DeleteBackupVault-notifications",
                    "DeleteFramework",
                    "DeleteRecoveryPoint",
                    "DeleteReportPlan",
                    "DeleteRestoreTestingPlan",
                    "DeleteRestoreTestingSelection",
                    "DisassociateRecoveryPoint",
                    "DisassociateRecoveryPointFromParent",
                    "PutBackupVaultAccessPolicy",
                    "PutBackupVaultLock-configuration",
                    "PutBackupVault-notifications",
                    "PutRestoreValidationResult",
                    "StartBackupJob",
                    "StartCopyJob",
                    "StartReportJob",
                    "StartRestoreJob",
                    "StopBackupJob",
                    "TagResource",
                    "UntagResource",
                    "UpdateBackupPlan",
                    "UpdateFramework",
                    "UpdateGlobalSettings",
                    "UpdateRecoveryPointLifecycle",
                    "UpdateRegionSettings",
                    "UpdateReportPlan",
                    "UpdateRestoreTestingPlan",
                    "UpdateRestoreTestingSelection"
                    "RestoreTableFromBackup"
                }

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

    path = "data/backup/sce"
    
    test = input("Selccione un escenario de prueba (Numero del 1 al 6)\n")
    path = path + test +"/"

    type = input("¿Sobre cual recurso quiere evaluar el backup?\n1. Bucket de S3\n2. Tabla de base de datos DynamoDB\n")

    
    if type=="1":
        with open(path+"list_buckets.json") as b:
            buckets = json.load(b)
            buckets = buckets["Buckets"]

        print("Seleccione el bucket al que se le hizo el backup")
        selectedBucket = selectBucket(buckets)

        bucketName = buckets[selectedBucket]["Name"]  #Nombre del bucket 
        bucketARN = "arn:aws:s3:::"+bucketName  #Identificador ARN del bucket

        typeBucketBackup = input("El backup del bucket fue realizado con:\n1. Otro bucket de S3\n2. AWS Backup\n")
        if typeBucketBackup == "1":
            buckets.pop(selectedBucket)
            print("Seleccione el bucket donde esta almacenado el backup")
            selectedBBucket = selectBucket(buckets)

            backupBucketName = buckets[selectedBBucket]["Name"]  #Nombre del bucket que tiene el backuo
            backupBucketARN = "arn:aws:s3:::"+bucketName  #Identificador ARN del bucket que tiene el backup

            with open(path+"bucket_location.json") as l:
                loc = json.load(l)
                loc = loc["LocationConstraint"]

            with open(path+"s3_backup_rules.json") as s: #En realidad deberia usarse el comando 
                s3 = json.load(s)
                s3 = s3["Rules"]

            bucketLifecycle(s3,loc)

            generalBucket(path)

            result = printResult("1",bucketName, backupBucketName)

            exp = input("¿Desea exportar los resultados?\n1.Si\n2.No\n")

            if exp == "1":
                export.export(result)
            
            print(result)
            
        elif typeBucketBackup == "2":
            with open(path+"describe-protected-resource.json") as p:
                pr = json.load(p)
            
            vault = pr["LastBackupVaultArn"] #Este identificador sirve para saber la información de recuperación de información
            loc = vault.split(':')[3]

            rp = pr["LastRecoveryPointArn"] #Este es el identificador del ultimo punto de recuperación que deberia usarse para saber la información del ciclo de vida del backup

            recP = awsBackupLifecycle(path, loc, rp)
            generalAwsBackup(path,False,recP,vault)

            result = printResult("2",bucketName, vault)

            exp = input("¿Desea exportar los resultados?\n1.Si\n2.No\n")

            if exp == "1":
                export.export(result)
            
            print(result)

        else:
            print("Ingrese una opción valida")
    elif type == "2":
        #TODO Inicialmente se deberia preguntar el nombre de la tabla, y de ahi sacar los buckets sobre esa tabla
        with open(path+"dynamo_list_backups.json") as b: #En realidad aqui deberia usarse el comando aws dynamodb list-backups <Nombre de la tabla>
            backupD = json.load(b)
            backupD = backupD["BackupSummaries"]

        

        for i in range(0, len(backupD)):
            
            if backupD[i]["BackupType"] == "AWS_BACKUP":
                tableName = backupD[i]["BackupArn"].split('/')[1] #!Esto deberia saberse desde antes cuando el usuario ponga el nombre de la tabla
                with open(path+"dynamo_describe_backup.json") as b: #En realidad aqui deberia usarse el comando aws dynamodb list-backups <Nombre de la tabla>
                    backupDD = json.load(b)
                    backupDD = backupDD["BackupDescription"]["SourceTableFeatureDetails"]["SSEDescription"] # TODO verificar que existan estos campos

                with open(path+"describe-protected-resource.json") as p:
                    pr = json.load(p)
                
                vault = pr["LastBackupVaultArn"] #Este identificador sirve para saber la información de recuperación de información
                loc = vault.split(':')[3]

                rp = pr["LastRecoveryPointArn"] #Este es el identificador del ultimo punto de recuperación que deberia usarse para saber la información del ciclo de vida del backup

                recP = awsBackupLifecycle(path, loc, rp)
                generalAwsBackup(path,backupDD,recP,vault)

                result = printResult("3",tableName, vault)

                exp = input("¿Desea exportar los resultados?\n1.Si\n2.No\n")

                if exp == "1":
                    export.export(result)
                
                print(result)
            elif backupD[i]["BackupType"] == "SYSTEM":
                print("SYSTEM")
            else:
                general.append("DYNAMO:USERB")
        #Dynamo awsBackupLifecycle(path)
        
    else:
        print("Ingrese una opción valida")

def printResult(type, resource, backupResource):
    b = ""
    response = ""
    response+="\nEVALUACIÓN DE CONFIGURACIÓN DE BACKUP\n"
    if type == "1":
        response += "\nBACKUP DE UN BUCKET DE S3 EN OTRO BUCKET\n"
        b = "bucket"
    elif type == "2":
        response += "\nBACKUP DE UN BUCKET DE S3 EN AWS BACKUP\n"
        b = "servicio de backup"
    else:
        response += "\nBACKUP DE UNA TABLA DE DYNAMODB\n"
        b = "servicio de backup"
    response += "\nRecurso:\n"+resource+"\n\nRecurso de almacenamiento del backup:\n"+backupResource
    response+="\nASPECTOS GENERALES:\n"
    if len(general) !=0:
        for i in range(0, len(general)):
            
            alert = general[i].split(':')
            if alert[0] == "CIPHER":
                response+="ADVERTENCIA - CIFRADO: No se encontró información del cifrado del "+b+", verifique el estado, su información podria no ser confidencial\n"
            if alert[0] == "CIPHERD":
                response+="ADVERTENCIA - CIFRADO: No se encontró información del cifrado en Amazon DynamoDB, verifique que si haya cifrado en su "+b+", su información podria no ser confidencial\n"
            elif alert[0] == "INFOREC":
                response+="ADVERTENCIA - RECUPERACIÓN DE INFORMACIÓN: No se encontró uso de logs para el "+b+", podria perderse información en caso de una eventualidad\n"
            elif alert[0] == "INFORECB":
                response+="ADVERTENCIA - RECUPERACIÓN DE INFORMACIÓN: No se tienen mas de un punto de recuperación para el "+b+", podria perderse información en caso de una eventualidad\n"
            elif alert[0] == "ACCESS":
                if alert[1] == "WARN":
                    response+="ADVERTENCIA - CONTROL DE ACCESO: Se encontraron "+alert[2]+" politicas con permisos que dan autorización completa sobre el "+b+" o con autorización para modificar la politica de control de acceso, verifique que los permisos esten asignados unicamente a usuarios autorizados\n"
                else:
                    response+="ADVERTENCIA - CONTROL DE ACCESO: Se encontraron "+alert[2]+" politicas con permisos que dan autorización para modificar los archivos contenidos en el "+b+" o con autorización para ver la politica de control de acceso, verifique que los permisos esten asignados unicamente a usuarios autorizados\n"

    else:
        response+="No se encontraron configuraciones inadecuadas en el cifrado, recuperación de información o control de acceso para el backup realizado\n"
    
    response+="\nASPECTOS ESPECIFICOS:\n"
    response+="CICLO DE VIDA DEL BACKUP:\n"
    if len(lifecycle) !=0:
        for i in range(0, len(lifecycle)):
            alert = lifecycle[i].split(':')
            if alert[0] == "ALLFILES":
                if alert[1] == "US":
                    docs = ""
                    docsN = alert[2].split(',')
                    for l in range(0,len(docsN)):
                        doc = docsN[l]
                        docs+=RETUSA[int(doc)][1]+"\n"

                    response+="\nERROR - LIFECYCLE: Se identifico la ubicación del backup en Estados Unidos, una politica del ciclo de vida del backup en el "+b+" indica que todos los archivos almacenados en el bucket no cumplen con el periodo de retención dado por la norma para los siguientes tipos de información:\n"+docs
                elif alert[1] == "ALL":
                    response+="\nERROR - LIFECYCLE: No se encontraron politicas del ciclo de vida que manejen un periodo para la eliminación de la información, tenga en cuenta la normativa de su pais y evite sanciones\n"
                else:
                    response+="\nERROR - LIFECYCLE: Se identifico la ubicación del backup en Europa, una politica del ciclo de vida del backup en el "+b+" indica que todos los archivos almacenados no cumplen con el periodo de retención dado por la organización para la información\n"
            elif alert[0] == "FOLDER":
                if alert[1] == "US":
                    docs = ""
                    docsN = alert[3].split(',')
                    for l in range(0,len(docsN)):
                        doc = docsN[l]
                        docs+=RETUSA[int(doc)][1]+"\n"

                    response+="\nERROR - LIFECYCLE: Se identifico la ubicación del backup en Estados Unidos, una politica del ciclo de vida del backup en el "+b+" indica que los archivos almacenados en la carpeta "+alert[2]+" del bucket no cumplen con el periodo de retención dado por la norma para los siguientes tipos de información:\n"+docs
                else:
                    response+="\nERROR - LIFECYCLE: Se identifico la ubicación del backup en Europa, una politica del ciclo de vida del backup en el "+b+" indica que todos los archivos almacenados en la carpeta "+alert[2]+ " del bucket no cumplen con el periodo de retención dado por la organización para la información contenida en la carpeta\n"
            elif alert[0] == "RULE":
                if alert[1] == "US":
                    docs = ""
                    docsN = alert[3].split(',')
                    for l in range(0,len(docsN)):
                        doc = docsN[l]
                        docs+=RETUSA[int(doc)][1]+"\n"

                    response+="\nERROR - LIFECYCLE: Se identifico la ubicación del backup en Estados Unidos, una politica del ciclo de vida del backup en el "+b+" indica en la regla "+alert[2]+" que los archivos en el backup no cumplen con el periodo de retención dado por la norma para los siguientes tipos de información:\n"+docs
                else:
                    response+="\nERROR - LIFECYCLE: Se identifico la ubicación del backup en Europa, una politica del ciclo de vida del backup en el "+b+" indica en la regla "+alert[2]+ " los archivos almacenados en el backup no cumplen con el periodo de retención dado por la organización.\n"

    else:
        response+="\nLa configuración del ciclo de vida del backup cumple con la norma establecida para su ubicación\n"

    return response
    

def selectBucket(buckets):
    for i in range(0,len(buckets)):
        print(str(i)+'.'+buckets[i]["Name"])
        
    selectedBucket = int(input())

    return selectedBucket

def generalBucket(path): #En realidad a esta funcion deberian pasarle el nombre del bucket para que pueda usarse de identificador
    #Cipher
    with open(path+"general_val/cipher_val_s3.json") as c: #En realidad se usa el comando aws s3api get-bucket-encryption
        cipher = json.load(c)
        cipher = cipher["ServerSideEncryptionConfiguration"]["Rules"]

    for i in range (0, len(cipher)):
        rule = cipher[i]["ApplyServerSideEncryptionByDefault"]

        if "SSEAlgorithm" not in rule:
            general.append("CIPHER")
    #InfoRecovery
    with open(path+"general_val/info_rec_s3.json") as ir: #En realidad se usa el comando aws s3api get-bucket-versioning
        infoR = json.load(ir)

    if infoR["Status"] == "Disabled":
        general.append("INFOREC")

    #AccessControl

    with open(path+"general_val/access_control_s3.json") as ac: #En realidad se usa el comando aws s3api get-bucket-acl
        accC = json.load(ac)
        accC = accC["Grants"]

    noAcc = 0
    regAcc = 0
    for j in range(0, len(accC)):
        permission = accC[j]["Permission"]
        if permission == "FULL_CONTROL" or permission == "WRITE_ACP":
            noAcc+=1
        elif permission == "READ_ACP" or permission == "WRITE":
            regAcc+=1

    if noAcc > 0:
        general.append("ACCESS:WARN:"+str(noAcc))

    if regAcc > 0:
        general.append("ACCESS:REG:"+str(regAcc))

def generalAwsBackup(path, dynamo, recPoint, vaultId):
    if dynamo:
        if dynamo["Status"] == "DISABLED":
            general.append("CIPHERD")

    if recPoint["IsEncrypted"] == False:
        general.append("CIPHER")

    with open(path+"general_val/describe_backup_vault.json") as v: #En realidad aqui se usaria el comando aws backup describe-backup-vault <ARN del vault>
        vault = json.load(v)
        vault = vault["NumberOfRecoveryPoints"]

    if vault <= 1:
        general.append("INFORECB")

    iamRole = recPoint["IamRoleArn"] #Este sirve como identificador del rol de iam

    with open(path+"general_val/access_control_iam_list_attached_role_policies.json") as p: #En realidad aqui se usaria el comando aws iam list-attached-role-policies <ARN del rol>
        iam = json.load(p)
        iam = iam["AttachedPolicies"]

    noAcc = 0
    regAcc = 0

    for i in range(0,len(iam)):
        policiy = iam[i]["PolicyArn"] #Este sirve como identificador de la politica de iam
        with open(path+"general_val/access_control_iam_list_policy_version.json") as pv: #En realidad aqui se usaria el comando aws iam list_policy_version <ARN de la politica>
            policyVer = json.load(pv)
            policyVer = policyVer["Versions"]
        
        ver = "" #Identificador de la version

        for j in range(0,len(policyVer)):
            version = policyVer[j]
            if version["IsDefaultVersion"] == True:
                ver = version["VersionId"]
                break
        
        with open(path+"general_val/access_control_iam_get_policy_version.json") as pvd: #En realidad aqui se usaria el comando aws iam get_policy_version <ARN de la versión y la politica>
            policyVerD = json.load(pvd)
            policyVerD = policyVerD["PolicyVersion"]["Document"]["Statement"]

        for k in range(0, len(policyVerD)):
            statement = policyVerD[k]
            if statement["Effect"] == "Allow":
                actions = statement["Action"]
                for w in range(0, len(actions)):
                    action = actions[w].split(':')[1]
                    if action in WARNPERMISSIONS:
                        noAcc += 1
                        break
                    elif action in REGPERMISSIONS:
                        regAcc += 1

    if noAcc > 0:
        general.append("ACCESS:WARN:"+str(noAcc))

    if regAcc > 0:
        general.append("ACCESS:REG:"+str(regAcc))
        
def bucketLifecycle(s3,loc):

    locS = loc.split('-')[0]

    ruleFound = False
    for i in range(0,len(s3)):
        rule = s3[i]
        status = rule["Status"]
        folder = rule["Prefix"]
        alert = ""
        
        if status == "Enabled":

            if "Expiration" in rule:
                expD = rule["Expiration"]
                if "Days" in expD:
                    ruleFound = True
                    expD = rule["Expiration"]["Days"]
                    #__
                    if locS == "us":
                        tDocs = input("¿Que información esta contenida en el bucket? (escriba el numero de la opción y separelas por comas)\n"+PRINTUSA).split(',')
                        
                        nDocs= ""
                        for j in range(0, len(tDocs)):
                            
                            doc = tDocs[j]
                            if expD > RETUSA[int(doc)][0]:
                                if j > 0:
                                    nDocs+=","
                                nDocs += doc
                        
                        if len(nDocs)>0:
                            if folder == "":
                                alert = "ALLFILES:US"
                            else:
                                alert = "FOLDER:US:"+folder+":"

                            lifecycle.append(alert+nDocs)

                    elif locS == "eu":
                            
                        retPeriodUser = 0

                        if folder == "":
                            retPeriodUser = int(input("Indique el numero de dias en los que se necesita la información contenida en el bucket en general (todos los archivos) para tareas de la organización, si no hay un numero de dias definido escriba -1\n"))
                            if expD > retPeriodUser:
                                alert = "ALLFILES:EU"
                                lifecycle.append(alert)
                        else:
                            retPeriodUser = int(input("Indique el numero de dias en los que se necesita la información contenida en el bucket en la carpeta "+folder+" para tareas de la organización, si no hay un numero de dias definido escriba -1\n"))
                            if expD > retPeriodUser:
                                alert = "FOLDER:EU:"+folder
                                lifecycle.append(alert)         

                    else:
                        alert = "NO:RET:LOC"
                        lifecycle.append(alert)
                        print("El periodo de retención para la localizacion " + LOCALIZATION[loc] + " aun no se encuentra definida, revise la normativa que estableca el periodo de retención del pais en cuestion para la información contenida en su backup ")
    
    if ruleFound == False:
        lifecycle.append("ALLFILES:ALL")
    
def awsBackupLifecycle(path, loc, rp):
    locS = loc.split('-')[0]
    with open(path+"list_recovery_points_by_vault.json") as r: #En realidad aqui se usaria el comando aws backup list_recovery_points_by_vault  <ARN del vault>
        recP = json.load(r)
        recP = recP["RecoveryPoints"]

    for i in range(0,len(recP)):
        recPoint = recP[i]
        if recPoint["RecoveryPointArn"] == rp:
            plan = recPoint["CreatedBy"]["BackupPlanId"]
            planVersion = recPoint["CreatedBy"]["BackupPlanVersion"]

            with open(path+"backup_plan.json") as p: #En realidad aqui se usaria el comando aws backup get-backup-plan <ARN del vault> --version <Version del plan>
                backupPlan = json.load(p)
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
                if expD > RETUSA[int(doc)][0]:
                    if j > 0:
                        nDocs+=","
                    nDocs += doc
            
            if len(nDocs) > 0:
                alert = "RULE:US:"+ruleName+":"
                lifecycle.append(alert+nDocs)

    elif locS == "eu":
        retPeriodUser = int(input("Indique el numero de dias en los que se necesita la información contenida en el backup en general (todos los archivos) para tareas de la organización, si no hay un numero de dias definido escriba -1\n"))
        if retPeriodUser != "-1":
            for k in range(0, len(backupPlan)):
                rule = backupPlan[k]
                ruleName = rule["RuleName"]
                alert = ""
                expD = rule["Lifecycle"]["DeleteAfterDays"]
                if expD > retPeriodUser:
                    alert = "RULE:EU"+ruleName
                    lifecycle.append(alert)   
        else:
            lifecycle.append("RULE:NORETORG")    
                       

    else:
        alert = "NO:RET:LOC"
        lifecycle.append(alert)
        print("El periodo de retención para la localizacion " + LOCALIZATION[loc] + " aun no se encuentra definida, revise la normativa que estableca el periodo de retención del pais en cuestion para la información contenida en su backup ")

    return recPoint