import re
from fpdf import FPDF
from fpdf.fonts import FontFace
from fractions import Fraction
from datetime import datetime


def create_pdf(rows, header, prices):
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font("Helvetica", size=14)
  pdf.set_auto_page_break(auto=True, margin=0)
  pdf.cell(
    200, 10, f"Comandas Reverdecer {datetime.now().strftime('%d/%m/%Y')}", 0, 1, "C"
  )
  pdf.set_font("Helvetica", size=8)
  cont = 0
  for row in rows:  # Por cada cliente
    cont += 1
    table_height = (len(list(filter(lambda x: x != "", row))) - 1) * 4 # calculo aproximado de la altura de la tabla
    if pdf.will_page_break(table_height):
      pdf.add_page()
    with pdf.unbreakable() as pdf:
      with pdf.table(
        col_widths=(40, 15, 95, 15),
        line_height=pdf.font_size * 1.4,
        text_align=("LEFT", "CENTER", "LEFT", "CENTER"),
        headings_style=FontFace(emphasis="BOLD", fill_color=(176, 196, 222)),
      ) as table:
        headings = table.row()
        headings.cell("Nombre")
        headings.cell("Cantidad")
        headings.cell("Producto")
        headings.cell("Precio")
        name = row[2]
        phone = row[3]
        direc = row[4]
        shipping = row[5]
        shippingPrice = re.search(r"\$([0-9]+)", shipping)
        first = True
        total = 0
        for i in range(6, len(row) - 1):  # Por cada producto
          if row[i] != "":
            if prices[i].isdigit():
              total += Fraction(row[i]) * Fraction(prices[i])
            r = table.row()
            if first:
              r.cell(f"{cont}: " + name, style=FontFace(fill_color=(173, 216, 230)))
              first = False
            else:
              r.cell("")
            r.cell(row[i])  # Cantidad
            r.cell(header[i])  # Producto
            if prices[i].isdigit():  # Precio
              r.cell(f"${Fraction(row[i])*Fraction(prices[i])}")
            else:
              r.cell("")
        else:
          r = table.row() # Envío
          r.cell(header[5], colspan=2, padding=(0, 0, 0, 2))
          r.cell(shipping)
          if shippingPrice:
            r.cell(shippingPrice.group())
            total += Fraction(shippingPrice.group()[1:])
          else:
            r.cell("")
          r = table.row()
          r.cell(phone, padding=(0, 0, 0, 2), colspan=2)
          r.cell("Sub Total", padding=(0, 0, 0, 60))
          r.cell(f"${total}", style=FontFace(emphasis="BOLD"))
          r = table.row()
          r.cell(direc, padding=(0, 0, 0, 2), colspan=2)
          r.cell(
            f"Total {name}", padding=(0, 0, 0, 60), style=FontFace(emphasis="BOLD")
          )
          r.cell("", style=FontFace(fill_color=(173, 216, 230)))
          if row[-1] != "":  # Comentario
            r = table.row()
            r.cell(header[-1], colspan=2, padding=(0, 0, 0, 2))
            r.cell(row[-1], colspan=2)
          r = table.row()
  pdf.output("comandas.pdf")
