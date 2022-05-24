import io
import base64
from PIL import Image
from urllib.request import urlopen

from database_utils import *

def save_image(image_url, type):
    if 'https://www.' not in image_url:
            image_url = 'https://www.' + image_url
    image_byt = urlopen(image_url).read()
    img_b64 = base64.encodebytes(image_byt)
    buffer = io.BytesIO()
    imgdata = base64.b64decode(img_b64)
    img = Image.open(io.BytesIO(imgdata))
    if type == 0:
        new_img = img.resize((40, 40))  # x, y
    else:
        new_img = img.resize((30, 30))  # x, 
    new_img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue())
    file_name = 'images/' + image_url.replace('/', '_').replace('.', '_').replace(':', '_') + '.png'
    with open(file_name, "w") as image_file:
        image_file.write(img_b64)
        image_file.close

def save_all_images(db, sport):
    if db:
        cursor = db.cursor()
        ligues_id = database_fetchall(cursor, "SELECT ID FROM %s.ligues" % (sport))
        logo_url = database_fetchall(cursor, "SELECT LIGUE_LOGO FROM %s.ligues" % (sport))
        for i in range(0, len(ligues_id)):
            save_image(logo_url[i], 0)
            teams_id = database_fetchall(cursor, "SELECT ID FROM %s.teams WHERE LIGUE_ID = %d" % (sport.get(), ligues_id[i] ))
            team_logo = database_fetchall(cursor, "SELECT TEAM_LOGO FROM %s.teams WHERE LIGUE_ID = %d" % (ligues_id[i]))
            for j in range(0, len(teams_id)):
                save_image(team_logo[j], 1)

s_db = Db()
db = connect_to_database(s_db)
save_all_images(db, 'football')