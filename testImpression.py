
# FPDF
from fpdf import FPDF


pdf = FPDF(orientation="P", unit="mm", format=(150,100))
pdf.add_page()
##pdf.add_font("BTTF","","./font/BTTF.ttf")
pdf.add_font("ARIAL_TTF","","./font/arial.ttf")
pdf.set_font('ARIAL_TTF',"",14)

pdf.image("images/photo1.png", x=30, y=35, w=111, h=56)

pdf.image("images/masquePhoto.png", x=0, y=0, w=150, h=100)
with pdf.rotation(angle=-11, x=0, y=0):
    pdf.text(80,0.4,"1965")

pdf.output("./temp/test.pdf")
print("lancement de l'impression")
