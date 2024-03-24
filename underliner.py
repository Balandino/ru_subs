import codecs
import glob

for file in glob.glob("*.srt"):
    with open(file, newline="", encoding="utf-8") as subs:
        new_name = file[:-4] + "_underlined.srt"
        new_subs = ""
        for row in subs:
            line = row.strip()

            if len(line) == 0:
                new_subs += "------------------------------\n"
                new_subs += line + "\n"
            else:
                new_subs += line + "\n"

    underlined = codecs.open(new_name, "w", encoding="utf-8")
    underlined.write(new_subs.strip())

