english = open("output_en.srt", "r", newline="", encoding="utf-8")
en_lines_pre = english.readlines()

russian = open("output.srt", "r", newline="", encoding="utf-8")
ru_lines = russian.readlines()

en_lines = []

for line in en_lines_pre:
    if len(line.strip()) > 0:
        en_lines.append(line[line.find(" ") + 1 :])


combined_lines = []
count = 0
for line in ru_lines:
    if len(line.strip()) == 0:
        combined_lines.append("-------------------\r\n" + en_lines[count])
        count = count + 1

    combined_lines.append(line)


# writing to file
output_file = open("combined.srt", "w", encoding="utf-8")
output_file.writelines(combined_lines)
output_file.close()

