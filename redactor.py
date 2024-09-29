import re
from quotes_and_brackets import get_quotes

def remove_tech_line_breaks (text, glue=' ', line_ends=get_quotes() | set('.!?…:;-–—‒؟؛।。！？：；一፡።፣፤፥፦፧፨፠'), start_line=2):
    """Remove technical line breaks in the middle of sentences appearing as a result
    of converting text formats, often PDF to TXT.

    str `text` - text in which to remove technical line breaks;
    set/list/tuple/str `line_ends` - set of characters; if a paragraph ends with
        a charachter from this set, removing line break is not needed here;
    return str - text with technical line breaks removed.
    """

    text = text.split('\n')
    text = [line.strip() for line in text]
    text_edited = [text.pop(0) for _ in range(start_line)]
    
    for i in range(len(text)):
        if text[i] == '':
            continue

        if text_edited[-1][-1] in line_ends or text[i][0] in get_quotes():
            text_edited.append(text[i])
        else:
            text_edited[-1] += glue + text[i]
            
    return '\n'.join(text_edited)

def set_to_str (input_set):
    return ''.join(sorted(list(input_set)))

def replace_by_regex(text, regex, old, new):
    """Replace old substring to new one inside the hits found by regular expression.
    
    str `regex` - string with regular expression for searching hits by re.findall;
    str `old` - string to be replace inside the hits found by regex;
    str `new` - target replacement;
    return: str - text with replacements in the hits.
    """
    
    for hit in set(re.findall(regex, text)):
        hit_replace = hit.replace(old, new)
        text = text.replace(hit, hit_replace)
        
    return text

def recover_apostrophes_by_lang (text, lang, replace_inner=False):
    """Replace typewriter apostrophe "'" to punctuation apostrophe "’" in the text.

    str `text` - text in which to recover apostrophes;
    str `lang` - ISO code of the language of the text;
    bool `replace_inner` - specifies if to recover all the apostrophes located inside
        words, i.e. surrounded by letter characters;
    return str - text with apostrophes recovered.
    """

    if lang == 'en':
        queries = ("I'm", "o'clock", "ma'am", "Qur'an", "ne'er-do-well", "'twere")
        for query in queries:
            for q in (query, query.upper(), query.capitalize()):
                regex = rf"\b{q}\b"
                text = replace_by_regex(text, regex, '\'', '’')
        queries = ('s', 'll', 'd', 've', 're')
        for query in queries:
            for q in (query, query.upper()):
                text = replace_by_regex(text, rf"\w'{q}\b", '\'', '’')
        queries = ("n't")
        for query in queries:
            for q in (query, query.upper()):
                text = replace_by_regex(text, rf"\w{q}\b", '\'', '’')
    elif lang == 'fr':
        queries = ("aujourd'hui")
        for query in queries:
            for q in (query, query.upper(), query.capitalize()):
                regex = rf"\b{q}\b"
                text = replace_by_regex(text, regex, '\'', '’')
        queries = ('c', 'd', 'j', 'l', 'n', 'qu', 't', 'm', 's',
                   'quelqu', 'quoiqu', 'lorsqu', 'puisqu')
        for query in queries:
            for q in (query, query.upper(), query.capitalize()):
                regex = rf"\b{q}'\w"
                text = replace_by_regex(text, regex, '\'', '’')
    elif replace_inner or lang in ('be', 'uk'):
        regex = '\w+\'\w+'
        text = replace_by_regex(text, regex, '\'', '’')
    return text

def get_number_intervals_by_dash (text, dash):
    """Get number intervals of the form "123–456" with a particular dash.

    str `text` - text where to search the number intervals;
    str `dash` - character of dash;
    return set - set of strings from the text representing number intervals
        with dashes.
    """
    
    return set(re.findall(f'\d+ ?{dash} ?\d+', text))