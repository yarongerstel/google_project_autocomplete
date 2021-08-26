import pandas as pd
import itertools
import os

# Folder Path
path = r'2021-archive'
pool = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z')
main_lst = []
word_found = ""
word_found_bool = False


class AutoCompleteData:
    def __init__(self, cs, st, o, s):
        self.completed_sentence = cs
        self.source_text = st
        self.offset = o
        self.score = s

    completed_sentence: str
    source_text: str
    offset: int
    score: int


# Read text File
def read_text_file(file_path):
    read_file = pd.read_fwf(file_path)
    new_dir = f"fixed/{os.path.dirname(file_path)}"
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)
    counter = 1
    while (len(read_file.columns) > 1):
        read_file['line content'] = read_file['line content'] + read_file[f'Unnamed: {counter}']
        del read_file[f'Unnamed: {counter}']
        counter += 1
    read_file.to_csv(f"fixed/{file_path[:-3]}csv")


def searchIt(file_path, input):
    global word_found, word_found_bool
    df = pd.read_csv(file_path, low_memory=False)
    input = word_found
    #input to lst all sintext thet contain "input" in row line content
    lst = list(df.loc[df['line content'].str.contains(input, na=False), 'line content'])
    if len(lst) == 0 and not word_found_bool: # if don't find anything make change and serching again
        for i in full_combinations(input):
            lst = list(df.loc[df['line content'].str.contains(i[0], na=False), 'line content'])
            if len(lst) != 0:
                word_found = i[0]
                word_found_bool = True
                for item in lst: # add the find to main_lst list
                    instance = AutoCompleteData(item, file_path, 0, len(input) * 2 - int(i[1]))
                    main_lst.append(instance)
                    if len(main_lst)>5:
                        break
                    # print(item + " score: " + str(len(input) * 2 - int(i[1])) + " location: " + file_path)
                break
    elif len(lst) != 0:
        word_found_bool = True
        for item in lst: # add the find to main_lst list
            instance = AutoCompleteData(item, file_path, 0, len(input) * 2)
            main_lst.append(instance)
            if len(main_lst) > 5:
                break
            # print(item + " score: " + str(len(input) * 2) + " location: " + file_path)


def mySort(instance):
    return instance.score


def finish_search():
    main_lst.sort(key=mySort, reverse=True)
    counter = min(len(main_lst), 5) #make shore print maximum gust 5 element
    for i in range(counter):
        print(main_lst[i].completed_sentence)
        print(main_lst[i].source_text)
        print(main_lst[i].offset)
        print(main_lst[i].score)
        print('\n')
    main_lst.clear()



def superFastSearch(path, input):
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            searchIt(f, input)
        else:
            superFastSearch(f, input)


def full_combinations(statement):
    for letter in pool:  # switch
        for i in range(len(statement)):
            temp = statement[:i] + letter + statement[1 + i:]
            score_down = calculate_char(statement, temp) + 2
            yield temp, score_down
    for letter in pool:  # add char to statment
        for i in range(len(statement)):
            temp = statement[:i] + letter + statement[i:]
            score_down = calculate_char(statement, temp) * 2  # get down also for worng char
            yield temp, score_down
    for tup in itertools.combinations(statement, len(statement) - 1):  # sub
        temp = ''.join(tup)
        score_down = calculate_char(statement, temp) * 2 + 2
        yield temp, score_down


def calculate_char(original, copy):
    for i in range(len(original)):
        if i < len(original) and i < len(copy) and original[i] != copy[i]:
            if i >= 5:
                return 1
            return 5 - i
    if len(original) >= 5 and len(copy) >= 5:
        return 1
    min_num = min(len(original), len(copy))
    return 5 - min_num


def prepend_line(file_name, line):
    """ Insert given string as a new line at the beginning of a file """
    # define name of temporary dummy file
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r', encoding='utf8') as read_obj:
        temp = read_obj.readlines()
    with open(file_name, 'w', encoding='utf8') as write_obj:
        write_obj.write(line + '\n')
        for selected_line in temp:
            write_obj.write(selected_line)


def initialization(path):
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            prepend_line(f, 'line content')
            read_text_file(f)
        else:
            initialization(f)


def startup(input):
    global word_found
    #checkOver(path, input)
    word_found = input
    superFastSearch('fixed/' + path, input)


def main():
    # initialization(path)
    temp = ""
    a = input("enter statement: ")
    while (a != '#'):
        a.lower().strip()
        # agnore multy space
        while "  " in a:
            a = a.replace("  ", " ")
        temp = temp + a
        word_found = ""
        main_lst = []
        startup(temp)
        finish_search()
        a = input(temp)


if __name__ == '__main__':
    main()