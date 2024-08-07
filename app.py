import re
import csv
import os
import sys
from answerChecker import answersChecker
from htmlHandler import create_html
from pdfHandler import create_pdf
from productsHandler import create_html_products

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
cants = []
for h in header:
  cants.append(0)
  price = (
    re.search(r"\$([0-9]+xKG)", h, re.IGNORECASE)
    or re.search(r"\$([0-9]+x[0-9]+gr)", h, re.IGNORECASE)
    or re.search(r"\$([0-9]+)", h)
    or None
  )
  prices.append(price.group()[1:] if price else "")

rows = []
for row in csvreader:
  rows.append(row)
file.close()

while header[-1] == "":
  for row in rows:
    if len(row) == len(header):
      row.pop()
  header.pop()

answersChecker(rows, header, cants)
create_html_products(header, cants)
create_pdf(rows, header, prices)
create_html(rows, header, prices)

os.system("start productos.html")
os.system("start comandas.pdf")
os.system("start comandas.html")
