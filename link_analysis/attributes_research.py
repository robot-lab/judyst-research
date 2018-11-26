import re
import json
import collections as cl
import numpy as np
'''
==============================
Инициализация исследования
==============================
'''
class KSRF_Solution:
    def __init__(self, header=None, form=None, beginning=None, topic=None, 
                 date_created=None, number=None, keyword=None, judges=None, main_judge=None):
        self.header = header
        self.form = form
        self.beginning = beginning
        self.topic = topic
        self.date_created = date_created
        self.number = number
        self.keyword = keyword
        self.judges = judges
        self.main_judge = main_judge
    def __repr__(self):
        return (f'header: {self.header}, form: {self.form}, '
               f'begins with: {self.beginning}, '
               f'topic: {self.topic}, '
               f'created on: {self.date_created}, '
               f'number: {self.number}, keyword: {self.keyword}, '
               f'judges: {self.judges}, main judge: {self.main_judge}')
with open('headers_names.txt', 'r+', encoding='utf-8') as headers:
    headers_list = [header.rstrip('\n') for header in headers]
headers_list.sort()
anything = re.compile(r'.+')
bodypart = (re.compile(r'.*(?=(?:(?:постанов|реш|определ)'
                                         r'(?:ил ?|ляет ?)|(?:о п р е д е л |'
                                         r'п о с т а н о в )и л *)(?=:))'))
reso = re.compile(r'(?<=:).*')
before_ending = re.compile(r'.*(?:не подлежит\.? *(?![,а-я])|Федерации["»]\.? *(?![,а-я]))')
simple_link = (re.compile(r'(?u)от +\d+ +\w+ +\d+ +года? +[№N] *[\dОПРЗУ/-]+[ОПРЗУ/-]+(?=\s)'
                          r'|(?u)от +\d{2}\.\d{2}\.\d{4} +[№N] *[\dОПРЗУ/-]+[ОПРЗУ/-]+(?=\s)'))
judge = re.compile(r'[А-Я]\.[А-Я]\.[А-Яа-яЁё]+(?!\.)|[А-Я]\.[А-Яа-яЁё]+')
'''
definitions_list = []
solutions_list = []
rulings_list = []
prpdefs_list = []
'''
docs_under_research = []
#print(sorted(list(set(re.findall(r'(?<=\d-)[А-Я-]+(?=[._])', str(headers_list))))))

for header in headers_list:
    #if re.fullmatch(r'[^О]+О_1999.txt', header) is not None:
    if (re.fullmatch(r'[^О]+О-{0,2}[ПР]?[^ОПР]+', header) is not None or
        re.fullmatch(r'.+КСРФ[^ОП]+Р.+', header) is not None or
        re.fullmatch(r'.+КСРФ[^ОР]+П[^Р]+', header) is not None or
        re.fullmatch(r'.+ПРП.+', header) is not None):
        #definitions_list.append(header)
    #elif re.fullmatch(r'.+КСРФ[^ОП]+Р.+', header) is not None:
        #solutions_list.append(header)
    #elif re.fullmatch(r'.+КСРФ[^ОР]+П[^Р]+', header) is not None:
        #rulings_list.append(header)
    #elif re.fullmatch(r'.+ПРП.+', header) is not None:
        #prpdefs_list.append(header)
        docs_under_research.append(header)
    
'''
with open('definitions.txt', 'w', encoding='utf-8') as deflistfile:
    for defin in definitions_list:
        deflistfile.write(f'{defin}\n')

with open('solutions.txt', 'w', encoding='utf-8') as solulistfile:
    for sol in solutions_list:
        solulistfile.write(f'{sol}\n')  

with open('rulings.txt', 'w', encoding='utf-8') as rullistfile:
    for rul in rulings_list:
        rullistfile.write(f'{rul}\n')
 

with open('prp_definitions.txt', 'w', encoding='utf-8') as prplistfile: 
    for prp in prpdefs_list:
        prplistfile.write(f'{prp}\n')

for header in headers_list:
    if re.fullmatch(r'.+О-О.+', header) is not None:
        unused_list.append(header)
    if re.fullmatch(r'[^О]+ПР[^П]+', header) is not None:
        unused_list.append(header)
with open('unused_docs.txt', 'w', encoding='utf-8') as unusedfile:
    for doc in unused_list:
        unusedfile.write(f'{doc}\n')
'''
docnumber = len(docs_under_research)
print(f'Number of docs under research: {docnumber}')
headers_true_names = []
for doc in docs_under_research:
    headers_true_names.append(re.search(r'(?<=\\).*(?=\.)', re.sub(r'_', r'/', doc))[0])
'''
1. Поиск ключевых слов, а заодно и вывод решений, в тексте которых нет ключевых слов
'''
#numberlist = []
wordlist = []
listoflists = []
keywords_list = []
with open('weird-docs_list.txt', 'w', encoding='utf-8') as wdl:
    for doc in docs_under_research:
        with open(doc, 'r+', encoding='utf-8') as docfile:
            text = docfile.read()
            opinion = (re.search(r'(?iu)(?:особое *| *)'
                                r'мнение\s+судьи\s+конституционного', text))
            if opinion is not None:
                text = anything.search(text, endpos=opinion.start())[0]
                #print(f'{doc}, \n{text}\n')
            #curtuple = (tuple(re.findall(r'\w+ил(?=:)|(?:(?:о п р е д е л |'
            #                             r'(?:п о|у) с т а н о в )и л ?)'
            #                             r'(?=:)|(?:постановляет)(?=:)', text)))
            curtuple = (tuple(re.findall(r'(?:(?:постанов|реш|определ)'
                                         r'(?:ил ?|ляет ?)|(?:о п р е д е л |'
                                         r'п о с т а н о в )и л *)(?=:)', text)))
            if len(curtuple) > 0:
               keywords_list.append(curtuple[-1])
            else:
                curtuple = tuple(re.findall(r'определил ', text))
                if len(curtuple) > 0:
                    keywords_list.append(curtuple[-1])
                else:
                    keywords_list.append('NONE')
            #listoflists.append(curtuple)

            #выводим подозрительные решения
            '''
            
            if (len(curtuple) != 2 or
                 re.findall(  #r'(?:о п р е д е л |(?:п о|у) с т а н о в )и л *'
                              r'(?:определ|(?:по|у)станов)ил'
                              r'|(?:о п р е д е л |(?:п о|у)'
                              r' с т а н о в )и л ?'
                              , str(curtuple)) == []):
                    wdl.write(f'{docfile.name}: {str(curtuple)}\n')
            
            '''
            
            if len(curtuple) != 1:
                wdl.write(f'{docfile.name}: {str(curtuple)}\n')
            #if len(wordlist) == 1:
                
                #and re.findall(r'у с т а н о в и л ?:', text) == [] and re.findall(r'о п р е д е л и л ?:', text) == []:
                #wdl.write(defifile.name + '\n')
            #else: 
               # if len(wordlist) != 1:
               #     numberlist.append(len(wordlist))
#print(numberlist)
#print(sum(numberlist) + 9)
#print(keywords_list)
#for keyword in keywords_list:
    #if keyword == 'NONE':
        #print(keyword)
words_ct = cl.Counter(keywords_list)
#words_tuple_ct = cl.Counter(listoflists)
#print(words_ct)
#print(words_tuple_ct)
#print(len(anyjudgeslist))
with open('docs-words_stats.txt', 'w', encoding='utf-8') as statsfile:
    statsfile.write(f'{str(words_ct)}\n')
'''
2. Выделение начала документов для выделения темы и даты
'''
beginnings_list = []
with open('beginnings_list.txt', 'w', encoding='utf-8') as begfile:
    for docname in docs_under_research:
        with open(docname, 'r+', encoding='utf-8') as docfile:
            text = docfile.read()
            text = re.sub(r'1 об', r'об', text)
            text = re.sub(r'менем.*?(?=[А-Я][А-Я])', '', text)
            #text = re.sub(r'\((?=по жа)', '**', text)
            #beg = re.search(r'(?<=\*\*).*?(?=\))', text)
            #if beg is not None:
            #    beginnings_list.append(beg[0])
            #    begfile.write(f'{docfile.name}:\n\n{beg[0]}\n\n')
            #else:
            beg = (re.search(r'(?<=\b)[а-я0-9].*?'
                            r'(?=(?:Рассмотрев|[Кк]онституционный +[Сс]уд))', text))
            if beg is not None:
                finalbeg = re.sub(r'(?<!о)б +отказе', r'об отказе', beg[0])
                #finalbeg = beg[0]
                beginnings_list.append(finalbeg)
                begfile.write(f'{docname}:\n\n{finalbeg}\n\n')
#print(len(beginnings_list))
'''
3. Поиск даты и темы, приведение их к некоторому нормальному виду
'''
dates_list = []
topics_list = []
#shitlist = []

with open('raw_dates.txt', 'w', encoding='utf-8') as dcfile:
    for i in range(len(beginnings_list)):
        
        #curdate = re.findall(r'(?iu)(?:(?:(?:(?:города?|г.)| *)(?: *Санкт-Петербурга? *| *Москв[аы] *)(?:\W*?| *от *)| *)\"?\d{1,2}\"? *?\w+ *?\d\d\d\d(?: *| *год[ а] *))(?=$)|(?:\"?\d{1,2}\"? *?\w+ *?\d\d\d\d(?: ?| *год[ а])[ ,] *?(?:(?:г\.?|города?)| *)(?: *Санкт-Петербурга? *| *Москв[аы] *))(?=$)', beginnings_list[i])
        curdate = (re.findall(r'(?iu)(?:(?:от *)?["“”]?\d{1,2}["“”]?'
                                    r' *?\w+ *?\d\d\d\d(?: *| *год[ а] *))'
                                    r'(?=$)', beginnings_list[i]))
        if curdate != []:
            pass
            #dcfile.write(f'{docs_under_research[i]}: \n{str(date_and_city)}\n\n')
        else:
            #curdate = re.findall(r'(?iu)(?:(?:(?:(?:города?|г.)| *)(?: *Санкт-Петербурга? *| *Москв[аы] *)(?:\W*?| *от *)| *)\"?\d{1,2}\"? *?\w+ *?\d\d\d\d(?: *| *год[ а] *))|(?:\"?\d{1,2}\"? *?\w+ *?\d\d\d\d(?: ?| *год[ а])[ ,] *?(?:(?:г\.?|города?)| *)(?: *Санкт-Петербурга? *| *Москв[аы] *))', beginnings_list[i])
            curdate = (re.findall(r'(?iu)(?:от *)?["“”]?\d{1,2}["“”]?'
                                        r' *?\w+ *?\d\d\d\d(?: *| *год[ а]'
                                        r' *)', beginnings_list[i]))
            if len(curdate) > 1:
                curdate[:-1] = []
            
            elif curdate == []:
                curdate = ['NONE']
                #shitlist.append(docs_under_research[i])
            
        dcfile.write(f'{docs_under_research[i]}: \n{str(curdate)}\n\n')
        dates_list += curdate

        curabout = re.search(r'\w+\s\w+', beginnings_list[i])
        if curabout is not None:
            if 'отказе' in curabout[0]:
                topics_list.append('об отказе')
            elif 'прекращении' in curabout[0]:
                topics_list.append('о прекращении производства')
            elif 'делу' in curabout[0]:
                topics_list.append('по делу')
            elif 'индивидуальной' in curabout[0] or 'жалобе' in curabout[0]:
                topics_list.append('по жалобе')
            elif 'индивидуальным' in curabout[0]:
                topics_list.append('по жалобам')
            elif 'официальном' in curabout[0]:
                topics_list.append('о разъяснении')
            elif 'город' in curabout[0] or '199' in curabout[0]:
                topics_list.append('NONE')
            else:
                topics_list.append(curabout[0])
#print(len(dates_list))   
#print(dates_list)
#print(shitlist)
for i in range(len(dates_list)):
    if dates_list[i] != '':
        dates_list[i] = re.sub(r' *года? *', r'', dates_list[i])
        dates_list[i] = re.sub(r'от', r'', dates_list[i])
        dates_list[i] = re.sub(r' *', '', dates_list[i])
        dates_list[i] = re.sub(r'["“”]', r'', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)^(?=[1-9][а-я])', r'0', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)январ[яь]', r'.01.', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)феврал[яь]', r'.02.', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)марта?', r'.03.', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)апрел[яь]', r'.04.', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)ма[яй]', r'.05.', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)июн[яь]', r'.06.', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)июл[яь]', r'.07.', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)августа?', r'.08.', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)сентябр[яь]', r'.09.', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)октябр[яь]', r'.10.', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)ноябр[яь]', r'.11.', dates_list[i])
        dates_list[i] = re.sub(r'(?iu)декабр[яь]', r'.12.', dates_list[i])
#with open('formatted_dates.txt', 'w', encoding='utf-8') as datefile:
    #datefile.write(str(dates_list))
print(cl.Counter(topics_list))
#print(docs_under_research[959])
#print(dates_list[docs_under_research.index('Decision files\\КСРФ_11-О_1995.txt')])

datedict = {}
for i in range(len(dates_list)):
    datedict.update({headers_true_names[i]: dates_list[i]})
#print(datedict)
with open('DatesCheck.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(datedict, jsonfile, ensure_ascii=False)
'''
4. Выделение типа и номера документа из заголовка
'''
numbers_list = []
forms_list = []
for doc in docs_under_research:
    numbers_list += re.findall(r'(?<=КСРФ_).+?(?=\-)', doc)
    forms_list += re.findall(r'(?<=\d-)[А-Я-]+(?=[._])', doc)
#print(len(numbers_list))
#print(len(forms_list))
resolutions_list = []
endings_list = []
'''
5. Выделение резолютивной части и окончания документа с подписями судей
'''
print('Invalid files are: ')
with open('resolutions_list.txt', 'w+', encoding='utf-8') as resfile:
    for i in range(docnumber):
            with open(docs_under_research[i], 'r+', encoding='utf-8') as docfile:
                text = docfile.read()
                text = re.sub(r'(?<!от )\b[0-9][0-9]?\s', r'', text)
                body = bodypart.search(text)
                opinion = (re.search(r'(?iu)(?:особое *| *)'
                                    r'мнение\s+судьи\s+конституционного', text))
                if body is not None:
                    if opinion is not None:
                        resolutions_list.append((reso.search
                         (text, pos=body.end(), endpos=opinion.start())[0]))
                        #print(docs_under_research[i])
                    else:
                        resolutions_list.append(reso.search(text, pos=body.end())[0])
                    if before_ending.search(resolutions_list[i]) is not None:
                        (endings_list.append(anything.search(resolutions_list[i],
                          pos=before_ending.search(resolutions_list[i]).end())[0]))
                        resolutions_list[i] = before_ending.search(resolutions_list[i])[0]
                        
                    else:
                        endings_list.append(resolutions_list[i])
                elif re.search(r'определил', text) is not None:
                    resolutions_list.append(re.search(r'(?<=определил ).*', text)[0])
                    #print(docs_under_research[i])
                    #эта проверка на самом деле нафиг не нужна
                    if before_ending.search(resolutions_list[i]) is not None:    
                        (endings_list.append(anything.search(resolutions_list[i], 
                          pos=before_ending.search(resolutions_list[i]).end())[0]))
                        resolutions_list[i] = before_ending.search(resolutions_list[i])[0]
                        
                else:
                    resolutions_list.append('NONE')
                    endings_list.append('NONE')
                    print(f'{docfile.name}')
                    #if len(resolutions_list[i]) > 1:
                    #resolutions_list[i] = resolutions_list[i][:-1]
                
                resfile.write(f'{str(resolutions_list[i])}\n')            
normal_endings_list = []
with open('endings_list.txt', 'w+', encoding='utf-8') as endings_file:
    for ending in endings_list:
    #print(ending)
    #ending = re.sub(r'\b[0-9][0-9]?\s', r'', ending)
        
        normal_ending = re.sub(r'.*(?=Председатель)', r'', ending)
        normal_ending = re.sub(r'.*(?=Конституционный)', r'', normal_ending)
        normal_ending = re.sub(r'.*\.   (?=З)', r'', normal_ending)
        normal_ending = re.sub(r'[№N ] *\d+.*', r'', normal_ending)
        normal_ending = re.sub(r'(?<=[А-Я])\.\s', r'.', normal_ending)
        normal_endings_list.append(normal_ending)
        endings_file.write(f'{normal_ending}\n')
#print(normal_endings_list)
'''
6. Исследование частот ссылок в резолютивной части и в начале решения
'''
list_of_links_in_resolutions = []
list_of_links_in_beginnings = []
percentage_resolutions_list = []
percentage_beginnings_list = []

with open('links_in_beginnings.txt', 'w+', encoding='utf-8') as links_file:
    for i in range(docnumber):
        #print(resolutions_list[i])
        curbeglist = simple_link.findall(beginnings_list[i])
        with open(docs_under_research[i], 'r+', encoding='utf-8') as docfile:
            text = docfile.read()
            curwholelist = simple_link.findall(text)
        if curwholelist != []:
            #print(f'{docs_under_research[i]}:\n{curlist}')
            links_file.write((f'{docs_under_research[i]}:\n{str(curbeglist)}\n'
                             f'{len(curbeglist)/len(curwholelist)}\n'))
            percentage_beginnings_list.append(len(curbeglist)/len(curwholelist))
            list_of_links_in_beginnings += curbeglist
with open('links_in_resolutions.txt', 'w+', encoding='utf-8') as links_file:
    for i in range(docnumber):
        #print(resolutions_list[i])
        curreslist = simple_link.findall(resolutions_list[i])
        with open(docs_under_research[i], 'r+', encoding='utf-8') as docfile:
            text = docfile.read()
            curwholelist = simple_link.findall(text)
        if curwholelist != []:
            #print(f'{docs_under_research[i]}:\n{curlist}')
            links_file.write((f'{docs_under_research[i]}:\n{str(curreslist)}\n'
                             f'{len(curreslist)/len(curwholelist)}\n'))
            percentage_resolutions_list.append(len(curreslist)/len(curwholelist))
            list_of_links_in_resolutions += curreslist
'''
7. Поиск судей в концовках документов
'''
all_judges_list = []
main_judges_list = []
numbers_of_judges_list = []
all_judges_tuple_list = []
for nending in normal_endings_list:
    curjudgelist = judge.findall(nending)
    if len(curjudgelist):
        main_judges_list.append(curjudgelist[0])
    else:
        main_judges_list.append('NONE')
    all_judges_list += curjudgelist
    all_judges_tuple_list.append(tuple(curjudgelist))
    numbers_of_judges_list.append(len(curjudgelist))
'''
==============================
Вывод статистики
==============================
'''
with open('links_positions_stats.txt', 'w+', encoding='utf-8') as statsfile:
    (statsfile.write(f'Наиболее часто встречающиеся ссылки в резолютивной части:\n'
                    f'{cl.Counter(list_of_links_in_resolutions).most_common(10)}\n'))
    #statsfile.write(f'{max(percentage_resolutions_list)}\n')
    (statsfile.write(f'Число документов, в которых ссылки только в резолютивной части:\n'
                     f'{sum(np.array(percentage_resolutions_list) == 1)}\n'))
    (statsfile.write(f'Средняя доля ссылок, расположенных в резолютивной части:\n'
                     f'{np.mean(percentage_resolutions_list)}\n'))
    (statsfile.write(f'Наиболее часто встречающиеся ссылки в начале документа:\n'
                     f'{cl.Counter(list_of_links_in_beginnings).most_common(10)}\n'))
    #statsfile.write(f'{max(percentage_beginnings_list)}\n')
    (statsfile.write(f'Число документов, в которых ссылки только в резолютивной части:\n'
                     f'{sum(np.array(percentage_beginnings_list) == 1)}\n'))
    (statsfile.write(f'Средняя доля ссылок, расположенных в резолютивной части:\n'
                     f'{np.mean(percentage_beginnings_list)}\n'))
    (statsfile.write(f'Наиболее часто встречающиеся судьи:\n'
                     f'{cl.Counter(all_judges_list).most_common(10)}\n'))
    (statsfile.write(f'Наиболее часто встречающиеся судебные составы:\n'
                     f'{cl.Counter(all_judges_tuple_list).most_common(20)}\n'))
    (statsfile.write(f'Наиболее часто встречающиеся главные судьи:\n'
                     f'{cl.Counter(main_judges_list).most_common(10)}\n'))
    statsfile.write(f'Число судей:\n{cl.Counter(numbers_of_judges_list)}\n')
with open('research_results.txt', 'w+', encoding='utf-8') as out_file:
    for i in range(docnumber):
        (out_file.write('{}\n'.format(KSRF_Solution(headers_true_names[i], forms_list[i],
                                                    beginnings_list[i], topics_list[i],
                                                    dates_list[i], numbers_list[i],
                                                    keywords_list[i],
                                                    all_judges_tuple_list[i],
                                                    main_judges_list[i]))))
        #out_file.write(f'{KSRF_Solution(headers_true_names[i], forms_list[i], beginnings_list[i], }' \
                    #f'{topics_list[i], dates_list[i], numbers_list[i], keywords_list[i], }'\
                    #f'{all_judges_tuple_list[i], main_judges_list[i])}\n')




        

        