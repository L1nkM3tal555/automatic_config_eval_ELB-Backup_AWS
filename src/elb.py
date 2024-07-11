import json

import time

import export


general = {}

dns = {}
protocols = {}
policies = {}
scalling = {}

def startEvaluation():
    start_time = time.time()

    path = "data/elb/sce"
    
    test = input("Selccione un escenario de prueba (Numero del 1 al 4)\n")
    path = path + test +"/"

    type = input("¿Quiere analizar los balanceadores de carga versión 1 (Classic Load Balancers) o balanceadores de carga versión 2 y 3 (Application Load Balancer y Network Load Balancer)?\n 1. Versión 1\n 2. Versión 2 y 3\n")
    if type=="1":
        with open(path+"classic_load_balancer_config.json") as c:
            classic = json.load(c)
            classic = classic["LoadBalancerDescriptions"]

        for i in range(0,len(classic)):
            lb_name = classic[i]["LoadBalancerName"]

            if "CanonicalHostedZoneNameID" in classic[i]:
                canonHostId = classic[i]["CanonicalHostedZoneNameID"]
                DNS(lb_name,canonHostId,path)
            else:
                dns[lb_name] = addToMapValue(dns, lb_name, "NO CUSTOM DNS")

            listeners = classic[i]["ListenerDescriptions"]

            #Protocols
            for k in range(0,len(listeners)):
                lis = listeners[k]

                if lis["Listener"]["Protocol"] != "HTTPS" and lis["Listener"]["Protocol"] != "SSL":
                    protocols[classic[i]["LoadBalancerName"]] = addToMapValue(protocols, classic[i]["LoadBalancerName"], "NO SECURE PROTOCOL")

            #Politicas
            target = classic[i]["HealthCheck"]["Target"]
            interval = classic[i]["HealthCheck"]["Interval"]
            timeout = classic[i]["HealthCheck"]["Timeout"]
            uThre = classic[i]["HealthCheck"]["UnhealthyThreshold"]
            hThre = classic[i]["HealthCheck"]["HealthyThreshold"]

            policiesE(classic, i,target,interval,timeout,uThre,hThre)
            autoScalling(path,lb_name)         
            generalClassic(classic, i,path)
    else:
        with open(path+"app-net_load_balancer_config.json") as a:
            appNet = json.load(a)
        
        appNet = appNet["LoadBalancers"]
   
        for j in range(0,len(appNet)):
            lb_name = appNet[j]["LoadBalancerName"]
            
            if "CanonicalHostedZoneId" in appNet[j]:
                canonHostId = appNet[j]["CanonicalHostedZoneId"]
                DNS(lb_name,canonHostId,path)
            else:
                dns[lb_name] = addToMapValue(dns, lb_name, "NO CUSTOM DNS")

            #Politicas

            with open(path+"describe-target-groups.json") as tg:
                targetG = json.load(tg)
                targetG = targetG["TargetGroups"]

            for k in range(0,len(targetG)):
                tGroup = targetG[k]
                
                target = tGroup["TargetGroupName"]
                interval = tGroup["HealthCheckIntervalSeconds"]
                timeout = tGroup["HealthCheckTimeoutSeconds"]
                uThre = tGroup["UnhealthyThresholdCount"]
                hThre = tGroup["HealthyThresholdCount"]

                policiesE(appNet, j,target,interval,timeout,uThre,hThre)
            autoScalling(path,lb_name)
            generalAN(appNet, j,path)

    result = printResult()
    exp = input("¿Desea exportar los resultados?\n1.Si\n2.No\n")
    if exp == "1":
        export.export(result)
    
    print(result)

    end_time = time.time()

    print("El tiempo de ejecución es:", end_time - start_time, "segundos")
    
def printResult():
    generalA = list(general.keys())
    dnsA = list(dns.keys())
    policiesA = list(policies.keys())
    protocolsA = list(protocols.keys())
    scallingA = list(scalling.keys())

    response = ""
    response+="\nEVALUACIÓN DE CONFIGURACIÓN DE BALANCEADORES DE CARGA\n"
    response+="\nASPECTOS GENERALES:\n"
    if len(generalA) !=0:
        for i in range(0, len(generalA)):
            balancer = generalA[i]
            response+=balancer+":\n"
            a = general[balancer]
            
            for j in range(0,len(a)):
                sep = a[j].split(':')
                if len(sep)>1:
                    if sep[1] == "DEACTIVATED":
                        response+="ADVERTENCIA - CIFRADO: Se encontró cifrado para el balanceador de carga pero este se encuentra desactivado, verifique el estado, su información podria no ser confidencial\n"
                    else:
                        response+="ERROR - CIFRADO: No se encontró cifrado para el balanceador de carga, verifique que exista o adicione uno, su información podria no ser confidencial\n"
                elif a[j] == "NO CIPHER ON LISTENER":
                    response+="ERROR - CIFRADO: No se encontró cifrado para los listeners del balanceador de carga, verifique que exista o adicionelo, su información podria no ser confidencial\n"
                elif a[j] == "NO INFO RECOVERY":
                    response+="ERROR - RECUPERACIÓN DE INFORMACIÓN: No se encontró uso de logs para el balanceador de carga, podria perderse información en caso de una eventualidad\n"
                elif a[j] == "OPEN PORTS":
                    response+="ERROR - CONTROL DE ACCESSO: El balanceador tiene todos los puertos abiertos para recibir trafico\n"
                elif a[j] == "NO IP RESTRICTION":
                    response+="ERROR - CONTROL DE ACCESO: No hay un rango de ip definido para comunicaciones entrantes (0.0.0.0/0), cualquier ip puede conectarse\n"
                elif a[j] == "OPEN PORTSB":
                    response+="ADVERTENCIA - CONTROL DE ACCESSO: El balanceador tiene todos los puertos abiertos para enviar trafico\n"
                elif a[j] == "NO IP RESTRICTIONB":
                    response+="ADVERTENCIA - CONTROL DE ACCESO: No hay un rango de ip definido para las comunicaciones salientes (0.0.0.0/0), asegurese que el balanceador de carga envia trafico hacia destinos autorizados\n"
                elif a[j] == "NO ACCESS CONTROL":
                    response+="ERROR - CONTROL DE ACCESO: No se encontró manejo de control de acceso en el balanceador, pueden haber conexiones no autorizadas\n"
    else:
        response+="No se encontraron configuraciones inadecuadas en el cifrado, recuperación de información o control de acceso para alguno de los balanceadores evaluados\n"
    
    response+="\nASPECTOS ESPECIFICOS:\n"
    response+="\nDNS:\n"
    if len(dnsA) !=0:
        for i in range(0, len(dnsA)):
            balancer = dnsA[i]
            response+=balancer+": "
            a = dns[balancer]
            
            for j in range(0,len(a)):
                if a[j] == "NO DNSSEC":
                    response+="ERROR - DNS: No se evidenció el uso del protocolo seguro DNSSEC para el DNS personalizado a traves del servicio Amazon Route 53, verifique la configuración del servicio de DNS o adicione la configuración, la comunicación con el servidor DNS puede no ser segura\n"
                else:
                    response+="ADVERTENCIA - DNS: Unicamente se tiene un direccionamiento por defecto a traves del DNS proporcionado de manera predeterminada por AWS, es necesario verificar manualmente el uso del protocolo DNSSEC, la comunicación con el servidor DNS puede no ser segura\n"
    else:
        response+="No se encontraron configuraciones inadecuadas en el DNS para alguno de los balanceadores evaluados\n"
    response+="\nPROTOCOLOS DEL BALANCEADOR DE CARGA:\n"
    if len(protocolsA) !=0:
        for i in range(0, len(protocolsA)):
            balancer = protocolsA[i]
            response+=balancer+": "
            a = protocols[balancer]
            if len(a) > 0: 
                response+="ERROR - PROTOCOLOS: No se evidenció el uso del protocolos seguros para la comunicación del balanceador de carga en "+str(len(a))+" Listeners, cambie los protocolos usados por sus versiones seguras, la comunicación no es segura\n"
                
    else:
        response+="No se encontraron configuraciones inadecuadas en los protocolos de comunicación para alguno de los balanceadores evaluados\n"

    response+="\nPOLITICAS SOBRE LOS TARGETS:\n"
    if len(policiesA) != 0:
        for i in range(0, len(policiesA)):
            balancer = policiesA[i]
            response+=balancer+":\n"
            a = policies[balancer]
            for j in range(0,len(a)):
                aS = a[j].split(':')

                if aS[0] == "TIMEOUTX":
                    response+="ERROR - VERIFICACIONES DE ESTADO: El tiempo que deben pasar sin respuesta a una verificación para que se considere fallida es mayor al tiempo entre verificaciones para el objetivo "+aS[1]+" asegurese de que el tiempo entre verificaciones siempre es mayor\n"
                elif aS[0] == "TIMEOUTA":
                    response+="ADVERTENCIA - VERIFICACIONES DE ESTADO: El tiempo que deben pasar sin respuesta a una verificación para que se considere fallida es alto para el objetivo "+aS[1]+", puede que no se identifiquen verificaciones fallidas a tiempo\n"
                elif aS[0] == "TIMEOUTB":
                    response+="ADVERTENCIA - VERIFICACIONES DE ESTADO: El tiempo que deben pasar sin respuesta a una verificación para que se considere fallida es bajo para el objetivo "+aS[1]+", puede que no se identifiquen correctamente verificaciones no fallidas\n"
                elif aS[0] ==  "UTHREA":
                    response+="ADVERTENCIA - VERIFICACIONES DE ESTADO: La cantidad de fallos que deben pasar para que se considere no sano el objetivo "+aS[1]+" es alta, puede que se considere el objetivo como no sano erroneamente\n"
                elif aS[0] ==  "UTHREB":
                    response+="ADVERTENCIA - VERIFICACIONES DE ESTADO: La cantidad de fallos que deben pasar para que se considere no sano el objetivo "+aS[1]+" es baja, puede que se considere el objetivo como no sano muy tarde\n"
                elif aS[0] == "HTHREA":
                    response+="ADVERTENCIA - VERIFICACIONES DE ESTADO: La cantidad de fallos que deben pasar para que se considere sano el objetivo "+aS[1]+" es alta, puede que se considere el objetivo como sano muy tarde\n"
                elif aS[0] == "HTHREB":
                    response+="ADVERTENCIA - VERIFICACIONES DE ESTADO: La cantidad de fallos que deben pasar para que se considere sano el objetivo "+aS[1]+" es baja, puede que se considere el objetivo como sano erroneamente\n"
                elif aS[0] == "INTERVALA":
                    response+="ADVERTENCIA - VERIFICACIONES DE ESTADO: El tiempo entre verificaciones de estado para el objetivo "+aS[1]+" es alta, es posible que no se omitan cambios de estado del objetivo\n"
                elif aS[0] == "INTERVALB":
                    response+="ADVERTENCIA - VERIFICACIONES DE ESTADO: El tiempo entre verificaciones de estado para el objetivo "+aS[1]+" es baja, es posible que no se de el tiempo necesario para realizar las verificaciones de estado\n"
    else:
        response+="No se encontraron configuraciones inadecuadas en las configuraciones de las verificaciones de estado para alguno de los balanceadores evaluados\n"
    
    response+="\nAUTOESCALADO:\n"
    if len(scallingA) !=0:
        for i in range(0, len(scallingA)):
            balancer = scallingA[i]
            response+=balancer+":\n"
            a = scalling[balancer]
            
            for j in range(0,len(a)):
                aS = a[j].split(':')
                if aS[0] == "BADMETRIC":
                    response+="ADVERTENCIA - AUTOESCALADO: La metrica usada en la politica "+aS[1]+" puede no funcionar bien para el tipo de la politica\n"
                elif aS[0] == "SCALEOUT":
                    response+="ERROR - "+aS[1]+" politicas de autoescalado estaticas que aumentan el numero de instancias necesitan una politica que reduzca el numero de instancias\n"
                elif aS[0] == "SCALEIN":
                    response+="ERROR - "+aS[1]+" politicas de autoescalado estaticas que reducen el numero de instancias necesitan una politica que aumenten el numero de instancias\n"

    else:
        response+="No se encontraron configuraciones inadecuadas en el autoescalado de alguno de los balanceadores evaluados\n"

    return response
    
def policiesE(lb, i, target,interval,timeout,uThre,hThre):
    if interval > 20:
        policies[lb[i]["LoadBalancerName"]] = addToMapValue(policies, lb[i]["LoadBalancerName"], "INTERVALA:"+target)
    elif interval < 10:
        policies[lb[i]["LoadBalancerName"]] =addToMapValue(policies, lb[i]["LoadBalancerName"], "INTERVALB:"+target)
    
    if timeout > interval:
        policies[lb[i]["LoadBalancerName"]] =addToMapValue(policies, lb[i]["LoadBalancerName"], "TIMEOUTX:"+target)
    elif timeout > 5:
        policies[lb[i]["LoadBalancerName"]] =addToMapValue(policies, lb[i]["LoadBalancerName"], "TIMEOUTA:"+target)
    elif timeout < 3:
        policies[lb[i]["LoadBalancerName"]] =addToMapValue(policies, lb[i]["LoadBalancerName"], "TIMEOUTB:"+target)

    if uThre > 4:
        policies[lb[i]["LoadBalancerName"]] =addToMapValue(policies, lb[i]["LoadBalancerName"], "UTHREA:"+target)
    elif uThre < 2:
        policies[lb[i]["LoadBalancerName"]] =addToMapValue(policies, lb[i]["LoadBalancerName"], "UTHREB:"+target)

    if hThre > 6:
        policies[lb[i]["LoadBalancerName"]] =addToMapValue(policies, lb[i]["LoadBalancerName"], "HTHREA:"+target)
    elif hThre < 2:
        policies[lb[i]["LoadBalancerName"]] =addToMapValue(policies, lb[i]["LoadBalancerName"], "HTHREB:"+target)


def DNS(lb_name, canonHostId,path):
    
    with open(path+canonHostId+"_dnssec_validation_app_lb.json") as ldns:
        dnssec= json.load(ldns)

    if dnssec["Status"]["ServeSignature"] == "NOT_SIGNING":
        dns[lb_name] = addToMapValue(dns, lb_name, "NO DNSSEC")

def autoScalling(path, lb_name):
    with open(path+"describe-auto-scaling-groups.json") as a:
        autoGroups= json.load(a)
        autoGroups= autoGroups["AutoScalingGroups"]

    for i in range(0,len(autoGroups)):
        group = autoGroups[i]

        name = group["AutoScalingGroupName"]

        with open(path+"autoscaling-describe-policies.json") as a:
            policies= json.load(a)
            policies= policies["ScalingPolicies"]

        scaleIn = 0
        scaleOut = 0

        for k in range(0,len(policies)):
            policy = policies[k]
            
            policyName = policy["PolicyName"]
            if policy["PolicyType"] == "TargetTrackingScaling":
                metric = policy["TargetTrackingConfiguration"]["PredefinedMetricSpecification"]["PredefinedMetricType"]
                if metric == "ALBRequestCountPerTarget":
                    scalling[lb_name] = addToMapValue(scalling, lb_name, "BADMETRIC:"+policyName)
            elif policy["PolicyType"] == "PredictiveScaling":
                metric = policy["TargetTrackingConfiguration"]["PredefinedMetricSpecification"]["PredefinedMetricType"]
                if metric == "ASGAverageNetworkIn" or metric == "ASGAverageNetworkOut":
                    scalling[lb_name] = addToMapValue(scalling, lb_name, "BADMETRIC:"+policyName)
            else:

                if policy["ScalingAdjustment"] > 0:
                    scaleIn+=1
                else:
                    scaleOut+=1

        if scaleIn > scaleOut:
            scalling[lb_name] = addToMapValue(scalling, lb_name, "SCALEOUT:"+str(scaleIn-scaleOut))
        elif scaleIn < scaleOut:
            scalling[lb_name] = addToMapValue(scalling, lb_name, "SCALEIN:"+str(scaleOut-scaleIn))


        


def generalClassic(classic, i, path): #O(b^2*p*a)

    #Cipher Classic 
    with open(path+"general_val/classic_lb_policies.json") as cc: #En realidad se ejecutaria el comando aws elb describe-load-balancer-policies --load-balancer-name <load-balancer-name> por cada balanceador
        policies = json.load(cc)
    policies= policies["PolicyDescriptions"]
    j=0
    cipherP = 0
    cipherPD = 0
    for j in range(0,len(policies)):
        policy = policies[j]

        if policy["PolicyTypeName"] == "SSLNegotiationPolicyType":
            cipherP+=1
            atributes = policy["PolicyAttributeDescriptions"]

            for k in range(0, len(atributes)):
                atribute = atributes[k]
                aName = atribute["AttributeName"]
                aValue = atribute["AttributeValue"]
            
                if ((aName == "Protocol-TLSv1.1") or (aName == "Protocol-TLSv1.2") or (aName == "Protocol-TLSv1.3")) and (aValue == "false"):
                    
                    cipherPD+=1

                  

    if cipherP > 0:
        if cipherPD > 0:
            general[classic[i]["LoadBalancerName"]] = addToMapValue(general, classic[i]["LoadBalancerName"], "CIPHER:DEACTIVATED:"+str(cipherPD))

    else:
        general[classic[i]["LoadBalancerName"]] = addToMapValue(general, classic[i]["LoadBalancerName"], "CIPHER:")
                  
    #Info recovery Classic
    with open(path+"general_val/info_rec_classic_lb.json") as cr: #En realidad se ejecutaria el comando aws elb describe-load-balancer-attributes --load-balancer-name <load-balancer-name> por cada balanceador
        lb_atr = json.load(cr)
        lb_atr = lb_atr["LoadBalancerAttributes"]

        if (lb_atr["AccessLog"] == None) or (lb_atr["AccessLog"]["Enabled"] == False):
            general[classic[i]["LoadBalancerName"]] = addToMapValue(general, classic[i]["LoadBalancerName"], "NO INFO RECOVERY")

    #Access Control
    if "SecurityGroups" in classic[i]:
        #c_sec_g = classic[i]["SecurityGroups"] en realidad deben detallarse todos los grupos de seguridad con el comando describe-security-groups --group-ids <security-group-id>
        accessControl(classic, i, path)
    else:
        general[classic[i]["LoadBalancerName"]] = addToMapValue(general, classic[i]["LoadBalancerName"], "NO ACCESS CONTROL")
    
   
def generalAN(appNet, i, path):          
    #Cipher App-Net 
    ty = appNet[i]["Type"]
    if ty == "application":
        with open(path+"/general_val/cipher_validation_app_lb.json") as app: #En realidad se ejecutaria el comando aws elbv2 describe-listeners --load-balancer-arn <load-balancer-arn> por cada balanceador
            listenersA = json.load(app)
        listenersA = listenersA["Listeners"]
        
        for j in range(0, len(listenersA)):
            lisA = listenersA[j]
            correctValues = {"TLS", "HTTPS"}
            if lisA["Protocol"] not in correctValues:
                protocols[appNet[i]["LoadBalancerName"]] = addToMapValue(protocols, appNet[i]["LoadBalancerName"], "NO SECURE PROTOCOL")

            if "SslPolicy" not in lisA:
                general[appNet[i]["LoadBalancerName"]] = addToMapValue(general, appNet[i]["LoadBalancerName"], "NO CIPHER ON LISTENER")

    else:
        with open(path+"/general_val/cipher_validation_net_lb.json") as app: #En realidad se ejecutaria el comando aws elbv2 describe-listeners --load-balancer-arn <load-balancer-arn> por cada balanceador
            listenersN = json.load(app)
        listenersN = listenersN["Listeners"]
        
        for j in range(0, len(listenersN)):
            lisN = listenersN[j]
            correctValues = {"TLS", "HTTPS"}
            if lisN["Protocol"] not in correctValues:
                protocols[appNet[i]["LoadBalancerName"]] = addToMapValue(protocols, appNet[i]["LoadBalancerName"], "NO SECURE PROTOCOL")

            if "SslPolicy" not in lisN:
                general[appNet[i]["LoadBalancerName"]] = addToMapValue(general, appNet[i]["LoadBalancerName"], "NO CIPHER ON LISTENER")

    #Info recovery App Net
    with open(path+"general_val/info_rec_app_lb.json") as anr: #En realidad se ejecutaria el comando aws elbv2 describe-load-balancer-attributes --load-balancer-arn <load-balancer-arn> por cada balanceador
        lb_atr = json.load(anr)
        lb_atr = lb_atr["Attributes"]

    w = 0
    ir = False
    while w <len(lb_atr)-1 and ir == False:
        at = lb_atr[w]
        if (at["Key"] == "access_logs.s3.enabled"):
            if (at["Value"] == "false"):
                general[appNet[i]["LoadBalancerName"]] = addToMapValue(general, appNet[i]["LoadBalancerName"], "NO INFO RECOVERY")

            ir = True
        w+=1

    #Access Control
    if "SecurityGroups" in appNet[i]:
        #an_sec_g = appNet[i]["SecurityGroups"] en realidad deben detallarse todos los grupos de seguridad con el comando describe-security-groups --group-ids <security-group-id>
        accessControl(appNet, i,path)
    else:
        general[appNet[i]["LoadBalancerName"]] = addToMapValue(general, appNet[i]["LoadBalancerName"], "NO ACCESS CONTROL")


def accessControl(lb,i, path):
    
    with open(path+"general_val/access_control_sec_groups_app_lb.json") as ca: #En realidad se ejecutaria el comando aws ec2 describe-security-groups --group-ids <security-group-id> por cada grupo de seguridad del balanceador
        sec_gd = json.load(ca)
        sec_gd = sec_gd["SecurityGroups"]

    for j in range(0,len(sec_gd)):
        ipPer = sec_gd[j]["IpPermissions"][0]

        correctValues = {"tcp", "udp", "icmp", "icmpv6"}
        if ipPer["IpProtocol"] not in correctValues:
            general[lb[i]["LoadBalancerName"]] = addToMapValue(general, lb[i]["LoadBalancerName"], "OPEN PORTS")

        ipRange = ipPer["IpRanges"][0]
        if ipRange["CidrIp"] == "0.0.0.0/0":
            general[lb[i]["LoadBalancerName"]] = addToMapValue(general, lb[i]["LoadBalancerName"], "NO IP RESTRICTION")
            
        ipPerE = sec_gd[j]["IpPermissionsEgress"][0]

        if ipPerE["IpProtocol"] not in correctValues:
            general[lb[i]["LoadBalancerName"]] = addToMapValue(general, lb[i]["LoadBalancerName"], "OPEN PORTSB")

        ipRange = ipPerE["IpRanges"][0]
        if ipRange["CidrIp"] == "0.0.0.0/0":
            general[lb[i]["LoadBalancerName"]] = addToMapValue(general, lb[i]["LoadBalancerName"], "NO IP RESTRICTIONB")

#MISC

def addToMapValue(map:dict, key, element):
    actualList:list = []
    if key in map:
        actualList = map[key]

    c = False
    x = 0
    while x < len(actualList) and c == False:
        if actualList[x] == element:
            c == True
        x+=1

    if c == False:

        actualList.append(element)

    return actualList
