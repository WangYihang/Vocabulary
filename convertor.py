#!/usr/bin/env python
# encoding: utf-8

import json

def main():
    words = {}
    filename = "data/cet6.txt"
    f = open(filename)
    word = None
    for line in f:
        data = line.rstrip()
        if data.startswith("\t"):
            index = data.index(".")
            speech = data[:index].strip()
            meaning = data[index+1:].strip(";").replace(" ", "").split(";")
            words[word][speech] = meaning
        else:
            word = data
            if word not in words.keys():
                words[word] = {}
    with open("%s.json" % (filename), "w") as f:
        f.write(json.dumps(words, ensure_ascii=False))

if __name__ == "__main__":
    main()