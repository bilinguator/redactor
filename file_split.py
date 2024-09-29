import os
import re
from itertools import zip_longest
import matplotlib.pyplot as plt


def plot_paragraphs_counts (text, by='<h1>', chapters_in_first_file=2, chapters_per_file=(1, 10)):
    """Plot how many files with how many paragraphs are created by dividing the text into parts of
        different chapters counts. Nothing is returned.
    
    str `text` - text to be splitted;
    str `by` - delimiter by which to divide text into chapters (it is not deleted from the text),
        specify "<h1>" (default) to divide text by headers into actual chapters;
    int `chapters_in_first_file` - defines how many chapters to write in the first file, default
        is 3 to include the author, title (tagged with "<h1></h1>") and first chapter parts;
    tuple `chapters_per_file` - tuple of 2 int - plotted range (both sides included) of chapters
        written to the second and all subsequent files.
    """
    
    mean_paragraph_counts = []
    
    for i in range(chapters_per_file[0], chapters_per_file[1]+1):
        text_splitted = split_text(text, by=by, chapters_in_first_file=chapters_in_first_file,
                                   chapters_per_file=i, verbose=False)
        mean_paragraph_counts.append([part.count('\n')+1 for part in text_splitted])
    
    xlabels = list(zip([len(mean_count) for mean_count in mean_paragraph_counts],
                       range(chapters_per_file[0], chapters_per_file[1]+1)))
    xlabels = [f'{files} files × {chapters} chapters' for files, chapters in xlabels]

    plt.figure(figsize=(5, 5))
    plt.boxplot(mean_paragraph_counts, labels=xlabels, vert=False, patch_artist=True)
    plt.xlabel('Paragraphs counts')
    plt.show()


def split_text (text, by='<h1>', chapters_in_first_file=3, chapters_per_file=1, verbose=True):
    """Split text into several parts with defined counts of chapters.

    str `text` - text to be splitted;
    str `by` - delimiter by which to divide text into chapters (it is not deleted from the text),
        specify "<h1>" (default) to divide text by headers into actual chapters;
    int `chapters_in_first_file` - defines how many chapters to write in the first file, default
        is 3 to include the author, title (tagged with "<h1></h1>") and first chapter parts;
    int `chapters_per_file` - count of chapters written to the second and all subsequent files.

    return list of str - text splitted into parts.
    """
    
    chapters = [chapter.strip() for chapter in text.split(by) if chapter != '']
    chapters = [by+chapter for chapter in chapters]
    
    if chapters[0] == by:
        del chapters[0]
    else:
        chapters[0] = chapters[0] if text.startswith(by) else chapters[0].replace(by, '', 1)
        
    total_chapters_count = len(chapters)
    
    part1 = ['\n'.join(chapters[:chapters_in_first_file])]
    parts_rest = chapters[chapters_in_first_file:]
    
    parts_rest = [list(filter(None, group)) for group in zip_longest(*[iter(parts_rest)]*chapters_per_file)]
    parts_rest = ['\n'.join(group).strip() for group in parts_rest]
    
    parts = part1 + parts_rest
    
    if verbose:
        print('Total chapters count:', total_chapters_count)
        print('Total paragraphs count:', text.count('\n')+1)
        print('Total symbols count', len(text))
        print('Chapters count in the first file:', chapters_in_first_file)
        print('Chapters count per file:', chapters_per_file)
        print()
        print('Files count:', len(parts))
        print('Chapters counts:')
        chapters_counts = []
        for part in parts:
            chapters_count = len(part.split(by))-1 if part.startswith(by) else len(part.split(by))
            chapters_counts.append(chapters_count)
        print(*chapters_counts, sep='\t')
        print('Paragraphs counts:')
        print(*[part.count('\n')+1 for part in parts], sep='\t')
        print('Symbols counts:')
        print(*[len(part) for part in parts], sep='\t')
        
    return parts


def split_file (file_address, text_splitted):
    """Split file into several parts according to `text_splitted`. Each part is named as
        `file_address` + index. Nothing is returned.

    str `file_address` - path to file to be splitted;
    list of str `text_splitted` - text splitted into parts.
    """

    digits_count = len(str(len(text_splitted)))
    
    print('\033[1mFiles created:\033[0m')
    
    for i in range(len(text_splitted)):
        i_digits_count = len(str(i+1))
        file_index = '0'*(digits_count-i_digits_count) + str(i+1)
        
        with open(file_address+file_index, 'w', encoding='utf-8') as file:
            file.write(text_splitted[i])

        if os.path.isfile(file_address+file_index):
            print(file_address+file_index)


def merge_file (file_address):
    """Merge files named as `file_address`+index to one file. Nothing is returned.
    
    str `file_address` - path to file to be merged. Function searches for files
        named as `file_address`+index, writes their contents to `file_address`
        delimited by line breaks "\\n" and deletes them.
    """
    
    file_folder = os.path.dirname(file_address)
    file_name = os.path.basename(file_address)
    file_paths = sorted([f'{file_folder}/{file}' for file in os.listdir(file_folder)
                         if bool(re.fullmatch(f'{file_name}\d+', file))])
    
    if len(file_paths) == 0:
        print('Nothing to merge!')
        return
        
    os.replace(file_paths[0], file_address)
    merged_file = open(file_address, 'a', encoding='utf-8')

    for path in file_paths[1:]:
        with open(path, 'r', encoding='utf-8') as part_file:
            part_text = part_file.read()

        merged_file.write(f'\n{part_text}')
        os.remove(path)

    merged_file.close()
    
    print(f'{len(file_paths)} files have been merged to 1:')
    print(file_address)