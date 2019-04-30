#!/usr/bin/env python
# encoding: utf-8

import json
import colorama
import readline

class Vocabulary:
    def __init__(self, filename):
        self.data = json.load(open(filename))
        self.speech_color = {
            "vt": colorama.Fore.GREEN,
            "vi": colorama.Fore.GREEN,
            "v": colorama.Fore.GREEN,
            "conj": colorama.Fore.MAGENTA,
            "prep": colorama.Fore.YELLOW,
            "n": colorama.Fore.CYAN,
            "adj": colorama.Fore.BLUE,
            "adv": colorama.Fore.WHITE,
        }

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
        for _, meaning in meanings.items():
            bucket += meaning
        for i in bucket:
            key = i.encode("utf-8")
            for word in words:
                key = key.replace(word, "")
            colored = "%s%s%s" % (colorama.Fore.GREEN, key.decode("utf-8"), colorama.Style.RESET_ALL)
            # Mark color
            colored_translated = {}
            for tword, tmeanings in self.translate(key).items():
                rmeaning = {}
                for speech, meaning in tmeanings.items():
                    rmeaning[speech] = [j.replace(key.decode("utf-8"), colored) for j in meaning]
                colored_translated[tword] = rmeaning
            result += list(colored_translated.items())
        return dict(result)


    def get_words(self):
        return self.data.keys()

    def visualize(self, data):
        for word, meanings in data.items():
            print(word)
            for speech, meaning in meanings.items():
                print("\t%s\t%s" % ("%s%s%s" % (self.speech_color[speech], speech, colorama.Style.RESET_ALL), ";".join(meaning)))

def loop(vocabulary):
    while True:
        data = raw_input("> ").strip()
        if data == "exit":
            break
        if data not in vocabulary.get_words():
            print("No such word")
            continue
        vocabulary.visualize({data:vocabulary.data[data]})
        symonyms = vocabulary.synonym(data)
        if len(symonyms) != 1:
            print("-" * 0x20)
            vocabulary.visualize(symonyms)

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