#!/usr/bin/env python
import re

WORDLIST = "wortliste/wortliste.txt"
INPUT = "scrambled.txt"

ADDITIONAL_WORDS = [
    "Stiko",
    "Astrazeneca",
    "mRNA-Impfstoff",
    "Biontech",
    "Moderna",
    "Berson",
    "Impfzentrum",
    "Viersen-Dülken",
    "Impfzentrums",
    "Astrazeneca-Sonderkontingent",
    "Astra-Impfung",
    "Astrazeneca-Impfung",
    "Biontech-Impfung",
    "Hausarztpraxen",
    "Vektor-basierte",
    "mRNA-Impfstoffe",
    "Impfstoffdosen",
    "Mischimpfung",
    "Impfintervalle",
    "Telefonnummmer", # typo in article
    "116117",
    "Dülkener",
    "Diesbezüglich",
    "heterologe",
    "Zugelassen",
    "Behandlungsbedürftigkeit",
    "intensivpflichtigen",
    "Delta-Variante",
    "mRNA-basierten",
    "Impferfolg",
    "kinderärztlichen"
]

UNLIKELY_WORDS = {
    "dun",
    "red",
    "ni",
    "na",
    "ned",
    "tags",
    "bare",
    "dei",
    "Dei",
    "sine",
    "isch",
    "se",
    "mi",
    "ma",
    "From",
    "Wei"
}

START_CHARS = ["(", "„"]
END_CHARS = ["“", ")", ",", ";", ":", ".", "?", "!"]
ONLY_LETTERS = re.compile(r"^[a-zA-Z0-9äöüÄÖÜß\-]+$")

def parseWordlist(wordlist, word_dict=dict()):
    for word in wordlist:
        if word in UNLIKELY_WORDS:
            continue
        sorted_word = "".join(sorted(word))
        if sorted_word not in word_dict:
            word_dict[sorted_word] = [word]
        else:
            word_dict[sorted_word].append(word)
    return word_dict

def addWordlist(word):
    global word_dict
    sorted_word = "".join(sorted(word))
    if sorted_word not in word_dict:
        word_dict[sorted_word] = [word]
    else:
        word_dict[sorted_word].append(word)

def prepare():
    global word_dict
    word_dict = parseWordlist([line.rstrip() for line in open(WORDLIST)] + ADDITIONAL_WORDS)

def unscrambleFile(filename="scrambled.txt"):
    file = open(filename)
    output = ""
    for line in file:
        outline = []
        for word in line.split():
            out_start = out_middle = out_end = ""
            for char in START_CHARS:
                out_start += char * word.count(char)
                word = word.replace(char, "")
            for char in END_CHARS:
                out_end += char * word.count(char)
                word = word.replace(char, "")
            if not ONLY_LETTERS.match(word):
                print(f"- Additional character found in word \"{word}\"")
            sorted_word = "".join(sorted(word))
            sorted_word_lower = "".join(sorted(word.lower()))
            found = None
            if sorted_word in word_dict:
                found = word_dict[sorted_word]
                firstupper = False
            elif sorted_word_lower in word_dict:
                found = word_dict[sorted_word]
                firstupper = True

            if found:
                entries = word_dict[sorted_word]
                if len(entries) == 1:
                    out_middle = entries[0]
                else:
                    select = ", ".join(f"{i}: {v}" for i, v in enumerate(entries))
                    choice = -1
                    while choice >= len(entries) or choice < 0:
                        try:
                            choice = int(input(f"Choose which matches best [{select}]:"))
                        except ValueError:
                            print("only enter number!")
                    out_middle = entries[choice]
                if firstupper:
                    out_middle = out_middle[0].upper() + out_middle[1:]
            else:
                out_middle = input(f"missing word, type what you think \"{word}\" means:")
                if not out_middle:
                    out_middle = word
                else:
                    addWordlist(out_middle)
            outline.append(out_start + out_middle + out_end)
            print(out_middle)
        output += " ".join(outline) + "\n"
    print("- done. Text:\n")
    print(output)

if __name__ == "__main__":
    prepare()
    unscrambleFile()