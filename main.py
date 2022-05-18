from pathlib import Path
import os
import string
import srt
from googletrans import Translator


translator = Translator()

def filter_for_transl_files(j: str) -> bool:
    return all([True if i not in string.ascii_letters else False for i in j])
    
    
def transl(file) -> None:
    '''file translate function'''
    with open(file,'r') as data:
        subtitles = list(srt.parse(data))

    first_word = subtitles[0].content.split()[0]
    if not filter_for_transl_files(first_word):
        for i in range(len(subtitles)):
            q = subtitles[i].content
            ru_subs = translator.translate(q, dest='ru', src='en')
            subtitles[i].content = ru_subs.text

        text = srt.compose(subtitles)
        with open(file,'w') as file:
            file.write(text)
            
    else:
        pass


def main(p) -> None:
    path = Path(p)
    if p.endswith('.srt'):
        print(f'Переводится файл {path.name}...')
        transl(path)
    else:
        for foldername, subfolders, filenames in os.walk(p):
            for filename in filenames:
                if filename[-4:] == '.srt':
                    path = os.path.join(foldername, filename)
                    print(f'Переводится файл {path.name}...')
                    transl(path)


if __name__ == '__main__':
    p = input("Введите путь к директорию с субтитрами:")
    main(p)
    print("Перевод успешно завершен!")
