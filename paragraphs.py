import re

def print_paragraphs (text, paragraphs, with_number=True, delimiter='\n\n'):
    """Print specified paragraphs of the text.

    str `text` - text, paragraphs of which need to be printed;
    list/set/tuple `paragraphs` - set of numbers of paragraphs to print;
    bool `with_number` - determines if numbers of paragraphs are printed;
    str `delimiter` - string to be printed between paragraphs.
    """

    text = text.split('\n')
    result = []
    for i in paragraphs:
        result.append(text[i])
        result[-1] = f'{str(i)}\n{result[-1]}' if with_number else result[-1]
    print(delimiter.join(result))


def search_in_paragraphs (text, query, case_matters=False):
    """Get numbers of paragraphs containing a particular query substring with counts
        of the query.
    
    str `text` - text where to search paragraphs and query;
    str `query` - substring to be found in paragraphs;
    bool `case_matters` - determines if case of th query matters;
    result dict - key: paragraph number, value: count of `query` in the paragraph.
    """

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
    """Print paragraphs containing a particular query substring.
    
    str `text` - text where to search paragraphs and query;
    str `query` - substring to be found in paragraphs;
    bool `case_matters` - determines if case of th query matters.
    """
    
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
                     numbering_first=False, return_content=False):
    """Get and print paragraphs containing chapters' headings. 
    
    str `chapter` - string containing key word for a chapter, e.g.
        "Chapter" for English, "Глава" for Russian, "Chapitre" for French,
        etc.; word case matters here; the space character delimiting the key
        word from a numeral is the part of this argument;
    str `numbering` - string of one of the following variants:
        - "arabic" for Arabic numbers ("1", "2", "3", etc.);
        - "roman" for the Roman numbers ("I", "II", "III", "IV", etc.);
        - "ja" or "zh" for Japanese or Chinese numerals ("一"、"二"、"三"
            "四", etc.);
        - "text" for non-numeric characters; suitable if numerals in words are
            presented ("One", "Two", "Three", etc.)
        - "ar", "fa" or "ur" for Eastern Arabic numerals ("۰", "۱", "۲", etc.),
            used in Arabic, Persian and Urdu languages;
        - "abjad" for Abjad numerals ("ا", "ب", "ج", etc.);
        - "indian" for languages of India: Bengali, Devanagari, Tamil, etc.
        - "th" for Thai ("๑", "๒", "๓", etc.);
        - "lo" for Lao ("໑", "໒", "໓", etc.);
        - "tibetic" for Tibetic ("༡", "༢", "༣", etc.);
        - "my" for Burmese ("၁", "၂", "၃", etc.);
        - "km" for Khmer ("១", "២", "៣", etc.);
        - "mn" for Mongolian ("᠑", "᠒", "᠓", etc.);
        - "lif" for Limbu ("᥇", "᥈", "᥉", etc.);

    str `delimiter` - delimiter among the chapter-numbering and title parts;
    bool `with_title` - specifies if chapters have titles;
    bool `numbering_first` - specifies if numbering precedes chapter key word
        (e.g., "XIX chapter");
    bool `paragraphs_content` - ruturn both paragraphs indexes and content;

    return:
        if `paragraphs_content` equals False:
            set of numbers of paragraphs containing chapters' headings;
        if `paragraphs_content` equals True:
            (list, list) - list of numbers of paragraphs containing chapters'
            headings and list of paragraphs' contents;

    If the chapters' headings of your text look like "Chapter MMMCMXCIX — Epilogue",
        specify arguments as follows:

        chapter = 'Chapter ',
        numbering = 'roman',
        delimiter = ' — ',
        with_title = True,
        numbering_first = False.
    """

    regex = '' if numbering_first else chapter
    if numbering == 'arabic':
        regex = f'{regex}[0-9１２３４５６７８９①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑⒒⒓⒔⒕⒖⒗⒘⒙⒚⒛⓪⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾⓿0⃣1⃣2⃣3⃣4⃣5⃣6⃣7⃣8⃣9⃣🔟]+'.strip()
    elif numbering == 'roman':
        regex = f'{regex}[IVXLCDMivxlcdmⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅬⅭⅮⅯⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹⅺⅻⅼⅽⅾⅿ]+'.strip()
    elif numbering == 'text':
        regex = f'{regex} \D+'.strip()
    elif numbering in ['ja', 'zh']:
        regex = f'{regex}[〇一七万三丗两九二五亿仟伍佰億兆兩八六十千卄卅卌叁四廾廿念拾捌柒玖百皕肆萬貳贰陆陸零]+'.strip()
    elif numbering in ['ar', 'fa', 'ur']:
        regex = f'{regex}[۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩]+'.strip()
    elif numbering == 'abjad':
        regex = f'{regex}[أبجدﻩوﺯﺡﻁﻱﻙﻝﻡﻥﺱﻉﻑصﻕﺭﺵﺕﺙﺥﺫﺽﻅﻍ]+'.strip()
    elif numbering == 'indian':
        regex = f'{regex}[०१२३४५६७८९০১২৩৪৫৬৭৮৯୦୧୨୩୪୫୬୭୮୯௦௧௨௩௪௫௬௭௮௯౦౧౨౩౪౫౬౭౮౯೦೧೨೩೪೫೬೭೮೯൦൧൨൩൪൫൬൭൮൯]+'.strip()
    elif numbering == 'th':
        regex = f'{regex}[๐๑๒๓๔๕๖๗๘๙]+'.strip()
    elif numbering == 'lo':
        regex = f'{regex}[໐໑໒໓໔໕໖໗໘໙]+'.strip()
    elif numbering == 'tibetic':
        regex = f'{regex}[༠༡༢༣༤༥༦༧༨༩]+'.strip()
    elif numbering == 'my':
        regex = f'{regex}[၀၁၂၃၄၅၆၇၈၉]+'.strip()
    elif numbering == 'km':
        regex = f'{regex}[០១២៣៤៥៦៧៨៩]+'.strip()
    elif numbering == 'mn':
        regex = f'{regex}[᠐᠑᠒᠓᠔᠕᠖᠗᠘᠙]+'.strip()
    elif numbering == 'lif':
        regex = f'{regex}[᥆᥇᥈᥉᥊᥋᥌᥍᥎᥏]+'.strip()
    
    regex += chapter if numbering_first else ''
    regex += delimiter
    regex += '.+' if with_title else ''
    
    text = text.split('\n')
    paragraphs = []
    paragraphs_content = []

    for i in range(len(text)):
        if bool(re.fullmatch(regex, text[i].strip())):
            paragraphs.append(i)
            paragraphs_content.append(text[i])
    
    if bool(paragraphs):
        for i in paragraphs:
            print(i, text[i], sep='\t')

        if return_content:
            return paragraphs, paragraphs_content
        
        return set(paragraphs)
    else:
        if return_content:
            return None, None
        
        print('No paragraphs detected.')
        return set()


def tag_paragraphs (text, paragraphs, tag='h1'):
    """Enclose specified paragraphs of the text in tags.

    str `text` - text in which to tag paragraphs;
    list/set/tuple `paragraphs` - set of numbers of paragraphs to tag;
    str `tag` - tag in which to enclose specified paragraphs;
    return str - text with tagged paragraphs.
    """
    
    text = text.split('\n')
    for i in range(len(text)):
        if i in paragraphs:
            text[i] = text[i].strip()
            text[i] = f'<{tag}>{text[i]}</{tag}>'
    return '\n'.join(text)


def search_paragraphs_by_regex (text, regex):
    """Get numbers of paragraphs matching regular expression.

    str `text` - text in which to search matching paragraphs;
    str `regex` - regular expression used to search matching paragraphs;
    return set - numbers of paragraphs matching regular expression.
    """

    text = text.split('\n')
    paragraphs = []
    for i in range(len(text)):
        if bool(re.fullmatch(regex, text[i].strip())):
            paragraphs.append(i)
    return set(paragraphs)


def print_paragraphs_by_regex (text, regex):
    """Print paragraphs matching regular expression.

    str `text` - text in which to search matching paragraphs;
    str `regex` - regular expression used to search matching paragraphs;
    """

    text = text.split('\n')
    paragraphs = []
    for i in range(len(text)):
        if bool(re.fullmatch(regex, text[i].strip())):
            paragraphs.append(i)
    print_paragraphs('\n'.join(text), paragraphs)


def tag_characters (text, paragraphs, characters, dialogue_delimiter, tag='b'):
    """Enclose characters names in the play to the specified tags.

    str `text` - text in which to tag characters' names;
    list/set/tuple `paragraphs` - set of numbers of paragraphs to in which to tag
        characters' names;
    list/set/tuple `characters` - set of characters' names;
    str `dialogue_delimiter` - specifies what punctuation mark separates characters'
        names from their speeches;
    str `tag` - tag in which to enclose characters' names;
    return str - text with characters' names tagged.
    """
    
    text = text.split('\n')
    characters = [c + dialogue_delimiter for c in characters]
    for i in paragraphs:
        for c in characters:
            if text[i].startswith(c):
                text[i] = f'<{tag}>{c}</{tag}>' + text[i][len(c):]
                break
    return '\n'.join(text)


def remove_paragraphs (text, paragraphs):
    """Remove paragraphs from the text.

    str `text` - text in which to remove paragraphs;
    list/set/tuple `paragraphs` - set of numbers of paragraphs to remove;
    return str - text with paragraphs removed.
    """

    text = text.split('\n')
    for i in range(len(text)-1, -1, -1):
        if i in paragraphs:
            del text[i]
    return '\n'.join(text)


def count_repeated_paragraphs (text):
    """Count repeated paragraphs.

    str `text` - text in which to coint repeated paragraphs;
    return dict - key: str with repeated paragraph, value - its count (int).
    """

    text = text.split('\n')
    unique_paragraphs = set(text)
    repeated_paragraphs = dict()
    
    for paragraph in unique_paragraphs:
        paragraph_count = text.count(paragraph)
        if paragraph_count > 1:
            repeated_paragraphs[paragraph] = paragraph_count
            
    return repeated_paragraphs


def replace_interactively (text, old, new, scope=55):
    """Replace one substring to another in the text in the interaction mode.

    str `text` - text in which to conduct replacement;
    str `old` - substring to be replaced;
    str `new` - replacement;
    int `scope` - how many characters to print to the right and to the left
        from the old substring;
    return str - text with the result of replacement.

    Usage:
    text = replace_interactively(text, '“', '‘')
    
    Each hit of the old substring will be accompanied with the input field.
    Leave the field empty if the replacement is not needed. Otherwise, type
    anything. Press Enter to confirm your choise.
    """

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


def join_strophes (text, delimiter='<delimiter>', start_line=2, min_line_breaks=2):
    """Join strophes with <delimiter>, so they constitute separate paragraphs.
    Strophe in this case is the part of a text, separated by more than one line breaks (\\n).

    str `text` - text in which to join strophes;
    str `delimiter` - glue with which join lines in strophes;
    int `start_line` - 0-based index of the first line where function starts to act;
    int `min_line_breaks` - minimal line breaks count between strophes;
    return str - text with the strophes joined.
    """

    text = text.split('\n')
    omitted_lines = text[:start_line]
    text = '\n'.join([line.strip() for line in text[start_line:]])
    text = [delimiter.join(re.split('\n+', line.strip()))
            for line in re.split(f'\n{{{min_line_breaks},}}', text)
            if line.strip() != '']
    text = '\n'.join(omitted_lines + text)
    return text


def detach_paragraphs (text, tags, delimiter):
    """Detach paragraphs with specified tags which are glued with delimiter.

    str `text` - text in which to detach paragraphs;
    list `tags` - list of str of tags;
    str `delimiter` - string-glue to be replaced with \\n;
    return str - text with paragraphs detached. 
    """
    
    for tag in tags:
        text = text.replace(f'{delimiter}<{tag}>', f'\n<{tag}>')
        text = text.replace(f'</{tag}>{delimiter}',  f'</{tag}>\n')
    return text


def trim_paragraphs (text, characters):
    """Trim leading and trailing characters specified in `symbols` in every
    paragraph of the `text`.
    
    str `text` - text where to trim paragraphs;
    str `characters` - characters to be trimmed.
    
    return str - text with paragraphs trimmed.
    """
    
    text = [paragraph.strip(characters) for paragraph in text.split('\n')]
    return '\n'.join(text)


def capitalyze (text):
    """Capytalyze text: make it lower cased, and make
    first possible letter to be upper cased.
    
    str `text` - text to be capitalyzed;
    
    return str - capitalized text.
    """
    
    text = text.lower()
    upper_char_index = None
    
    for i in range(len(text)):
        if text[i] != text[i].upper():
            upper_char_index = i
            break
    
    if upper_char_index != None:
        text = text[:upper_char_index+1].upper() + text[upper_char_index+1:]
        
    return text


def change_headings_case (text, paragraphs, case='capitalised', tags=['h1']):
    """Change headings case not changing tags in interactive mode.
    
    str `text` - text where to change headings case;
    iterable `paragraphs` - list of int: paragraphs numbers of headings;
    str `case` - what case to apply: "capitalised" (i.e. first letter upper, default),
        "upper" for upper case or "lower" for lower case;
    iterable `tags` - list of str: tags which case will not be changed.
        Default: ['h1'] for "<h1>" and </h1> tags.
        
    return str - text where headings have changed case.
    """
    
    message = ('\033[1mEnter one of the options:\033[0m\n'
               '"y" – accept replacement;\n'
               '"n" or empty input – reject replacement;\n'
               'or enter your variant for replacement.\n')
    print(message)

    text = text.split('\n')
    
    for i in paragraphs:
        changed_heading = text[i]
        
        for tag in tags:
            changed_heading = re.split(rf'(</?{tag}>)', changed_heading)
            changed_heading = [c for c in changed_heading if c != '']
            
            for j in range(len(changed_heading)):
                if changed_heading[j] in (f'<{tag}>', f'</{tag}>'):
                    continue
                
                if case == 'capitalised':
                    changed_heading[j] = capitalyze(changed_heading[j])
                    
                elif case == 'upper':
                    changed_heading[j] = changed_heading[j].upper()
                    
                elif case == 'lower':
                    changed_heading[j] = changed_heading[j].lower()
            
            changed_heading = ''.join(changed_heading)
        
        message = '\n\033[1mOld heading\033[0m\n'
        message += text[i]
        message += '\n\n\033[1mReplacement\033[0m\n\n'
        message += changed_heading
        print(message)
        
        reply = input().strip()
        
        if reply.lower() in ('y', 'д'):
            text[i] = changed_heading
        elif reply.lower() in ('n', 'н', ''):
            pass
        else:
            text[i] = reply
            
    return '\n'.join(text)


def insert_corresponding_paragraphs(text, paragraphs, paragraphs_content):
    """Insert paragraphs contents by their indexes to text.
    
    str `text` - text where to insert paragraphs;
    list `paragraphs` - list of paragraphs numbers;
    list `paragraphs_content` - list of paragraphs contents.
    
    return str - text with new paragraphs. 
    """
    
    paragraphs = [paragraphs[i] - i for i in range(len(paragraphs))]
    
    text = text.split('\n')
    print(len(text))
    
    for i in range(len(paragraphs)):
        if paragraphs[i] < len(text):
            text[paragraphs[i]] = paragraphs_content[i] + '\n' + text[paragraphs[i]]
        else:
            text.append(paragraphs_content[i])
    
    return '\n'.join(text)