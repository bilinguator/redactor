import re

def print_paragraphs (text, paragraphs, with_number=True, delimiter='\n\n'):
    text = text.split('\n')
    result = []
    for i in paragraphs:
        result.append(text[i])
        result[-1] = f'{str(i)}\n{result[-1]}' if with_number else result[-1]
    print(delimiter.join(result))
    
def search_in_paragraphs (text, query, case_matters=False):
    text = text.split('\n')
    result = dict()
    for i in range(len(text)):
        count = 0
        if case_matters:
            count = text[i].count(query)
        else:
            count = text[i].count(query.lower())
            count += text[i].count(query.upper())
        if count > 0:
            result[i] = count
    return result

def print_paragraphs_by_query (text, query, case_matters=False):
    text = text.split('\n')
    result = []
    for i in range(len(text)):
        if query not in text[i] and case_matters:
            continue
        
        if query.lower() not in text[i].lower() and not case_matters:
            continue
            
        result.append(str(i) + '\n')
        result[-1] += text[i].replace(query, f'\033[1;31m{query}\033[0m') if case_matters \
            else text[i].replace(query.lower(), f'\033[1;31m{query.lower()}\033[0m') \
                .replace(query.upper(), f'\033[1;31m{query.upper()}\033[0m')
    if len(result) > 0:
        print('\n\n'.join(result))

def detect_chapters (text, chapter='', numbering='arabic', delimiter='', with_title=False,
                     numbering_first=False):
    regex = '' if numbering_first else chapter
    if numbering == 'arabic':
        regex = f'{regex}[0-9]+'.strip()
    elif numbering == 'roman':
        regex = f'{regex}[IVXLCDMGH]+'.strip()
    elif numbering in ['ja', 'zh']:
        numerals = '〇一七万三丗两九二五亿仟伍佰億兆兩八六十千卄卅卌叁四廾廿念拾捌柒玖百皕肆萬貳贰陆陸零'
        regex = f'{regex}[{numerals}]+'.strip()
    elif numbering == 'text':
        regex = f'{regex} \D+'.strip()
    
    regex += chapter if numbering_first else ''
    regex += delimiter
    regex += '\w+' if with_title else ''
    
    text = text.split('\n')
    paragraphs = list()
    for i in range(len(text)):
        if bool(re.fullmatch(regex, text[i].strip())):
            paragraphs.append(i)
    
    if bool(paragraphs):        
        for i in paragraphs:
            print(i, text[i], sep='\t')
        return set(paragraphs)
    else:
        print('No paragraphs detected.')
        return set()
    
def tag_paragraphs (text, paragraphs, tag='h1'):
    text = text.split('\n')
    
    for i in range(len(text)):
        if i in paragraphs:
            text[i] = text[i].strip()
            text[i] = f'<{tag}>{text[i]}</{tag}>'

    return '\n'.join(text)

def search_paragraphs_by_regex (text, regex):
    text = text.split('\n')
    paragraphs = []
    for i in range(len(text)):
        if bool(re.fullmatch(regex, text[i].strip())):
            paragraphs.append(i)
    return set(paragraphs)

def print_paragraphs_by_regex (text, regex):
    text = text.split('\n')
    paragraphs = []
    for i in range(len(text)):
        if bool(re.fullmatch(regex, text[i].strip())):
            paragraphs.append(i)
    print_paragraphs('\n'.join(text), paragraphs)

def tag_characters (text, paragraphs, characters, dialogue_delimiter, tag='b'):
    text = text.split('\n')
    characters = [c + dialogue_delimiter for c in characters]
    for i in paragraphs:
        for c in characters:
            if text[i].startswith(c):
                text[i] = f'<{tag}>{c}</{tag}>' + text[i][len(c):]
                break
    return '\n'.join(text)

def remove_paragraphs (text, paragraphs):
    text = text.split('\n')
    
    for i in range(len(text)-1, -1, -1):
        if i in paragraphs:
            del text[i]
            
    return '\n'.join(text)

def count_repeated_paragraphs (text):
    text = text.split('\n')
    unique_paragraphs = set(text)
    repeated_paragraphs = dict()
    
    for paragraph in unique_paragraphs:
        paragraph_count = text.count(paragraph)
        if paragraph_count > 1:
            repeated_paragraphs[paragraph] = paragraph_count
            
    return repeated_paragraphs

def replace_interactively (text, old, new, scope=55):
    old = old if type(old) == list else [old]
    for c in old:
        hits = re.finditer(re.escape(c), text)
        for hit in hits:
            start = hit.start()
            end = hit.end()
            print_start = max(0, start - scope)
            print_end = min(len(text), end + scope)
            printed_text = f'\n{text[print_start:start]}\033[1;31m{text[start:end]}\033[0m{text[end:print_end]}\n'
            print('_'*scope*2)
            print(printed_text)
            if input(f'{c} → {new}? ') != '':
                text = text[:start] + new + text[end:]
    return text