import sqlite3
import json

from flask import Flask, request, send_file

app = Flask(__name__)

dbname = "dict.db"

@app.route("/")
def main():
    return send_file('templates/index.html')


@app.route("/create")
def set():
    db = sqlite3.connect(dbname)
    db.execute("""
    CREATE TABLE IF NOT EXISTS words_en_ru
    (
    word text PRIMARY KEY 
    )
                   """)
    db.execute("""CREATE TABLE IF NOT EXISTS translations_en_ru
    (
    word text, 
    translation text
    )
                   """)
    return "Created new tables"


@app.route("/words", methods=['GET'])
def get_all_json():
    db = sqlite3.connect(dbname)
    cursor = db.execute("SELECT rowid, word FROM words_en_ru")
    rows = []
    for tuple in cursor.fetchall():
        rows.append({tuple[0]: tuple[1]})
    return json.dumps(rows)

@app.route("/words", methods=["POST"])
def add_word():
    db = sqlite3.connect(dbname)
    ad = request.get_json()
    for name, value in ad.items():
        db.execute("INSERT INTO words_en_ru VALUES('%s')" % (value))
    db.commit()
    return "ok"


@app.route("/words/<id>", methods=['DELETE'])
def delete_word(id):
    db = sqlite3.connect(dbname)
    db.execute("DELETE FROM words_en_ru WHERE rowid=%s" % id)
    db.commit()
    return "ok"


@app.route("/translate", methods=["POST"])
def get_translatе():
    db = sqlite3.connect(dbname)
    ad = request.get_json()
    for k,v in ad.items():
        if k == "word":
            word = v
        if k == "language":
            language = v
    if language == "en_ru":
        cursor = db.execute("SELECT translation FROM translations_en_ru WHERE word='%s'" % word)
        translaion = [f[0] for f in cursor.fetchall()][0]
    return translaion


@app.route("/translation", methods=["POST"])
def add_translation():
    db = sqlite3.connect(dbname)
    ad = request.get_json()
    for k,v in ad.items():
        if k == "word_of_added_translation":
            word = v
        if k == "translation_to_add":
            translation = v
        if k == "language":
            language = v
    if language == "en_ru":
        db.execute("INSERT INTO translations_en_ru VALUES('%s', '%s')" % (word, translation))
    db.commit()
    return "ok"