from PIL import Image

background = Image.open('./images/fond.jpg').convert('RGBA')
masque = Image.open('./images/masquePhoto.png').convert('RGBA')
annee = Image.open('./images/1965.png').convert('RGBA')
photo = Image.open('./images/photo_1965.jpg')

background.paste(photo,(362,441))
background.alpha_composite(masque)
background.alpha_composite(annee,(850,120))
background.save("./temp/impr.png")
