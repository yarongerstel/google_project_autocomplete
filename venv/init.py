import pandas as pd
import itertools
import os

# Folder Path
path = r'test'
pool = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z')


# Read text File
def read_text_file(file_path, input):
    read_file = pd.read_fwf(file_path)
    new_dir = f"fixed/{os.path.dirname(file_path)}"
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)
    read_file.to_csv(f"fixed/{file_path[:-3]}csv")
    df = pd.read_csv(f"fixed/{file_path[:-3]}csv")
    lst = list(df.loc[df['line content'].str.contains(input, na=False), 'line content'])
    if len(lst) == 0:
        for i in full_combinations(input):
            lst = list(df.loc[df['line content'].str.contains(i[0], na=False), 'line content'])
            if len(lst) != 0:
                for item in lst:
                    print(item+" score: "+str(len(input)*2-int(i[1]))+" location: "+file_path)
                break
    else:
        for item in lst:
            print(item + " score: " + str(len(input)*2) + " location: " + file_path)



def full_combinations(statement):
    for letter in pool: #switch
        for i in range(len(statement)):
            temp = statement[:i] + letter + statement[i:]
            score_down = calculate_char(statement, temp) + 2
            yield temp, score_down
    for letter in pool: #add
        for i in range(len(statement)):
            temp = statement[:i] + letter + statement[i + 1:]
            score_down = calculate_char(statement, temp)*2 + 2 #get down also for worng char
            yield temp, score_down
    for tup in itertools.combinations(statement, len(statement) - 1): #sub
        temp = ''.join(tup)
        score_down = calculate_char(statement, temp) * 2 + 2
        yield temp, score_down

def calculate_char(original, copy):
    i = 0
    if len(original) > len(copy):
        i = 0
        j = 0
        while i < 5:
            if original[i] != copy[j]:
                return 5-i

            else:
                i += 1
                j += 1

    elif len(original) < len(copy):
        pass
    else:
        pass
    while i < len(original) or i < len(copy):


    for i in range(len(original)):
        if original[i] != copy[i] and i < len(original) and i < len(copy):
            if i>=5:
                return 1
            return 5-i
    if i >= 5:
        return 1
    return 5-i

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
    checkOver(path, input)


def main():
    a = input("enter statement: ")
    startup(a)



if __name__ == '__main__':
    main()
