from threading import Lock
import csv

class BaseDeDatos:
    def __init__(self):
        self.datos = {}

    def alta(self, clave: str, atributos: list) -> str:
        candado = Lock()
        atri_con_candado = [candado] + atributos
        if clave not in self.datos:
            self.datos[clave] = atri_con_candado

            # Vamos a comprobar que no han entrado varios clientes a la vez a dar de
            # alta en la base de datos a la misma clave.
            atri1, atri2, atri3 = (self.datos[clave][1], self.datos[clave][2],
                                   self.datos[clave][3])
            candado_actual = self.datos[clave][0]
            if (candado_actual == candado and atri1 == atributos[0] and
                    atri2 == atributos[1] and atri3 == atributos[2]):
                return (f"El registro del cliente con clave {clave} se ha registrado "
                        f"correctamente. ")
            else:
                return (f"Error: La clave {clave} ya existe en la base de datos. "
                        f"Inténtelo de nuevo.")
        else:
            return (f"Error: La clave {clave} ya existe en la base de datos. "
                        f"Inténtelo de nuevo.")


    def baja(self, clave: str, _) -> str:
        if clave not in self.datos:
            return (f"Error: La clave {clave} no existe en la base de datos. "
                    f"Inténtelo de nuevo.")
        else:
            try:
                candado = self.datos[clave][0]
                candado.acquire()
                try:
                    del self.datos[clave]
                    return (f"El registro del cliente con clave {clave} se ha "
                            f"eliminado correctamente. ")
                except:
                    return (f"Error: La clave {clave} no existe en la base de "
                            f"datos. Inténtelo de nuevo.")
                finally:
                    candado.release()

            except:
                return (f"Error: La clave {clave} no existe en la base de datos. "
                        f"Inténtelo de nuevo.")


    def consultar(self, clave: str, atributo: list) -> str:
        relacion_atrib_index = {"atributo1": 1, "atributo2": 2, "atributo3": 3}
        if clave in self.datos:
            atributo_minuscula = atributo[0].lower()  # Se coge el primer elem porque es una lista de un solo elem (el atributo)
            if atributo_minuscula not in relacion_atrib_index:
                return (f"Error: El atributo {atributo_minuscula} no existe en "
                        f"la base de datos. Inténtelo de nuevo.")
            index = relacion_atrib_index[atributo_minuscula]
            try:
                candado = self.datos[clave][0]
                candado.acquire()
                try:
                    consulta = self.datos[clave][index]
                    return (f"El {atributo_minuscula} para el registro con clave "
                            f"{clave} es: {consulta}")
                except:
                    return (f"Error: La clave {clave} no existe en la base de "
                            f"datos. Inténtelo de nuevo.")
                finally:
                    candado.release()

            except:
                return (f"Error: La clave {clave} no existe en la base de datos. "
                        f"Inténtelo de nuevo.")
        else:
            return (f"Error: La clave {clave} no existe en la base de datos. "
                    f"Inténtelo de nuevo.")


    def modificar(self, clave: str, valor: list[str]) -> str:
        relacion_concept_index = {"atributo1": 1, "atributo2": 2, "atributo3": 3}
        atributo, valor = valor[0].split("->")[0], valor[0].split("->")[1:]

        # Escribo .split() para quitar los espacios en blanco que pueda haber.
        atributo_minuscula = atributo.split()[0].lower()
        if atributo_minuscula not in relacion_concept_index:
            return (f"Error: El atributo {atributo_minuscula} no existe en la base de "
                    f"datos. Inténtelo de nuevo.")
        if clave in self.datos:
            index = relacion_concept_index[atributo_minuscula]
            try:
                candado = self.datos[clave][0]
                candado.acquire()
                try:
                    self.datos[clave][index] = "->".join(valor) # Porque hicimos split(->), por eso ponemos "->".join()
                    return (f"Se ha modificado correctamente el registro del cliente con "
                            f"clave {clave} en el atributo {atributo_minuscula}")
                except:
                    return (f"Error: La clave {clave} no existe en la base de "
                            f"datos. Inténtelo de nuevo.")
                finally:
                    candado.release()

            except:
                return (f"Error: La clave {clave} no existe en la base de datos. "
                        f"Inténtelo de nuevo.")

        else:
            return (f"Error: La clave {clave} no existe en la base de datos. "
                    f"Inténtelo de nuevo.")


    def guardar(self, nombre_archivo: str) -> None:
        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow(['Clave', 'atributo1', 'atributo2', 'atributo3'])
            # Escribir datos del diccionario
            for clave, valores in self.datos.items():
                escritor_csv.writerow([clave] + valores[1:])

    def cargar(self, nombre_archivo: str) -> None :
        with open(nombre_archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            next(lector_csv)
            for fila in lector_csv:
                clave = fila[0]
                valores = [valor for valor in fila[1:]]
                self.alta(clave, valores)