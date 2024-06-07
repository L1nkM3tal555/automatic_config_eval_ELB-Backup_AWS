import elb as lb
import backup as b

if __name__ == "__main__":
    on = True
    while on:
        service = input("Elija el servicio a evaluar\n 1. Balanceador de carga (ELB)\n 2. Backup\n")
        if service == "1":
            lb.startEvaluation()
        elif service == "2":
            b.startEvaluation()
        else:
            print("Seleccione una opción valida")

