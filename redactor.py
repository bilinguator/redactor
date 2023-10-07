from quotes_and_brackets import get_quotes

def remove_tech_line_breaks (text, line_ends=get_quotes() | set('.!?;-–—‒')):
    text = text.split('\n')
    text = [line.strip() for line in text]
    text_edited = list([text.pop(0)])
    
    for i in range(len(text)):
        if text[i] == '':
            continue
        if text_edited[-1][-1] in line_ends:
            text_edited.append(text[i])
        else:
            text_edited[-1] += ' ' + text[i]
            
    return '\n'.join(text_edited)

def set_to_str (input_set):
    return ''.join(sorted(list(input_set)))

def replace_by_regex (text, regex, old_substr, new_substr):
    hits = re.finditer(regex, text)
    for hit in hits:
        start = hit.start()
        end = hit.end()
        text = text[:start] + text[start:end].replace(old_substr, new_substr) \
            + text[end:]
    return text

def recover_apostrophes_by_lang (text, lang, replace_inner=False):
    if lang == 'en':
        queries = ["I'm", "o'clock", "ma'am", "Qur'an", "ne'er-do-well", "'twere"]
        for query in queries:
            for q in [query, query.upper(), query.capitalize()]:
                regex = rf"\b{q}\b"
                text = replace_by_regex(text, regex, '\'', '’')
        queries = ['s', 'll', 'd', 've', 're']
        for query in queries:
            for q in [query, query.upper()]:
                text = replace_by_regex(text, rf"\w'{q}\b", '\'', '’')
        queries = ["n't"]
        for query in queries:
            for q in [query, query.upper()]:
                text = replace_by_regex(text, rf"\w{q}\b", '\'', '’')
    elif lang == 'fr':
        queries = ["aujourd'hui"]
        for query in queries:
            for q in [query, query.upper(), query.capitalize()]:
                regex = rf"\b{q}\b"
                text = replace_by_regex(text, regex, '\'', '’')
        queries = ['c', 'd', 'j', 'l', 'n', 'qu', 't', 'm', 's',
                   'quelqu', 'quoiqu', 'lorsqu', 'puisqu']
        for query in queries:
            for q in [query, query.upper(), query.capitalize()]:
                regex = rf"\b{q}'\w"
                text = replace_by_regex(text, regex, '\'', '’')
    elif replace_inner or lang in ['be', 'uk']:
        regex = rf"\w{q}'\w"
        text = replace_by_regex(text, regex, '\'', '’')
    return text

def get_number_intervals_by_dash (text, dash):
    return set(re.findall(f'\d+ ?{dash} ?\d+', text))

def join_speeches (text, delimiter='<delimiter>'):
    text = text.split('\n')
    text = [text[0]] + ['\n'+line if bool(re.fullmatch('<b>.*|<h1>.*', line)) \
                                  else delimiter+line for line in text[1:]]
    return ''.join(text)