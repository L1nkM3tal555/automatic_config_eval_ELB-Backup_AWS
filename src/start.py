import elb as lb
import backup as b

if __name__ == "__main__":
    on = True
    while on:
        service = input("Elija el servicio a evaluar\n 1. Balanceador de carga (ELB)\n 2. Backup\n 3. Salir\n")
        if service == "1":
            lb.startEvaluation()
        elif service == "2":
            b.startEvaluation()
        elif service == "3":
            on = False
        else:
            print("Seleccione una opción valida")

