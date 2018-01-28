#!/usr/bin/env python2.7
import psycopg2
import urllib
from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont
from resizeimage import resizeimage
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Image, LongTable, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


def csv_to_db(csv_path):
    conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
    cur = conn.cursor()
    cur.execute("""DELETE FROM users;""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS  users(
        name text,
        surname text,
        company text,
        title text,
        dateofbirth text,
        photo text
    )
    """)

    with open(csv_path, 'r') as csv_file:
        cur.copy_from(csv_file, 'users', sep=',')
        cur.execute("""
            SELECT * FROM users ORDER BY company ASC, title ASC;
            """)

    rows = cur.fetchall()

    doc = SimpleDocTemplate("list_of_people.pdf", pagesize=A4, rightMargin=30, leftMargin=20, topMargin=30,
                            bottomMargin=18)
    pdf_elements = []
    s = getSampleStyleSheet()
    s = s["BodyText"]

    data_rows = [('NAME', 'SURNAME', 'COMPANY', 'TITLE', 'DOB', 'PHOTO'), ]
    for row in rows:
        img = urllib.urlretrieve(row[5], "pic of {} {}.jpg".format(row[0], row[1]))
        watermark = str(row[0])
        edit_image("pic of {} {}.jpg".format(row[0], row[1]), watermark)
        I = Image("pic of {} {}.jpg".format(row[0], row[1]))
        data_rows.append((row[0], row[1], Paragraph(row[2], s), Paragraph(row[3], s), row[4], I),)

    main_table_from_db = LongTable(data_rows, 5 * [1 * inch], len(data_rows) * [1 * inch], repeatRows=1,
                                   splitByRow=1)
    main_table_from_db.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    cur.execute("""SELECT company, COUNT(company) FROM users GROUP BY company""")
    table_of_people = cur.fetchall()
    people_in_company = []
    for row in table_of_people:
        people_in_company.append((Paragraph(row[0], s), row[1]),)

    people_in_company = [('COMPANY', Paragraph('NUMBER OF EMPLOYEES', s)), ] + people_in_company

    table_for_employees_amount = Table(people_in_company, 5 * [1 * inch], len(people_in_company) * [0.4 * inch])
    table_for_employees_amount.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    pdf_elements.append(main_table_from_db)
    pdf_elements.append(Spacer(1, 30))
    pdf_elements.append(table_for_employees_amount)
    doc.build(pdf_elements)

    conn.commit()


def edit_image(user_foto, watermark):
    fd_img = open(user_foto, 'r')
    img = PILImage.open(fd_img)
    img = resizeimage.resize_thumbnail(img, [50, 50])
    drawing = ImageDraw.Draw(img)
    black = (3, 8, 12)
    font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 12)
    drawing.text((2, 2), watermark, fill=black, font=font)
    img.save(user_foto, img.format)
    fd_img.close()
    return user_foto


if __name__ == '__main__':
    csv_file = raw_input("Please enter a path to csv file: ")
    csv_to_db(csv_file)





