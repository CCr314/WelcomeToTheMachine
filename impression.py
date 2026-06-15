import cups
conn = cups.Connection ()

def impression(file_path):
    #printer_name = list(printers.keys())[0]
    #file_path = "./images/impression_2026.png"
    title = "Welcome to the machine"
    options = {"media": "jpn_hagaki_100x148mm", "sides": "one-sided"}

    job_id = conn.printFile("Canon_SELPHY_CP1300_USB", file_path, title, options)

    print(f"Impression lancée avec succès. ID du job : {job_id}")
