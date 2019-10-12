import polls.logic as logic
from fpdf import FPDF


def simple_table(spacing=1):

    data = logic.get_all_Futures()

    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()
    a = ['date', 'time', 'datetime', 'datetime.date', 'datetime.time', 'datetime.datetime']
    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    for row in data:
        for i, item in enumerate(row):
            print(item)
            if i == 2:
                print(item)
                print(type(item))
                print(a)
                for g in a:
                    print(type(item) is g)
                item = item.strftime("%d/%m/%Y")
            pdf.cell(col_width, row_height * spacing,
                     txt=item, border=1)
        pdf.ln(row_height * spacing)

    pdf.output('simple_table.pdf')