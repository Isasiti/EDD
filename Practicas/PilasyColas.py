import random

class Node:
  __slots__ = ('__value','__next')

  def __init__(self,value):
    self.__value = value
    self.__next = None

  def __str__(self):
    return str(self.__value)

  @property
  def next(self):
    return self.__next

  @next.setter
  def next(self,node):
    if node is not None and not isinstance(node,Node):
      raise TypeError("next debe ser un objeto tipo nodo ó None")
    self.__next = node

  @property
  def value(self):
    return self.__value

  @value.setter
  def value(self,newValue):
    if newValue is None:
      raise TypeError("el nuevo valor debe ser diferente de None")
    self.__value = newValue


class LinkedList:

  def __init__(self):
    self.__head = None
    self.__tail = None
    self.__size = 0

  @property
  def head(self):
    return self.__head

  @property
  def tail(self):
    return self.__tail

  @property
  def size(self):
    return self.__size

  @head.setter
  def head(self,node):
    if node is not None and not isinstance(node,Node):
      raise TypeError("Head debe ser un objeto tipo nodo ó None")
    self.__head = node

  @tail.setter
  def tail(self,node):
    if node is not None and not isinstance(node,Node):
      raise TypeError("Tail debe ser un objeto tipo nodo ó None")
    self.__tail = node

  @size.setter
  def size(self,num):
    self.__size = num

  def __str__(self):
    result = [str(nodo.value) for nodo in self]
    return ' <--> '.join(result)

  def print(self):
    for nodo in self:
      print(str(nodo.value))

  def __iter__(self):
    current = self.__head
    while current is not None:
      yield current
      current = current.next

  def append(self,value):
    newnode = Node(value)
    if self.__head is None:
      self.__head = newnode
      self.__tail = newnode
    else:
      self.__tail.next = newnode
      self.__tail = newnode
    self.__size += 1


  def popfirst(self):
    tempNode = self.__head
    if self.__head is None:
      return False
    elif self.__size == 1:
      self.__head = None
      self.__tail = None
      self.__size = 0
    else:
      self.__head = self.__head.next
      self.__size -= 1

    tempNode.next = None  #limpiar la referencia al segundo nodo, ahora nueva cabeza
    return tempNode

  def pop(self):

    if self.__head is None:
      print("No hay elementos en la lista")
      return None
    elif self.__size == 1:
      popped_node = self.__head
      self.__head = None
      self.__tail = None
      self.__size = 0
      return popped_node
    else:
      #print("self.__tail",self.__tail)
      popped_node = self.__tail
      #obtener el penultimo
      #1ra forma new_tail = self.get_by_index(customll.size-2)

      #2da forma
      current_node = self.__head
      for _ in range(self.__size-2):
        current_node = current_node.next
      current_node.next = None
      self.__tail = current_node
      self.__size -= 1
      return popped_node
class Queue:

  def __init__(self):
    self.__q = LinkedList()


  def enqueue(self, e):
    self.__q.append(e)
    return True

  def dequeue(self):

    if self.is_empty():
      return "No hay elementos en la cola"

    temp_node = self.__q.popfirst()
    return temp_node.value

  def is_empty(self):

    return self.__q.size == 0

  def len(self):
    return self.__q.size

  def firs(self):
    if self.is_empty():
      return "No hay elementos en la cola"

    return self.__q.head.value

  def first(self):
    return self.firs()

  def __str__(self):
    result = [str(nodo.value) for nodo in self.__q]
    return ' -- '.join(result)

class Stack:
  def __init__(self):
    self.__s = LinkedList()
  def push(self, e):
    self.__s.append(e)
    return True
  def pop(self):
    if self.is_empty():
      return "No hay elementos en la pila"
    temp_node = self.__s.pop()
    return temp_node.value
  def is_empty(self):
    return self.__s.size == 0
  def len(self):
    return self.__s.size
  def top(self):
    if self.is_empty():
      return "No hay elementos en la pila"

    return self.__s.tail.value
  def __str__(self):
    result = [str(nodo.value) for nodo in self.__s]
    return ' | '.join(result)

  def __iter__(self):
    current = self.__s.head
    while current is not None:
      yield current
      current = current.next

class Area:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad
        self.cola_pacientes = Queue() # Usando tu clase Queue

    def __str__(self):
        return f"{self.nombre} (Esperando: {self.cola_pacientes.len()})"
class Laboratorio:
    def __init__(self):
        self.pila_areas = Stack() # Usando tu clase Stack

    def agregar_area(self, nombre, capacidad):
        nueva_area = Area(nombre, capacidad)
        self.pila_areas.push(nueva_area)

    def agregar_paciente(self, nombre_paciente):
        if self.pila_areas.is_empty():
            print("No hay áreas en el sistema.")
            return
        # El paciente entra al área en el tope de la pila
        area_tope = self.pila_areas.top()
        area_tope.cola_pacientes.enqueue(nombre_paciente)
        print(f"Paciente {nombre_paciente} ingresó a {area_tope.nombre}.")

    def ejecutar_turno(self):
        if self.pila_areas.is_empty():
            return

        pila_aux = Stack()
        # Cola temporal para guardar quiénes pasan a la siguiente área
        # Para evitar que un paciente avance 2 áreas en un mismo turno
        transito = Queue() 

        print("\n--- EJECUTANDO TURNO ---")

        # 1. Procesar de arriba hacia abajo (LIFO)
        while not self.pila_areas.is_empty():
            area_actual = self.pila_areas.pop()
            
            procesados_este_area = Queue()
            print(f"\nÁrea: {area_actual.nombre}")
            
            # Atender según capacidad
            count = 0
            while count < area_actual.capacidad and not area_actual.cola_pacientes.is_empty():
                paciente = area_actual.cola_pacientes.dequeue()
                procesados_este_area.enqueue(paciente)
                count += 1
            
            print(f"Atendidos: {procesados_este_area}")
            print(f"En espera: {area_actual.cola_pacientes}")

            # Los pacientes atendidos aquí se guardan para el área que sigue (abajo)
            # Primero guardamos los que ya venían de arriba en el área actual
            while not transito.is_empty():
                area_actual.cola_pacientes.enqueue(transito.dequeue())
            
            # Ahora los que acabamos de procesar pasan al "transito" para la siguiente área
            while not procesados_este_area.is_empty():
                transito.enqueue(procesados_este_area.dequeue())

            pila_aux.push(area_actual)

        # 2. Restaurar la pila original
        while not pila_aux.is_empty():
            self.pila_areas.push(pila_aux.pop())

    def eliminar_area(self, nombre_area):
        pila_aux = Stack()
        area_a_eliminar = None

        while not self.pila_areas.is_empty():
            area = self.pila_areas.pop()
            if area.nombre == nombre_area:
                area_a_eliminar = area
                break
            pila_aux.push(area)

        if area_a_eliminar is None:
            print(f"Área {nombre_area} no encontrada.")
        else:
            if not self.pila_areas.is_empty():
                siguiente_area = self.pila_areas.top()
                while not area_a_eliminar.cola_pacientes.is_empty():
                    siguiente_area.cola_pacientes.enqueue(area_a_eliminar.cola_pacientes.dequeue())
                print(f"Área {nombre_area} eliminada. Pacientes movidos a {siguiente_area.nombre}.")
            else:
                print(f"Área {nombre_area} eliminada. No hay área para transferir pacientes.")

        while not pila_aux.is_empty():
            self.pila_areas.push(pila_aux.pop())

    def tiene_pacientes_pendientes(self):
        current = self.pila_areas._Stack__s.head
        while current is not None:
            if not current.value.cola_pacientes.is_empty():
                return True
            current = current.next
        return False

def menu():
    lab = Laboratorio()
    # Configuración inicial (Orden inverso para que Toma sea el tope)
    lab.agregar_area("Entrega de resultados", 2)
    lab.agregar_area("Validación de resultados", 1)
    lab.agregar_area("Análisis", 2)
    lab.agregar_area("Toma de muestras", 3)

    while True:
        print("\n--- SISTEMA CLÍNICO EDD 2026-1 ---")
        print("1. Agregar Paciente")
        print("2. Ejecutar Turno Manual")
        print("3. Ejecutar Automático (Hasta vaciar)")
        print("4. Agregar Nueva Área")
        print("5. Eliminar Área")
        print("6. Salir")
        
        op = input("Seleccione: ")
        
        if op == "1":
            nombre = input("Nombre del paciente: ")
            lab.agregar_paciente(nombre)
        elif op == "2":
            lab.ejecutar_turno()
        elif op == "3":
            if not lab.tiene_pacientes_pendientes():
                print("No hay pacientes en ninguna área.")
            else:
                turno = 1
                while lab.tiene_pacientes_pendientes():
                    print(f"\n=== TURNO AUTOMÁTICO {turno} ===")
                    lab.ejecutar_turno()
                    turno += 1
                print("\nTodos los pacientes han sido atendidos.")
        elif op == "4":
            nombre_area = input("Nombre de la nueva área: ")
            try:
                capacidad = int(input("Capacidad de la nueva área: "))
                if capacidad <= 0:
                    raise ValueError
            except ValueError:
                print("Capacidad inválida. Debe ser un número entero positivo.")
            else:
                lab.agregar_area(nombre_area, capacidad)
                print(f"Área '{nombre_area}' agregada con capacidad {capacidad}.")
        elif op == "5":
            nombre_area = input("Nombre del área a eliminar: ")
            lab.eliminar_area(nombre_area)
        elif op == "6":
            break
if __name__ == "__main__":
    menu()