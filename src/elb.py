import json

import time


#"NO CIPHER", "CIPHER DEACTIVATED", "NO CIPHER ON LISTENER", "NO INFO RECOVERY",  "OPEN PORTS", "NO IP RESTRICTION"

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

    type = input("¿Quiere verificar tambien los Classic Load Balancers?\n 1.Si\n2.No")
    if type=="1":
        with open(path+"classic_load_balancer_config.json") as c:
            classic = json.load(c)
        classic = classic["LoadBalancerDescriptions"]

    with open(path+"app-net_load_balancer_config.json") as a:
        appNet = json.load(a)
    
    appNet = appNet["LoadBalancers"]

    with open(path+"list_hosted_zones_route53.json") as ldns:
        listHostedZones= json.load(ldns)
    listHostedZones = listHostedZones["HostedZones"]
    listHostedZones = extractHostedZones(listHostedZones)

    if classic:
        for i in range(0,len(classic)):
            lb_name = classic[i]["LoadBalancerName"]
            lb_dns_name = classic[i]["DNSName"]

            DNS(lb_name,lb_dns_name,listHostedZones,path)

            listeners = classic[i]["ListenerDescriptions"]

            #Protocols
            for k in range(0,len(listeners)):
                lis = listeners[k]
                if lis["Listener"]["Protocol"] != "HTTPS" or lis["Listener"]["Protocol"] != "SSL":
                    protocols[classic[i]["LoadBalancerName"]] = addToMapValue(protocols, classic[i]["LoadBalancerName"], "NO SECURE PROTOCOL")

            generalClassic(classic, i,path)
        
    for j in range(0,len(appNet)):
        lb_name = appNet[j]["LoadBalancerName"]
        lb_dns_name = appNet[j]["DNSName"]
        DNS(lb_name,lb_dns_name,listHostedZones,path)
        generalAN(appNet, j,path)

    printResult()

    end_time = time.time()

    print("El tiempo de ejecución es:", end_time - start_time, "segundos")
    
def printResult():
    generalA = list(general.keys())
    dnsA = list(dns.keys())
    protocolsA = list(protocols.keys())
    scallingA = list(scalling.keys())
    print("EVALUACIÓN DE CONFIGURACIÓN DE BALANCEADORES DE CARGA")
    print("\nASPECTOS GENERALES:\n")
    if len(generalA) !=0:
        for i in range(0, len(generalA)):
            balancer = generalA[i]
            print(balancer+":")
            a = general[balancer]
            
            for j in range(0,len(a)):
                if a[j] == "NO CIPHER":
                    print("ERROR - CIFRADO: No se encontró cifrado para el balanceador de carga, verifique que exista o adicione uno, su información podria no ser confidencial")
                elif a[j] == "CIPHER DEACTIVATED":
                    print("ADVERTENCIA - CIFRADO: Se encontró cifrado para el balanceador de carga pero este se encuentra desactivado, verifique el estado, su información podria no ser confidencial")
                elif a[j] == "NO CIPHER ON LISTENER":
                    print("ERROR - CIFRADO: No se encontró cifrado para los listeners del balanceador de carga, verifique que exista o adicionelo, su información podria no ser confidencial")
                elif a[j] == "NO INFO RECOVERY":
                    print("ERROR - RECUPERACIÓN DE INFORMACIÓN: No se encontró uso de logs para el balanceador de carga, podria perderse información en caso de una eventualidad")
                elif a[j] == "OPEN PORTS":
                    print("ADVERTENCIA - CONTROL DE ACCESSO: Se esta permitiendo la comunicación a traves de varios puertos, asegurese de que no tiene mas puertos abiertos de los que realmente esta usando")
                elif a[j] == "NO IP RESTRICTION":
                    print("ERROR - CONTROL DE ACCESO: No hay un rango de ip definido para la comunicación (0.0.0.0/0), cualquier ip puede conectarse")
                elif a[j] == "NO ACCESS CONTROL":
                    print("ERROR - CONTROL DE ACCESO: No se encontró manejo de control de acceso en el balanceador, pueden haber conexiones no autorizadas")
    else:
        print("No se encontraron configuraciones inadecuadas en el cifrado, recuperación de información o control de acceso para alguno de los balanceadores evaluados")
    
    print("\nASPECTOS ESPECIFICOS:\n")
    #print("DNS:")
    if len(dnsA) !=0:
        for i in range(0, len(dnsA)):
            balancer = dnsA[i]
            print(balancer+":")
            a = dns[balancer]
            
            for j in range(0,len(a)):
                if a[j] == "NO DNSSEC":
                    print("ERROR - DNS: No se evidenció el uso del protocolo seguro DNSSEC para el DNS personalizado a traves del servicio Amazon Route 53, verifique la configuración del servicio de DNS o adicione la configuración, la comunicación con el servidor DNS puede no ser segura")
                else:
                    print("ADVERTENCIA - DNS: Unicamente se tiene un direccionamiento por defecto a traves del DNS proporcionado de manera predeterminada por AWS, es necesario verificar manualmente el uso del protocolo DNSSEC, la comunicación con el servidor DNS puede no ser segura")
    else:
        print("No se encontraron configuraciones inadecuadas en el DNS para alguno de los balanceadores evaluados")

    if len(protocolsA) !=0:
        for i in range(0, len(protocolsA)):
            balancer = protocolsA[i]
            print(balancer+":")
            a = protocols[balancer]
            
            for j in range(0,len(a)):
                if a[j] == "NO SECURE PROTOCOL":
                    print("ERROR - PROTOCOLOS: No se evidenció el uso del protocolos seguros para la comunicación del balanceador de carga, cambie los protocolos usados por sus versiones seguras, la comunicación no es segura")
                
    else:
        print("No se encontraron configuraciones inadecuadas en los protocolos de comunicación para alguno de los balanceadores evaluados")

    if len(scallingA) !=0:
        for i in range(0, len(scallingA)):
            balancer = scallingA[i]
            print(balancer+":")
            a = scalling[balancer]
            
            for j in range(0,len(a)):
                if a[j] == "LIMIT EXCEDED":
                    print("ERROR - AUTOESCALADO: Se han alcanzado los limites de autoescalado, el balanceador de carga puede fallar lidiando con grandes cantidades de trafico")
                
    else:
        print("No se encontraron configuraciones inadecuadas en el autoescalado de alguno de los balanceadores evaluados")
    

def DNS(lb_name, lb_dns_name, listHostedZones,path):
    k=0
    f = False
    while k < len(listHostedZones) and f == False:
        hz = listHostedZones[k]

        with open(path+hz+"_asociation_val.json") as asoc:
            aso= json.load(asoc)
        aso=aso["ResourceRecordSets"]

        for o in range(0,len(aso)):

            if aso[o]["AliasTarget"]["DNSName"] == lb_dns_name:

                with open(path+hz+"_dnssec_validation_app_lb.json") as ldns:
                    dnssec= json.load(ldns)
                if dnssec["Status"]["ServeSignature"] == "NOT_SIGNING":
                    dns[lb_name] = addToMapValue(general, lb_name, "NO DNSSEC")

                f =True
        k+=1

    if f == False:
        dns[lb_name] = addToMapValue(general, lb_name, "NO CUSTOM DNS")
        



def extractHostedZones(hz):
    n_hz = []
    for k in range(0,len(hz)):
        n_hz.append(hz[k]["Id"].split('/')[2])
    return n_hz

def generalClassic(classic, i, path): #O(b^2*p*a)

    #Cipher Classic 
    with open(path+"general_val/classic_lb_policies.json") as cc: #En realidad se ejecutaria el comando aws elb describe-load-balancer-policies --load-balancer-name <load-balancer-name> por cada balanceador
        policies = json.load(cc)
    policies= policies["PolicyDescriptions"]

    for j in range(0,len(policies)):
        policy = policies[j]
        atributes = policy["PolicyAttributeDescriptions"]

        for k in range(0, len(atributes)):
            atribute = atributes[k]
            aName = atribute["AttributeName"]
            if (aName != "Server-Defined-Cipher-Order"):
                if (aName != "Protocol-TLSv1.1") or (aName != "Protocol-TLSv1.2") or (aName != "Protocol-TLSv1.3") or (aName != "Server-Defined-Cipher-Order"):
                    general[classic[i]["LoadBalancerName"]] = addToMapValue(general, classic[i]["LoadBalancerName"], "NO CIPHER")
                else:
                    aValue = atribute["AttributeValue"]
                    if aValue == "false":
                        general[classic[i]["LoadBalancerName"]] = addToMapValue(general, classic[i]["LoadBalancerName"], "CIPHER DEACTIVATED")
    #Info recovery Classic
    with open(path+"general_val/info_rec_classic_lb.json") as cr: #En realidad se ejecutaria el comando aws elb describe-load-balancer-attributes --load-balancer-name <load-balancer-name> por cada balanceador
        lb_atr = json.load(cr)
        lb_atr = lb_atr["LoadBalancerAttributes"]

        if (lb_atr["AccessLog"] == None) or (lb_atr["AccessLog"]["Enabled"] == "false"):
            general[classic[i]["LoadBalancerName"]] = addToMapValue(general, classic[i]["LoadBalancerName"], "NO INFO RECOVERY")

    #Access Control
    if "SecurityGroups" in classic[i]:
        c_sec_g = classic[i]["SecurityGroups"]
        accessControl(c_sec_g,classic, i, path)
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
            if lisA["SslPolicy"] == None:
                general[appNet[i]["LoadBalancerName"]] = addToMapValue(general, appNet[i]["LoadBalancerName"], "NO CIPHER ON LISTENER")

                protocols[appNet[i]["LoadBalancerName"]] = addToMapValue(protocols, appNet[i]["LoadBalancerName"], "NO SECURE PROTOCOL")
    else:
        with open(path+"/general_val/cipher_validation_app_lb.json") as app: #En realidad se ejecutaria el comando aws elbv2 describe-listeners --load-balancer-arn <load-balancer-arn> por cada balanceador
            listenersN = json.load(app)
        listenersN = listenersN["Listeners"]
        
        for j in range(0, len(listenersN)):
            lisN = listenersN[j]
            if lisN["SslPolicy"] == None:
                general[appNet[i]["LoadBalancerName"]] = addToMapValue(general, appNet[j]["LoadBalancerName"], "NO CIPHER ON LISTENER")
                protocols[appNet[i]["LoadBalancerName"]] = addToMapValue(protocols, appNet[j]["LoadBalancerName"], "NO SECURE PROTOCOL")

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
        an_sec_g = appNet[i]["SecurityGroups"]
        accessControl(an_sec_g,appNet, i,path)
    else:
        general[appNet[i]["LoadBalancerName"]] = addToMapValue(general, appNet[i]["LoadBalancerName"], "NO ACCESS CONTROL")


def accessControl(sec_g, lb, i, path):
    for s in range(0,len(sec_g)):
        with open(path+"general_val/access_control_sec_groups_app_lb.json") as ca: #En realidad se ejecutaria el comando aws ec2 describe-security-groups --group-ids <security-group-id> por cada grupo de seguridad del balanceador
            sec_g = json.load(ca)
        sec_g = sec_g["SecurityGroups"]

        for i in range(0,len(sec_g)):
            ipPer = sec_g[i]["IpPermissions"][0]

            if ipPer["FromPort"] != ipPer["FromPort"]:
                general[lb[i]["LoadBalancerName"]] = addToMapValue(general, lb[i]["LoadBalancerName"], "OPEN PORTS")

            ipRange = ipPer["IpRanges"][0]
            if ipRange["CidrIp"] == "0.0.0.0/0":
                general[lb[i]["LoadBalancerName"]] = addToMapValue(general, lb[i]["LoadBalancerName"], "NO IP RESTRICTION") #:+sec_g[s]["GroupName"]

#MISC

def addToMapValue(map:dict, key, element):
    actualList:list = []
    if key in map == True:
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
