#!/usr/bin/env python
# encoding: utf-8

def pretreat(filename):
    data = open(filename).read()
    data = data.replace("…", "...")
    data = data.replace("，", ",")
    data = data.replace("；", ";")
    data = data.replace("【", "[")
    data = data.replace("】", "]")
    data = data.replace("（", "(")
    data = data.replace("）", ")")
    data = data.replace("\t", " ")
    data = data.replace(":", ".")
    data = data.replace("  ", " ")
    data = data.replace("  ", " ")
    data = data.replace("  ", " ")
    data = data.replace("  ", " ")
    data = data.replace("  ", " ")
    with open(filename, "w") as f:
        f.write(data)

def custom_format(filename):
    data = open(filename).read()
    speeches = ["v.", "vi.", "vt.", "adj.", "adv.", "prep.", "conj.", "n."]
    f = open(filename, "w")
    for line in data.split("\n"):
        d = line.strip()
        is_meaning = False
        for speech in speeches:
            if d.startswith(speech):
                is_meaning = True
        if is_meaning:
            f.write("\t")
            f.write(d.replace(" ", ""))
            f.write("\n")
        else:
            for speech in speeches:
                d = d.replace(speech, "\n\t%s" % (speech)).replace(" ", "")
            f.write(d)
            f.write("\n")
    f.close()

def main():
    filename = "data/gee.txt"
    custom_format(filename)

if __name__ == "__main__":
    main()
