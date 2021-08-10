import pandas as pd
import itertools
import os

# Folder Path
path = r'2021-archive'
pool = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z')
main_lst = []

class AutoCompleteData:
    def __init__(self, cs, st, o,s):
        self.completed_sentence = cs
        self.source_text = st
        self.offset = o
        self.score = s

    completed_sentence: str
    source_text: str
    offset: int
    score: int



# Read text File
def read_text_file(file_path, input):
    read_file = pd.read_fwf(file_path)
    new_dir = f"fixed/{os.path.dirname(file_path)}"
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)
    read_file.to_csv(f"fixed/{file_path[:-3]}csv")


def searchIt(file_path, input):
    df = pd.read_csv(file_path,low_memory=False)
    lst = list(df.loc[df['line'].str.contains(input, na=False), 'line'])
    if len(lst) == 0:
        for i in full_combinations(input):
            lst = list(df.loc[df['line'].str.contains(i[0], na=False), 'line'])
            if len(lst) != 0:
                for item in lst:
                    instance = AutoCompleteData(item,file_path,0, len(input) * 2 - int(i[1]) )
                    main_lst.appeand(instance)
                    #print(item + " score: " + str(len(input) * 2 - int(i[1])) + " location: " + file_path)
                break
    else:
        for item in lst:
            instance = AutoCompleteData(item, file_path, 0, len(input) * 2)
            main_lst.append(instance)
            #print(item + " score: " + str(len(input) * 2) + " location: " + file_path)

def mySort(instance):
    return instance.score

def finish_search():
    main_lst.sort(key=mySort)
    for item in main_lst:
        print(item.completed_sentence)
        print(item.source_text)
        print(item.offset)
        print(item.score)
        print('\n')

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
            temp = statement[:i] + letter + statement[1+i:]
            score_down = calculate_char(statement, temp) + 2
            yield temp, score_down
    for letter in pool:  # add
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


def checkOver(path, input):
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            prepend_line(f, 'line content')
            read_text_file(f, input)
        else:
            checkOver(f, input)


def startup(input):
    #checkOver(path, input)
    superFastSearch('fixed/'+path, input)


def main():
    a = input("enter statement: ")
    startup(a)
    finish_search()
    """temp=""
    a = input("enter statement: ")
    while(a!='#'):
        a.lower().strip()
        #agnore multy space
        while "  " in a:
            a=a.replace("  "," ")
        temp = temp + a
        startup(temp)
        a = input(temp)"""

if __name__ == '__main__':
    main()
