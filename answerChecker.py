from fractions import Fraction
from string import printable
import sys


class colors:
  FAIL = "\033[91m"
  ENDC = "\033[0m"
printable = "ñÑáéíóúÁÉÍÓÚ¿°" + printable
def answersChecker(rows, header, cants):
  try:
    for row in rows:  # Por cada cliente
      for i in range(6, len(row) - 1):  # Por cada producto
        if row[i] != "":
          while not isValid(row[i]):
            print(
              f"{colors.FAIL}La cantidad de '{header[i]}' ({row[2].strip().upper()}) es '{row[i]}' pero debería ser un número.{colors.ENDC}"
            )
            row[i] = input("Ingrese el nuevo valor para reemplazarlo: ")
          cants[i] += Fraction(row[i])
      else:
        if set(row[-1]).difference(printable):
          not_allowed = list(set(row[-1]).difference(printable))
          print(
            f"{colors.FAIL}El comentario de '{row[2].strip().upper()}' contiene caracteres no permitidos: {not_allowed}.{colors.ENDC}"
          )
          print(f"Comentario actual: {row[-1]}")
          row[-1] = input("Ingrese el nuevo comentario: ")
  except Exception:
    print(
      f"{colors.FAIL}Hubo un error al intentar validar los datos. Por favor, revise que los datos sean correctos.{colors.ENDC}"
    )
    input("Press RETURN...")
    sys.exit()


def isValid(num):
  try:
    float(Fraction(num))
    return True
  except ValueError:
    return False
