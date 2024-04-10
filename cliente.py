from socket import socket


def imprimir_respuesta(respuesta: str) -> None:
    print(respuesta)
    print("")

def cremallera(lista1, lista2 : list) -> list:
    result = []
    for i in range(len(lista1)):
        result += [lista1[i], lista2[i]]
    return result

def nuevo_cliente(sckt: socket) -> None:
    accion = input("Introduce una acción para la base de datos (alta, baja, consultar, modificar o salir): ")
    accion = accion.split()[0] # Por si se escriben espacios
    while accion != "salir":
        clave = input("Clave del cliente: ")
        mensaje = [accion, clave]
        if accion not in ["alta", "baja", "consultar", "modificar"]:
            print("Esa acción no es válida. Inténtelo de nuevo.")
            print("")
        else:
            if accion == "alta":
                atributo1 = input("Atributo1 : ")
                atributo2 = input("Atributo2 : ")
                atributo3 = input("Atributo3 : ")
                mensaje.extend([atributo1, atributo2, atributo3])
            elif accion == "baja":
                mensaje.append(" ")
            elif accion == "consultar":
                atributo = input("Introduce el atributo a consultar (atributo1, atributo2, atributo3): ")
                mensaje.append(atributo)
            else:
                modif = input("Introduce el atributo (atributo1, atributo2, atributo3) y el nuevo valor a modificar separados por -> : ")
                mensaje.append(modif)

            barras = ["/"]*len(mensaje)
            list_palabras_barras = cremallera(mensaje, barras)

            mandar = "".join(list_palabras_barras)
            msj_env = mandar.encode()
            sckt.send(msj_env)
            msj_rec = sckt.recv(1024)
            respuesta = msj_rec.decode()

            imprimir_respuesta(respuesta)

        accion = input("Introduce una nueva operación para la base de datos (alta, baja, consultar, modificar o salir): ")

    sckt.close()

if __name__ == "__main__":
    sckt = socket()
    srvr_ip = 'localhost'
    srvr_puerto = 54321
    sckt.connect((srvr_ip, srvr_puerto))

    nuevo_cliente(sckt)