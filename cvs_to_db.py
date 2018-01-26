import psycopg2
import urllib
from PIL import Image, ImageDraw, ImageFont
from resizeimage import resizeimage
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4


def cvs_to_db(csv_path):
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
    for row in rows:
        img = urllib.urlretrieve(row[5], "pic of {} {}.jpg".format(row[0], row[1]))
        watermark = str(row[0])
        print (row[2] + "-" + row[3])
        edit_image("pic of {} {}.jpg".format(row[0], row[1]), watermark)

    doc = SimpleDocTemplate("list_of_people.pdf", pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    Story = []

    rows = [('NAME', 'SURNAME', 'COMPANY', 'TITLE', 'DOB', 'PHOTO'), ] + rows

    t = Table(rows, 5 * [1 * inch], len(rows) * [0.4 * inch])
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    Story.append(t)
    doc.build(Story)

    conn.commit()


def edit_image(user_foto, watermark):
    fd_img = open(user_foto, 'r')
    img = Image.open(fd_img)
    img = resizeimage.resize_thumbnail(img, [300, 300])
    drawing = ImageDraw.Draw(img)
    black = (3, 8, 12)
    font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 15)
    drawing.text((2, 6), watermark, fill=black, font=font)
    img.save(user_foto, img.format)
    fd_img.close()


if __name__ == '__main__':
    csv_file = raw_input("Please enter a path to csv file: ")
    cvs_to_db(csv_file)





