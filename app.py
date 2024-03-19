import re
import csv
import os
import sys
from airium import Airium
from fractions import Fraction
from datetime import datetime

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

a = Airium()
a("<!DOCTYPE html>")
with a.html(lang="es"):
  with a.head():
    a.meta(charset="UTF-8")
    a.meta(name="viewport", content="width=device-width, initial-scale=1")
    a.title(_t="Comandas Reverdecer")
    a.link(
      rel="stylesheet",
      href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
    )
    a.link(rel="stylesheet", href="style.css")
#     a.style(
#       _t="""
#       *,
#       *::before,
#       *::after {
#         box-sizing: border-box;
#       }
#       *::-webkit-scrollbar {
#         width: 12px;
#       }
#       *::-webkit-scrollbar-track {
#         background: #f0f0f0;
#         border: 2px solid transparent;
#         scrollbar-gutter: stable;
#       }
#       *::-webkit-scrollbar-thumb {
#         border-radius: 20px;
#         border: 2px solid transparent;
#         box-shadow: inset 0 0 10px 10px #aaa;
#       }
#       html {
#         background: #f0f0f0;
#       }
#       body {
#         font-family: 'Lato', sans-serif;
#         margin: 0;
#         padding: 0;
#         width: 100%;
#         height: 100dvh;
#         display: flex;
#         flex-direction: column;
#         justify-content: center;
#         align-items: center;
#       }
#       h1 {
#         margin-top: 0;
#         color: #333;
#       }
#       body .table-container {
#         background: #fff;
#         max-height: 80vh;
#         width: 80%;
#         overflow-y: auto;
#       }
#       table {
#         width: 100%;
#         border-collapse: collapse;
#         table-layout: fixed;
#         border: 2px solid #333;
#       }
#       table th {
#         background-color: lightsteelblue;
#         border: 2px solid #333;
#         padding: 10px 0;
#       }
#       table td {
#         border: 1px solid #333;
#       }
#       table .name {
#         width: 200px;
#       }
#       table .quantity,
#       table .value {
#         width: 100px;
#       }
#       table .number {
#         text-align: center;
#       }
#       table .client-name {
#         background: lightblue;
#         overflow: hidden;
#         padding-left: 10px;
#       }
#       table .client-info {
#         padding-left: 10px;
#       }
#       table .sub-total,
#       table .total {
#         text-align: right;
#         padding-right: 10px;
#       }
#       table .sub-total-value {
#         font-weight: bold;
#         text-align: center;
#       }
#       table .total {
#         font-weight: bold;
#       }
#       table .total-value {
#         background: lightblue;
#       }
#       table .separator {
#         height: 2px;
#         background: #333;
#       }
#       table .separator:last-child {
#         display: none;
#       }
#       @media print {
#       body {
#         page-break-after: always;
#       }
#       .title {
#         display: none !important;
#       }
#       .table-container {
#       max-height: none !important;
#       }
#     }
# """
#     )

  with a.body():
    with a.h1(klass="title"):
      a(f"Comandas Reverdecer {datetime.now().strftime('%d/%m/%Y')}")
    with a.div(klass="table-container"):
      with a.table():
        with a.tr():
          a.th(_t="Nombre", klass="name")
          a.th(_t="Cantidad", klass="quantity")
          a.th(_t="Producto", klass="product")
          a.th(_t="Precio", klass="value")
        for row in rows:  # Por cada cliente
          name = row[2]
          phone = row[3]
          direc = row[4]
          shipping = row[5]
          shippingPrice = re.search(r"\$([0-9]+)", shipping)
          first = second = third = fourth = True
          total = 0
          for i in range(6, len(row) - 1):  # Por cada producto
            if row[i] != "":
              if prices[i].isdigit():
                total += Fraction(row[i]) * Fraction(prices[i])
              with a.tr():
                if first:
                  a.td(_t=name, klass="client-name")
                  first = False
                elif second:
                  a.td(_t=phone, klass="client-info")
                  second = False
                elif third:
                  if direc != "":
                    a.td(_t=direc, klass="client-info", rowspan="2")
                    third = False
                  else:
                    a.td()
                    third = fourth = False
                elif fourth:
                  fourth = False
                else:
                  a.td()
                a.td(_t=row[i], klass="number")
                a.td(_t=header[i])
                if prices[i].isdigit():
                  a.td(_t=f"${Fraction(row[i])*Fraction(prices[i])}", klass="number")
                else:
                  a.td()
          else:
            if row[-1] != "":
              with a.tr():
                a.td(_t=header[-1], klass="number", colspan="2")
                a.td(_t=row[-1], colspan="2")
            with a.tr():
              a.td(_t=header[5], klass="number", colspan="2")
              a.td(_t=shipping)
              if shippingPrice:
                a.td(_t=shippingPrice.group(), klass="number")
                total += Fraction(shippingPrice.group()[1:])
              else:
                a.td()
            with a.tr():
              a.td()
              a.td()
              a.td(_t="Sub Total", klass="sub-total")
              a.td(_t=f"${total}", klass="sub-total-value")
            with a.tr():
              a.td()
              a.td()
              a.td(_t=f"Total {name}", klass="total")
              a.td(_t="", klass="total-value")
            with a.tr(klass="separator"):
              a.td()
              a.td()
              a.td()
              a.td()

html_bytes = bytes(a)

# print(html)
with open("index.html", "wb") as f:
  f.write(bytes(html_bytes))

os.system("start index.html")
