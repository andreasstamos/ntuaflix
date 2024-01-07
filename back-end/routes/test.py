import codecs

with open("a.txt", "rb") as f:
    f1 = codecs.getreader("utf-8")(f)
    print(f1.read(1))
