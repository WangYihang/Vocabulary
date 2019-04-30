#!/usr/bin/env python
# encoding: utf-8

import json

class Vocabulary:
    def __init__(self, filename):
        self.data = json.load(open(filename))

    def translate(self, target):
        result = {}
        for word, meanings in self.data.items():
            for _, v in meanings.items():
                for i in v:
                    if target in i.encode("utf-8"):
                        result[word] = meanings
        return result

    def synonym(self, target):
        meanings = self.data[target]
        result = []
        bucket = []
        words = ["的", "得", "地"]
        for speech, meaning in meanings.items():
            bucket += meaning
        for i in bucket:
            key = i.encode("utf-8")
            for word in words:
                key = key.replace(word, "")
            result += list(self.translate(key).items())
        return dict(result)



def visualize(data):
    for word, meanings in data.items():
        print(word)
        for speech, meaning in meanings.items():
            print("\t%s => %s" % (speech, ";".join(meaning)))

def loop(vocabulary):
    while True:
        data = raw_input("> ").strip()
        if data == "exit":
            break
        visualize(vocabulary.synonym(data))


def main():
    filename = "data/gee.txt.json"
    v = Vocabulary(filename)
    loop(v)

if __name__ == "__main__":
    main()