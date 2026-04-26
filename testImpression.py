
# FPDF
from fpdf import FPDF


pdf = FPDF(orientation="L", unit="mm", format="A4")
pdf.add_page()
#pdf.add_font("BTTF","","./font/BTTF.ttf")
pdf.set_font('Arial', size=48)

pdf.image("images/photo1.png", x=118, y=140)

pdf.image("images/masquePhoto.png", x=0, y=0)
with pdf.rotation(angle=-10, x=20, y=30):
    pdf.text(265,30,"1965")

pdf.output("./temp/test.pdf")
print("lancement de l'impression")
