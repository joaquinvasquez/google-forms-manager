import re
import csv
import os
import sys
from htmlHandler import create_html
from pdfHandler import create_pdf

try:
  file = open("Solicitud de pedido.csv", encoding="utf-8")
except OSError:
  print("No existe el archivo 'Solicitud de pedido.csv'")
  input("Press RETURN...")
  sys.exit()

type(file)
csvreader = csv.reader(file)
header = []
header = next(csvreader)
prices = []
for h in header:
  priceKG = re.search(r"\$([0-9]+xKg)", h) or re.search(r"\$([0-9]+xKG)", h)
  price = re.search(r"\$([0-9]+)", h)
  if priceKG:
    prices.append(f"{priceKG.group()[1:]}")
  elif price:
    prices.append(price.group()[1:])
  else:
    prices.append("")
rows = []
for row in csvreader:
  rows.append(row)
file.close()
# print(prices)
# print(header)
# print(rows)

create_html(rows, header, prices)
create_pdf(rows, header, prices)

os.system("start index.html")
os.system("start Comandas.pdf")
