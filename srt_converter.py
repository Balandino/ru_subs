import codecs
import csv
import glob
import os
import re


def get_word_positions(line: str) -> list[list[int]]:
    """
    Gets index positions of words within a line for verb checking.  It is done this way to target individual words
    and their locations.  The issue with taking a more simple approach is that some words are hyphen separated or
    a word could exist within another (e.g говорит and поговорить in the same sentence, or жил-бил which is two words)

    Args:
        line: Line containing potential words

    Returns:
        A list of index positions within the string for potential replacements
    """
    pattern = re.compile("[а-яА-Я]")
    boundary_characters = [" ", "-", ",", "!", ".", "?"]
    indexes = []

    word_start = 0
    start_set = False
    for i in range(0, len(line)):
        if pattern.match(line[i]) and start_set is False:
            start_set = True
            word_start = i

        if i == (len(line) - 1) and start_set:
            indexes.append([word_start, i])

        if line[i] in boundary_characters and start_set:
            indexes.append([word_start, i])
            start_set = False

    return indexes


def generate_ru_subs(file: str):
    """
    Extracts lines from the file, modifies them for verb aspect colouring and writes a new file

    Args:
        file: File name with extension
    """
    srt_file = open(file, "r", encoding="utf-8")
    lines = srt_file.readlines()

    # Check for any russian letters in the line
    pattern = re.compile(".*[а-яА-Я]+")
    new_subs = ""

    for line in lines:
        if pattern.match(line):
            line_to_add = process_line(line)
            # line_to_add = debug_process_line(line)  # Switch to here for debugging
        else:
            line_to_add = line

        new_subs += line_to_add

    srt_file.close()
    os.remove(file)
    aspects_subs = codecs.open(file, "w", encoding="utf-8")
    aspects_subs.write(new_subs.strip())
    print(f"{file} Completed!")


def get_word_variations(word: str) -> list[str]:
    """
    Gets possible variations of words for better processing.  For instance, снесет should be
    снесёт to get a match.

    Args:
        word: Original russian word

    Returns:
        List of words, including original
    """
    words = [word]

    index = word.rfind("е")
    if index > -1:
        words.append(word[:index] + "ё" + word[index + 1 :])

    return words


def process_line(line: str) -> str:
    """
    Creates a line that has been modified with coloured variables

    Args:
        line: The unmodified line

    Returns:
        The modified line
    """
    word_indexes = get_word_positions(line)
    new_line = ""

    index_pair_count = 0
    current_index = 0
    index_start = 0
    rest_of_line = ""
    while current_index < len(line):

        if index_pair_count < len(word_indexes):
            if current_index == word_indexes[index_pair_count][0]:
                new_line += line[index_start:current_index]

                index_start = word_indexes[index_pair_count][0]
                index_end = word_indexes[index_pair_count][1]
                coloured_word = get_coloured_verb(line[index_start:index_end])
                new_line += coloured_word
                rest_of_line = line[index_end:]

                current_index = word_indexes[index_pair_count][1]
                index_start = current_index

                index_pair_count += 1

                if index_pair_count > len(word_indexes) - 1:
                    new_line += rest_of_line

                continue

        current_index += 1

    return new_line


# Switch to this for debugging
def debug_process_line(line: str) -> str:
    """
    Creates a line that has been modified with coloured variables

    Args:
        line: The unmodified line

    Returns:
        The modified line
    """
    word_indexes = get_word_positions(line)
    new_line = ""

    # These are the indexes of the words that need to be checked for aspect and coloured
    print("These are the indexes of word that need checking for verb aspect:")
    for index_pair in word_indexes:
        print(index_pair)

    print()

    print("The line to be checked: ")
    print("=================== Start ===================")
    print(line)
    print("===================  End  ===================")

    """
    HOW THIS WORKS:

    The code will iterate character by character over the line.  When current_index gets to a position that is covered by a
    pair of indexes in word_indexes, it will stop and append everything covered so far into new line.  The next part of the
    line, which will be covered by a pair of indexes in index_pair, will be checked for verb aspect and then added to
    new_line.  The algorithm then continues in the same manner until another word index is reached.

    After each word is processed the rest of the line is stored in a variable.  Once there are no more words to be checked
    the rest of the line is appended.

    """

    index_pair_count = 0  # Which pair of indexes in word_indexes are we using
    current_index = 0  # Tracks current index position in line
    index_start = 0  # The substring between this and current_index will be appended if it's not a word
    rest_of_line = ""  # Holds reamining part of line, added at end to capture remaining part of line
    while current_index < len(line):

        if index_pair_count < len(word_indexes):
            if current_index == word_indexes[index_pair_count][0]:
                new_line += line[index_start:current_index]
                print("Adding to new_line (1): ", line[index_start:current_index])

                index_start = word_indexes[index_pair_count][0]
                index_end = word_indexes[index_pair_count][1]
                print("word being checked for: ", line[index_start:index_end])
                coloured_word = get_coloured_verb(line[index_start:index_end])
                new_line += coloured_word
                print("Adding to new_line (2): ", coloured_word)
                rest_of_line = line[index_end:]
                print("Rest of line now: ", rest_of_line)

                current_index = word_indexes[index_pair_count][1]
                index_start = current_index

                index_pair_count += 1

                if index_pair_count > len(word_indexes) - 1:
                    print("Adding the following rest of line")
                    new_line += rest_of_line

                continue

        current_index += 1

    print()

    print("The new line:")
    print("=================== Start ===================")
    print(new_line, end="")
    print("===================  End  ===================")

    print()
    print()
    return new_line


def get_coloured_verb(word):
    colours = {"perfective": "#ff0000", "imperfective": "#00ff00", "both": "#ffA500"}

    words = get_word_variations(word)

    for word in words:
        verb_aspect = get_verb_type(word.lower())

        if verb_aspect == "":
            continue

        return f'<font color="{colours[verb_aspect]}">{word}</font>'

    return words[0]


def get_csv_as_list(filename: str) -> list[list[str]]:
    """
    Returns the list of lists of verbs with their aspect and conjugations.

    Args:
        filename: Name of csv file

    Returns:
        List of lists of verbs to be used in get_verb_type
    """
    with open(filename, newline="", encoding="utf-16") as words_csv:
        word_lists = csv.reader(words_csv, delimiter=",")
        return list(word_lists)


def get_verb_type(word: str) -> str:
    """
    Check the list of lists of verbs from the csv for the type of verb, either perfective or imperfective

    Args:
        word: Lower case word to search for

    Returns:
        Blank string if not found, otherwise 1 of 'perfective' or 'imperfective'

    """
    for line in VERB_LIST:
        for conjugation in line:
            if conjugation == word:
                return line[0]

    return ""


VERB_LIST = get_csv_as_list("verb_aspects - Copy.csv")
WORD_CACHE = {
    "я": "",
    "вы": "",
    "ты": "",
    "мой": "",
    "подсыпаю": "both",
    "подсыпаешь": "both",
    "подсыпает": "both",
    "подсыпаем": "both",
    "подсыпаете": "both",
    "подсыпают": "both",
    "подсыпал": "both",
    "подсыпала": "both",
    "подсыпали": "both",
    "подсыпать": "both",
    "буду": "imperfective",
    "день": "",
    "какая": "",
}

for file in glob.glob("subs\\*.srt"):
    generate_ru_subs(file)

