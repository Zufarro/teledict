import sqlite3
import json

from flask import Flask, request

app = Flask(__name__)

dbname = "dict.db"

def words_en_ru():
    db = sqlite3.connect(dbname)
    return db.execute("""
CREATE TABLE IF NOT EXISTS words
(
word text
)
               """)


def translation_en_ru():
    db = sqlite3.connect(dbname)
    return db.execute("""
CREATE TABLE IF NOT EXISTS translations
(
id_word number, 
translation text
)
               """)


def get_all_json():
    db = sqlite3.connect(dbname)
    cursor = db.execute("SELECT rowid, word FROM words")
    rows = []
    for tuple in cursor.fetchall():
        rows.append({tuple[0]: tuple[1]})
    return json.dumps(rows)

@app.route("/")
def hello():
    words_en_ru()
    translation_en_ru()
    return "Created new tables"


@app.route("/words", methods=['GET'])
def get_words():
    return get_all_json()


@app.route("/words", methods=["POST"])
def add_words():
    db = sqlite3.connect(dbname)
    ad = request.get_json()
    for name, value in ad.items():
        db.execute("INSERT INTO words VALUES('%s')" % (value))
    db.commit()
    return ""


@app.route("/words/<id>", methods=['DELETE'])
def delete_word(id):
    db = sqlite3.connect(dbname)
    db.execute("DELETE FROM words WHERE rowid=%s" % id)
    db.commit()
    return "ok"