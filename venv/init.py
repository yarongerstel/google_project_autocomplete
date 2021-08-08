import pandas as pd
import os

# Folder Path
#path = r'2021-archive'
path = r'test'

# Read text File
def read_text_file(file_path):
    read_file = pd.read_fwf(file_path)
    print(file_path[:-3])
    read_file.to_csv(f"{file_path[:-3]}csv")


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
