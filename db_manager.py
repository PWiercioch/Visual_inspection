import psycopg2
import pandas as pd
from confidentials import *
import matplotlib.pyplot as plt


class DB_manager:
    def __init__(self):
        self.conn = psycopg2.connect(host=HOST, database=DB, user=USER, password=PASSWORD)
        self.cur = conn.cursor()

    def send_data(self, error_flag=False, img_flag=False):
        pass

    def close(self):
        self.curr.close()
        self.conn.close()


img = open(r'pictures/regular_shapes/black_1.jpg', 'rb')
data = img.read()

conn = psycopg2.connect(host=HOST, database=DB, user=USER, password=PASSWORD)

cur = conn.cursor()

# cur.execute(f"insert into test values (5, 'picture', 99, E'{data.hex()}')")
cur.execute("select encode(picture, 'escape') from test where id = 5")
# cur.execute("SELECT lo_export(test.picture, 'D:\_moje\AGH\semestr 9\ISP\Projekt\Visual_inspection/pictures/regular_shapes/black_1_export.jpg') FROM test  -- need superuser permission.WHERE name = 'picture';")

rows = cur.fetchall()

for r in rows:
    print(r)

conn.commit()
cur.close()

conn.close()

import_bytes = r[0]
str_bytes = data.hex()

print(str_bytes) == import_bytes

with open('image.jpg', 'wb') as file:
    file.write(bytes.fromhex(import_bytes))