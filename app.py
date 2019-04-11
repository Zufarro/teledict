import sqlite3
import json

from flask import Flask, request, send_file

app = Flask(__name__)

dbname = "dict.db"

@app.route("/")
def main():
    return send_file('templates/index.html')


@app.route("/create/<lang>/<transl>", methods=['POST'])
def create_table(lang, transl):
    db = sqlite3.connect(dbname)
    db.execute("""
    CREATE TABLE IF NOT EXISTS words_%s
    (
    word text PRIMARY KEY 
    )
""" % (lang,))
    db.execute("""CREATE TABLE IF NOT EXISTS translations_%s_%s
    (
    word text PRIMARY KEY, 
    translation text
    )
""" % (lang, transl))
    db.close()
    return "Created new tables"


@app.route("/words/<lang>", methods=['GET'])
def get_all_words(lang):
    db = sqlite3.connect(dbname)
    cursor = db.execute("SELECT rowid, word FROM words_%s" % (lang,))
    rows = []
    for item in cursor.fetchall():
        id, word = item
        rows.append({"id":id, "word":word})
    db.close()
    return json.dumps(rows)


@app.route("/words/<lang>", methods=["POST"])
def add_word(lang):
    db = sqlite3.connect(dbname)
    item = request.get_json()
    if item["word"]:
        db.execute("INSERT OR IGNORE INTO words_%s VALUES('%s')" % (lang, item["word"]))
        db.commit()
        result = "success"
    else:
        result = "Error: missing word"
    db.close()
    return result


@app.route("/words/<lang>/<id>", methods=['DELETE'])
def delete_word(lang, id):
    db = sqlite3.connect(dbname)
    db.execute("DELETE FROM words_%s WHERE rowid=%s" % (lang, id))
    db.commit()
    db.close()
    return "success"


@app.route("/translation/<lang>/<transl>", methods=["POST"])
def add_translation(lang, transl):
    db = sqlite3.connect(dbname)
    item = request.get_json()
    if item["word"] and item["translation"]:
        db.execute("INSERT OR IGNORE INTO translations_%s_%s VALUES('%s', '%s')" % (lang, transl, item["word"], item["translation"]))
        db.execute("DELETE FROM words_%s WHERE word='%s'" % (lang, item["word"]))
        db.commit()
        result = "success"
    else:
        result = "Error: missing word or translation"
    db.close()
    return result


@app.route("/translate/<lang>/<transl>", methods=["POST"])
def get_translate(lang, transl):
    db = sqlite3.connect(dbname)
    item = request.get_json()
    cursor = db.execute("SELECT translation FROM translations_%s_%s WHERE word='%s'" % (lang, transl, item["word"]))
    translate = cursor.fetchone()[0]
    db.close()
    return translate


@app.route("/translation/<lang>/<transl>", methods=['GET'])  #
def get_all_translation(lang, transl):
    db = sqlite3.connect(dbname)
    cursor = db.execute("SELECT rowid, word,translation FROM translations_%s_%s" % (lang, transl))
    rows = []
    for item in cursor.fetchall():
        id, word, translation = item
        rows.append({"id": id, "word": word, "translation":translation})
    db.close()
    return json.dumps(rows)

