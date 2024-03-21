from airium import Airium
from fractions import Fraction
from datetime import datetime


def create_html_products(rows, header, cants):
  for row in rows:  # Por cada cliente
    for i in range(6, len(row) - 1):  # Por cada producto
      if row[i] != "":
        cants[i] += Fraction(row[i])

  a = Airium()
  a("<!DOCTYPE html>")
  with a.html(lang="es"):
    with a.head():
      a.meta(charset="UTF-8")
      a.meta(name="viewport", content="width=device-width, initial-scale=1")
      a.title(_t="Productos Vendidos")
      a.link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
      )
      a.style(
        _t="""
              *,
              *::before,
              *::after {
                box-sizing: border-box;
              }
              *::-webkit-scrollbar {
                width: 12px;
              }
              *::-webkit-scrollbar-track {
                background: #f0f0f0;
                border: 2px solid transparent;
                scrollbar-gutter: stable;
              }
              *::-webkit-scrollbar-thumb {
                border-radius: 20px;
                border: 2px solid transparent;
                box-shadow: inset 0 0 10px 10px #aaa;
              }
              html {
                background: #f0f0f0;
              }
              body {
                font-family: 'Lato', sans-serif;
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100dvh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
              }
              .title {
                margin-top: 0;
                color: #333;
              }
              body .table-container {
                background: #fff;
                max-height: 80vh;
                width: max(60%, 1000px);
                overflow-y: auto;
              }
              table {
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed;
                border: 2px solid #333;
              }
              table th {
                background-color: thistle;
                border: 2px solid #333;
                padding: 10px 0;
              }
              table td {
                border: 1px solid #333;
              }
              table .quantity {
                width: 100px;
              }
              table .number {
                text-align: center;
              }
              table .total {
                font-weight: bold;
                border-top: 2px solid #333;
              }
              table .total-value {
                text-align: center;
                font-weight: bold;
                border-top: 2px solid #333;
                background-color: plum;
              }
  """
      )

    with a.body():
      with a.h1(klass="title"):
        a(f"Productos Vendidos {datetime.now().strftime('%d/%m/%Y')}")
      with a.div(klass="table-container"):
        with a.table():
          with a.tr():
            a.th(_t="Producto")
            a.th(_t="Cantidad", klass="quantity")
          for i in range(len(cants) - 1):  # Por cada producto
            if cants[i] > 0:
              with a.tr():
                a.td(_t=header[i])
                a.td(_t=float(cants[i]), klass="number")
          a.td(_t="TOTAL", klass="total")
          a.td(_t=sum(cants), klass="total-value")

  html_bytes = bytes(a)

  # print(html)
  with open("productos.html", "wb") as f:
    f.write(bytes(html_bytes))
