
# FPDF
from fpdf import FPDF

import cups
conn = cups.Connection ()
printers = conn.getPrinters ()
for printer in printers:
    print( printers[printer].keys())

printer_name = list(printers.keys())[0]
# 4. Lancer l'impression
# Arguments : Nom de l'imprimante, Chemin du fichier, Titre du job, Options
file_path = "/home/claude/dev/pipo/WelcomeToTheMachine/images/impression_2026.png"
title = "Impression via Python"
options = {"media": "jpn_hagaki_100x148mm", "sides": "one-sided"}

job_id = conn.printFile("Canon_SELPHY_CP1300_USB", file_path, title, options)

print(f"Impression lancée avec succès. ID du job : {job_id}")
