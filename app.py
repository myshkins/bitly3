import json
import csv
import sqlite3
from timer import Timer

ENCODES_FILE_PATH = "encodes.csv"
DECODES_FILE_PATH = "decodes.json"


conn = sqlite3.connect("bitly.db")
cur = conn.cursor()


def create_decode_table():
    cur.execute("DROP TABLE IF EXISTS decodes")
    cur.execute(
        """
        CREATE TABLE decodes(
            bitlink TEXT,
            user_agent TEXT,
            timestamp TIMESTAMP,
            referrer TEXT,
            remote_ip TEXT
            )
        """
    )


def insert_decode_data():
    with open("decodes.json") as file:
        data = json.load(file)
    for row in data:
        bitlink = row["bitlink"]
        user_agent = row["user_agent"]
        timestamp = row["timestamp"][:-1]
        referrer = row["referrer"]
        remote_ip = row["remote_ip"]
        conn.execute(
            "INSERT INTO decodes VALUES (?, ?, ?, ?, ?)",
            (bitlink, user_agent, timestamp, referrer, remote_ip),
        )
    conn.commit()


def create_encode_table():
    cur.execute("DROP TABLE IF EXISTS encodes")
    cur.execute(
        """
        CREATE TABLE encodes(
            long_url TEXT,
            domain TEXT,
            hash TEXT,
            bitlink TEXT
        )
        """
    )


def insert_encode_data():
    with open("encodes.csv", mode="r+") as file:
        data = csv.reader(file)
        values = []
        for row in data:
            if row[0] == 'long_url':
                row.append('bitlink')
            else:
                bitlink = f"http://{row[1]}/{row[2]}"
                row.append(bitlink)
            values.append(row)
        cur.executemany(
            """
        insert into encodes (long_url, domain, hash, bitlink)
        values (?, ?, ?, ?)""",
            values,
        )


def count_clicks(year):
    res = cur.execute(
        """
        select long_url, count(*)
        from decodes join encodes on decodes.bitlink = encodes.bitlink
        where strftime('%Y', timestamp) = ?
        group by long_url
        order by count(*)
        """, year
    )
    return [{k: v} for k, v in res]

timer = Timer()
timer.start()
create_decode_table()
insert_decode_data()
create_encode_table()
insert_encode_data()
result = count_clicks(('2021',))
timer.stop()
print(result)
