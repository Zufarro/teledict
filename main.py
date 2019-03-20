from teledic import Teledict

MyDict1 = Teledict("mydict1")

MyDict1.add_word("ручка")
MyDict1.add_word("яблоко")
MyDict1.add_word("ананас")


words = MyDict1.db.execute("SELECT * FROM words")
print(words.fetchall())

MyDict1.add_translation(1,"pen")
MyDict1.add_translation(2,"apple")
MyDict1.add_translation(3,"pineapple")

translations = MyDict1.db.execute("SELECT * FROM translations")
print(translations.fetchall())

print(MyDict1.get_translation("яблоко"))