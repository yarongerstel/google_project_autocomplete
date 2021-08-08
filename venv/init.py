import pandas as pd

if __name__ == '__main__':
    main()


def startup():

def main():
    read_file = pd.read_csv(r'C:\Users\USER001\PycharmProjects\google_project_autocomplete\2021-archive.txt')
    read_file.to_csv(r'C:\Users\USER001\PycharmProjects\google_project_autocomplete\venv\txt.csv', index=None)
    