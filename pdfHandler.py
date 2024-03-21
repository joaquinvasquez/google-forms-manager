import re
from fpdf import FPDF
from fpdf.fonts import FontFace
from fractions import Fraction
from datetime import datetime


def create_pdf(rows, header, prices):
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font("Helvetica", size=14)
  pdf.cell(
    200, 10, f"Comandas Reverdecer {datetime.now().strftime('%d/%m/%Y')}", 0, 1, "C"
  )
  pdf.set_font("Helvetica", size=8)
  for row in rows:  # Por cada cliente
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
        first = second = third = fourth = True
        total = 0
        for i in range(6, len(row) - 1):  # Por cada producto
          if row[i] != "":
            if prices[i].isdigit():
              total += Fraction(row[i]) * Fraction(prices[i])
            r = table.row()
            if first:
              r.cell(name, style=FontFace(fill_color=(173, 216, 230)))
              first = False
            elif second:
              r.cell(phone, padding=(0, 0, 0, 2))
              second = False
            elif third:
              if direc != "":
                r.cell(direc, padding=(0, 0, 0, 2), rowspan=2)
                third = False
              else:
                r.cell("")
                third = fourth = False
            elif fourth:
              fourth = False
            else:
              r.cell("")
            r.cell(row[i])  # Cantidad
            r.cell(header[i])  # Producto
            if prices[i].isdigit():  # Precio
              r.cell(f"${Fraction(row[i])*Fraction(prices[i])}")
            else:
              r.cell("")
        else:
          if row[-1] != "":  # Comentario
            r = table.row()
            r.cell(header[-1], colspan=2, padding=(0, 0, 0, 2))
            r.cell(row[-1], colspan=2)
          r = table.row()
          r.cell(header[5], colspan=2, padding=(0, 0, 0, 2))
          r.cell(shipping)
          if shippingPrice:
            r.cell(shippingPrice.group())
            total += Fraction(shippingPrice.group()[1:])
          else:
            r.cell("")
          r = table.row()
          r.cell("")
          r.cell("")
          r.cell("Sub Total", padding=(0, 0, 0, 60))
          r.cell(f"${total}", style=FontFace(emphasis="BOLD"))
          r = table.row()
          r.cell("")
          r.cell("")
          r.cell(
            f"Total {name}", padding=(0, 0, 0, 60), style=FontFace(emphasis="BOLD")
          )
          r.cell("", style=FontFace(fill_color=(173, 216, 230)))
          r = table.row()
  pdf.output("comandas.pdf")
