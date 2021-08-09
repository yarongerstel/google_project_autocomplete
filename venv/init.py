import pandas as pd
import os

# Folder Path
path = r'2021-archive'

# Read text File and write to csv file in "cvs_file" floder
def read_text_file(file_path):
    read_file = pd.read_fwf(file_path)
    print(file_path[:-3])
    file_name=file_path[13:-3].replace("\\",".")
    read_file.to_csv(f"cvs_file\\{file_name}csv")

# run of all filse on tree directory
def checkOver(path):
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            read_text_file(f)
        else:
            checkOver(f)

def startup():
    checkOver(path)


def main():
    startup()


if __name__ == '__main__':
    main()
