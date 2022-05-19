import os
from pathlib import Path
import srt
from googletrans import Translator
from progress.bar import IncrementalBar
from typing import NoReturn


translator = Translator()


def lang_detect(pa):
    with open(pa, 'r') as data:
        subtitles = list(srt.parse(data))
    dt1 = translator.detect(subtitles[0].content)
    return dt1.lang


def file_translator(file) -> NoReturn:

    if lang_detect(file) == "en":

        with open(file, 'r') as data:
            subtitles = list(srt.parse(data))

        bar = IncrementalBar(f'Перевод {file.name}', max=len(subtitles))
        for i in range(len(subtitles)):
            bar.next()
            q = subtitles[i].content
            ru_subs = translator.translate(q, dest='ru', src='en')
            subtitles[i].content = ru_subs.text
        bar.finish()

        text = srt.compose(subtitles)
        with open(file, 'w') as file:
            file.write(text)
    else:
        print(f'Файл {file.name} уже переведен')


def main(ppath) -> NoReturn:
    path_files_list = []

    for foldername, subfolders, filenames in os.walk(ppath):
        for filename in filenames:
            if filename.endswith('.srt'):
                path_files_list.append(Path(os.path.join(foldername, filename)))

    for path_to_sub in sorted(path_files_list):
        file_translator(path_to_sub)


if __name__ == '__main__':
    p = input("Введите путь к директорию с субтитрами:")
    path = Path(p)
    if str(path).endswith('.srt'):
        file_translator(path)
    else:
        main(path)
