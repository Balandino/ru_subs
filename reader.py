import codecs
import csv
import sys


def run():
    verb_lists = get_verb_lists()[1:]
    inifinitives_csv = get_csv_as_list("russian3 - words.csv")
    conjucations_csv = get_csv_as_list("russian3 - words_forms.csv")

    num_verbs = len(verb_lists)
    count = 0

    for sub_list in verb_lists:
        word_id = int(sub_list[0])

        for row in inifinitives_csv:
            if "id" in row[0].strip():
                continue

            if int(row[0]) == word_id:
                sub_list.append(row[2])
                break

        conjugations_found = False

        for row in conjucations_csv:
            if row[1] == "word_id":
                continue

            if int(row[1]) == word_id:
                sub_list.append(row[5])
                conjugations_found = True

                # Once gone past set of conjugations, break
                if conjugations_found == True and int(row[1]) != word_id:
                    break

        count += 1

        # sys.stdout.write(f"Processed {count} of {num_verbs}, word_id: {word_id}\n")
        sys.stdout.write(f"Processed {count} of {num_verbs}, word_id: {word_id}\r")
        sys.stdout.flush()

    aspects_csv = codecs.open("verb_aspects.csv", "w", encoding="utf-16")
    count = 0

    for sub_list in verb_lists:
        new_list = sub_list
        new_list.pop(0)
        aspects_csv.write(",".join(new_list))
        aspects_csv.write("\n")
        count = count + 1
        sys.stdout.write(f"Written {count} of {num_verbs}  \r")
        sys.stdout.flush()


def get_conjugations(word_id):
    conjugations = []
    with open("russian3 - words_forms.csv", newline="", encoding="utf-8") as words_csv:
        words_csv = csv.reader(words_csv, delimiter=",")
        for row in words_csv:
            if row[1] == word_id:
                conjugations.append(row[5])

    return conjugations


def get_csv_as_list(filename):
    with open(filename, newline="", encoding="utf-8") as words_csv:
        words_csv = csv.reader(words_csv, delimiter=",")
        return list(words_csv)


def get_verb_lists():
    """
    Gets the list of word ids for every verb.

    Returns:
        List of lists, with each sublist containing word id and imperfective or perfective text
        e.g ['58658', 'imperfective'], ['58661', 'imperfective'],
    """
    ids = []

    LIMIT = 0  # Set to value over 0 to impose limit
    count = 0

    with open(
        "russian3 - verbs.csv", newline="", encoding="utf-8"
    ) as verbs_infinitives_csv:
        verb_infinitive_row_reader = csv.reader(verbs_infinitives_csv, delimiter=",")
        for row in verb_infinitive_row_reader:
            ids.append([row[0], row[1]])

            count = count + 1
            if LIMIT > 0 and count == LIMIT:
                break

    return ids


run()

