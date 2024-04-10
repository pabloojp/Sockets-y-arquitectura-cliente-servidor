from socket import socket
from threading import Thread
from base_de_datos import BaseDeDatos
import os


def cargar_baseDatos() -> BaseDeDatos:
    accion = input("¿Desea crear una nueva base de datos o cargar una ya existente? (nueva o cargar): ")
    bd = BaseDeDatos()
    while accion not in ["cargar", "nueva"]:
        print("Error. Inténtalo de nuevo.")
        print()
        accion = input("¿Desea crear una nueva base de datos o cargar una ya existente? (nueva o cargar): ")
    if accion == "cargar":
        nombre_BD = input("Nombre de la base de datos que desea cargar: ")
        if nombre_BD in os.listdir(os.getcwd()):
            bd.cargar(nombre_BD)
            print("Base de datos cargada completamente.")
            print()
        else:
            print("El nombre de la base de datos no se encuentra en la carpeta. Se ha creado una nueva vacía")
            print()
    return bd

def administrador(_) -> None:
    clave = input("Ingrese la contraseña de administrador para cerrar el servidor (1234): ")
    while clave != "1234":
        print("Contraseña incorrecta. Intentalo de nuevo.")
        print("")
        clave = input("Ingrese la contraseña de administrador para cerrar el servidor (1234): ")
    else:
        print("¡Contraseña correcta!")
        deseo = input("¿Desea acabar con la ejecución del servidor? (Y/N): ")
        while deseo != "Y":
            print("Vale.")
            print("")
            deseo = input("¿Desea acabar con la ejecución del servidor? (Y/N): ")

        guardar = input("¿Desea guardar la base de datos? (Y/N): ")
        if guardar == "Y":
            nombre_arch = input("Nombre del archivo para guardar la base de datos: ")
            bd.guardar(nombre_arch)


def modificar_base_datos(accion, clave : str, atributos: list) -> str:
    funcion = getattr(bd, accion)
    respuesta = funcion(clave, atributos)
    return respuesta


def tarea_cliente(cl_socket: socket) -> None:
    msj_rec = cl_socket.recv(1024)
    while msj_rec:
        pregunta = msj_rec.decode()
        mensaje = pregunta.split("/")[:-1]  # -1 porque el último es un str vacío
        accion, clave, atributos = mensaje[0], mensaje[1], mensaje[2:]
        respuesta = modificar_base_datos(accion, clave, atributos)
        msj_env = respuesta.encode()
        cl_socket.send(msj_env)
        msj_rec = cl_socket.recv(1024)
    cl_socket.close()

def main(srvr_socket: socket) -> None:
    admin = Thread(target=administrador, args= ("",))
    admin.start()
    hebras = []
    while admin.is_alive():
        try:
            cl_socket,_ = srvr_socket.accept()   # Espera 10s una nueva conexión, sino, vuelve a empezar el bucle.
            hebra = Thread(target=tarea_cliente, args=(cl_socket,))
            hebra.start()
            hebras.append(hebra)
        except:
            pass
    for hebra in hebras:
        hebra.join()
    srvr_socket.close()


if __name__ == "__main__":
    srvr_socket = socket()
    ip_addr = 'localhost'
    puerto = 54321
    srvr_socket.bind((ip_addr, puerto))
    srvr_socket.settimeout(10)
    srvr_socket.listen()

    bd = cargar_baseDatos()

    main(srvr_socket)
