"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""
    def __init__(self, max_iters : int = 20):
        super().__init__()
        #Elegimos 20 reinicios por defecto tras realizar pruebas por incremento de un reinicio a la vez, fue el mejor
        #Resultado para la instancia mas grande
        #Las pruebas se encuentran en el archivo AnalisisHillClimbingReinicioAleatorio.xls
        self.max_iters: int = max_iters
        
    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)
        self.value = value
        self.tour = actual
        
        for i in range(self.max_iters):
            
            while True:
                # Buscamos la acción que genera el sucesor con mayor valor objetivo
                act, succ_val = problem.max_action(actual)
                # Hacemos un break si estamos en un maximo local:
                # el valor objetivo del sucesor es menor o igual al del estado actual
                if succ_val <= value:
                    break

                # Sino, nos movemos al sucesor
                actual = problem.result(actual, act)
                value = succ_val
                self.niters += 1
                
            if(self.value < value):
                self.value = value
                self.tour = actual
            
            actual = problem.random_reset()
            value = problem.obj_val(actual)
        
        end = time()
        self.time = end-start    
            


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""
    def __init__(self):
        super().__init__()
        self.tabu : list[tuple[int,int]] = []
        #Elegimos el valor 10 por defecto porque es el que mejor resultados consistentes obtiene en todos las instancias
        self.tabu_max_size : int = 10
        #Elegimos 3 segundos porque para la instancia mas grande nos permite mejorar el valor objetivo sin gran costo de tiempo
        self.max_runtime : float = 3
        
    def solve(self, problem: OptProblem):
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)
        self.value = value
        self.tour = actual
        
        while(self.time <= self.max_runtime):
            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            # Modificamos el metodo max_action para que reciba una lista tabu
            act, succ_val = problem.max_action(actual,self.tabu)
            self.add(act)
            actual = problem.result(actual, act)
            value = succ_val
            if(self.value < value):
                self.value = value
                self.tour = actual
            self.niters += 1
            end = time()
            self.time = end-start
            
    def is_empty(self):
        return self.tabu == []
    
    def pop(self):
        if(not self.is_empty()):
            return self.tabu.pop(0)
    
    def add(self, action : tuple[int,int]):
        if(len(self.tabu) == self.tabu_max_size):
            self.pop()
        self.tabu.append(action)