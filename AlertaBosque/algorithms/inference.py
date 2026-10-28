"""Punto 2. Inferencia exacta por enumeración."""
from algorithms.probability import normalize


def enumeration_ask(network, query: str, evidence: dict) -> dict:
    """Calcula P(query | evidence) sobre la conjunta factorizada.

    Entradas: network es la red; query es el nombre de la
    variable consultada; evidence es {nombre de variable: 0 o 1}.
    Salida: {0: probabilidad, 1: probabilidad}.

    Tips:
    - Recorra network.variables en orden topológico.
    - Para una variable fijada multiplique su probabilidad; para una oculta
      sume las dos alternativas 0 y 1. Normalice al terminar.
    - Use copias del evento y no modifique evidence.
    - network.probability(variable, valor, evento) consulta la CPT;
      el evento debe contener los valores de todos los padres.
    - Puede usar una función auxiliar recursiva. Al terminar el recorrido,
      el producto sin factores restantes vale 1.
    - Evidencia imposible: ValueError. Consulta observada: distribución puntual
      solo si la evidencia es posible.
    """
    # Valida nombres de variables y dominio de la evidencia.
    network.validate_query(query, evidence)

    # TODO: Add your code here
    
    def enumerate_all(variables, event):
        if not variables:
            return 1.0
        first = variables[0]
        rest = variables[1:]

        if first in event:
          probability = network.probability(first, event[first], event)
          return probability * enumerate_all(rest, event)

        
        total = 0.0

        for value in [0, 1]:
          new_event = event.copy()
          new_event[first] = value

          probability = network.probability(first, value, new_event)
          total += probability * enumerate_all(rest, new_event)

        return total

    if query in evidence:
        probability_evidence = enumerate_all(
            network.variables, evidence.copy()
        )

        if probability_evidence == 0:
            raise ValueError("La evidencia es imposible")

        return {
            0: 1.0 if evidence[query] == 0 else 0.0,
            1: 1.0 if evidence[query] == 1 else 0.0
        }


    weights = {}

    for value in [0, 1]:
        new_evidence = evidence.copy()
        new_evidence[query] = value

        weights[value] = enumerate_all(
            network.variables, new_evidence
        )


    if sum(weights.values()) == 0:
        raise ValueError("La evidencia es imposible")

    return normalize(weights)

