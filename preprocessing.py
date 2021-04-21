import os


# Перемещаю файлы из папки "Диалог/*год*" в папку "Диалог"
def change_dialog_directory():
    path = '/Users/mariabocharova/PycharmProjects/Thesis/texts/Диалог'
    for year in range(2003, 2021):
        dirs = os.listdir(f'{path}/{year}')
        for i in dirs:
            os.replace(f'{path}/{str(year)}/{i}', f'{path}/{i}')
        os.remove(f'{path}/{year}')


# Перемещаю все файлы в одну папку "articles"
def change_files_directory():
    dic = {}
    path = '/Users/mariabocharova/PycharmProjects/Thesis/texts'
    for folder in os.listdir(path):
        if folder != '.DS_Store' and os.path.isdir(f'{path}/{folder}'):
            dic[folder] = os.listdir(f'{path}/{folder}')


# os.replace(f'', '/Users/mariabocharova/PycharmProjects/Thesis/texts/articles')
change_files_directory()
