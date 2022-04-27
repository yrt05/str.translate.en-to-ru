import srt
from googletrans import Translator
from pathlib import Path
import os

translator = Translator()

def transl(file):
    with open(file,'r') as data:
        subtitles = list(srt.parse(data))

    for i in range(len(subtitles)):
        q = subtitles[i].content
        ru_subs = translator.translate(q, dest='ru', src='en')
        subtitles[i].content = ru_subs.text

    text = srt.compose(subtitles)
    with open(file,'w') as file:
        file.write(text)

p = input("Введите путь к директорию с субтитрами:")

for foldername, subfolders, filenames in os.walk(p):
    for filename in filenames:
        if filename[-4:] == '.srt':
            pat = foldername + '/' + filename
            p = Path(pat)
            print(f'Переводится файл {p.name}...')
            transl(pat)
            
print("Перевод успешно завершен!")
