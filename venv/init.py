import pandas as pd
import os

# Folder Path
path = r'2021-archive'

# Read text File
def read_text_file(file_path, input):
    read_file = pd.read_fwf(file_path)
    #read_file.to_csv(f"fixed/{file_path[:-3]}csv")
    new_dir = f"fixed/{os.path.dirname(file_path)}"
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)
    read_file.to_csv(f"fixed/{file_path[:-3]}csv")
    df = pd.read_csv(f"fixed/{file_path[:-3]}csv")
    lst = list(df.loc[df['line content'].str.contains(input, na=False), 'line content'])
    if len(lst) != 0:
        print(lst[0]+" "+file_path)


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
