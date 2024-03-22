from fractions import Fraction


class colors:
  FAIL = "\033[91m"
  ENDC = "\033[0m"


def answersChecker(rows, header, cants):
  for row in rows:  # Por cada cliente
    for i in range(6, len(row) - 1):  # Por cada producto
      if row[i] != "":
        while not isValid(row[i]):
          print(
            f"{colors.FAIL}La cantidad de '{header[i]}' ({row[2].strip().upper()}) es '{row[i]}' pero debería ser un número.{colors.ENDC}"
          )
          num = input("Ingrese el nuevo valor para reemplazarlo: ")
          row[i] = num
        cants[i] += Fraction(row[i])


def isValid(num):
  try:
    float(Fraction(num))
    return True
  except ValueError:
    return False
