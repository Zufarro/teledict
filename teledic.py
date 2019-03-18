import sqlite3

class Teledict():
    def __init__(self,name):
        db = sqlite3.connect(str(name)+".db")
        db.execute("""
CREATE TABLE IF NOT EXISTS words
(
id number PRIMARY KEY,
word text
)
               """)

        db.execute("""
CREATE TABLE IF NOT EXISTS translations
(
id number PRIMARY KEY,
id_word number, 
translation text
)
               """)

        self.db = db
        self.last_word_id = 0
        self.last_translation_id = 0

    def add_word(self,word):
        self.last_word_id += 1
        self.db.execute("INSERT INTO words VALUES(%s, '%s')" % (self.last_word_id,word))

    def remove_word(self,id_word):
        self.db.execute("DELETE FROM words WHERE id=%s"  % id_word)

    def add_translation(self,id_word,translation):
        self.last_translation_id += 1
        self.db.execute("INSERT INTO translations VALUES(%s, %s,'%s')" % (self.last_translation_id,id_word,translation))

    def get_translation(self, id_translation):
        self.db.execute("DELETE FROM translations WHERE id=%s"  % id_translation)

