#!/usr/bin/env python
# encoding: utf-8

import json
import colorama
import readline

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
        if target in self.data.keys():
            meanings = self.data[target]
            result = []
            bucket = []
            words = ["的", "得", "地"]
            for _, meaning in meanings.items():
                bucket += meaning
            for i in bucket:
                colored = "%s%s%s" % (colorama.Fore.RED, i, colorama.Style.RESET_ALL)
                key = i.encode("utf-8")
                for word in words:
                    key = key.replace(word, "")
                # Mark color
                colored_translated = {}
                for tword, tmeanings in self.translate(key).items():
                    rmeaning = {}
                    for speech, meaning in tmeanings.items():
                        rmeaning[speech] = [j.replace(i, colored) for j in meaning]
                    colored_translated[tword] = rmeaning
                result += list(colored_translated.items())
            return dict(result)
        else:
            print("No such word")
            return {}

    def get_words(self):
        return self.data.keys()


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
        visualize(vocabulary.translate(data))
        visualize(vocabulary.synonym(data))

commands = []

def completer(text, state):
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

def main():
    global commands
    colorama.init()
    filename = "data/gee.txt.json"
    v = Vocabulary(filename)
    commands = v.get_words()
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    loop(v)

if __name__ == "__main__":
    main()