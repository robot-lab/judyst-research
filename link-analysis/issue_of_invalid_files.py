import re
import collections as cl

with open('headers_names.txt', 'r+', encoding='utf-8') as headers:
    headers_list = [h.rstrip('\n') for h in headers]
with open('headers_names.txt', 'r+', encoding='utf-8') as headers:
    numbers_list = re.findall(r'(?<=КСРФ_).+(?=\-)', headers.read())
with open('unused_docs.txt', 'r+', encoding='utf-8') as unused:
    unused_list = [u.rstrip('\n') for u in unused]
'''
print(headers_list)
print(unused_list)
'''
wrong_endings_list = []
#здесь была проверка на одну из опечаток
'''
print(headers_list.index('Decision files\\КСРФ_П-Р3-1_1992.txt'))
print(numbers_list[31049])
'''
'''
wrong_endings.txt - четыре файла: три с грубыми опечатками
и один битый.
'''
with open('wrong_endings.txt', 'w', encoding='utf-8') as endings_file:
    for i in range(len(headers_list)):
        with open(headers_list[i], 'r+', encoding='utf-8') as current_doc:
            text = current_doc.read()
            '''
            рабочая регулярка: в конце либо номер этого решения,
            либо инициалы судьи, либо инициалы и номер страницы
            '''
            if (re.findall(r'(?ui)(?:(?:№|N| ) *' + numbers_list[i] +
                r'\s*?|\w\.\w\. ?\w+\s+\d?\s*$)', text) == []):
               #if (re.findall(r'[Мм]нение ', text) == [] and 
               #    headers_list[i] not in unused_list):
               if headers_list[i] not in unused_list:
                   endings_file.write(f'{headers_list[i]}\n')
                   wrong_endings_list.append(headers_list[i])
                   #print(i) 
print(wrong_endings_list)                   
'''
В strange_endings.txt хранятся заголовки всех документов, которые
не содержат своего номера в конце текста. Кроме кривых файлов
из wrong-endings.txt, это около 600 решений 2006 года 
и одно решение 2013 года.
pages_number_in_the_end.txt - список заголовков документов, у которых 
номер страницы попал в конец текста после инициалов судьи.
'''

with open('strange_endings.txt', 'w', encoding='utf-8') as endings_file:
    for i in range(len(headers_list)):
        with open(headers_list[i], 'r+', encoding='utf-8') as current_doc:
            text = current_doc.read()
            if (re.findall(r'(?ui)(?:(?:№|N| ) *' + numbers_list[i] +
                r'\s*?)', text) == []):
                '''
                Здесь была проверка на то, в каких случаях
                в тексте документа может встречаться его номер
                более одного раза. Невалидного поведения
                не обнаружено.
                '''
               #if (re.findall(r'[Мм]нение ', text) == [] and 
               #    headers_list[i] not in unused_list):
                if headers_list[i] not in unused_list:
                   endings_file.write(f'{headers_list[i]}\n')
                   #print(i) 

with open('strange_endings.txt', 'r+', encoding='utf-8') as remainder_file:
    remainder_list = [h.rstrip('\n') for h in remainder_file]
with open('pages_number_in_the_end.txt', 'w', encoding='utf-8') as endings_file:
    for doc in remainder_list:
         with open(doc, 'r+', encoding='utf-8') as curdoc:
            text = curdoc.read()
            if (re.findall(r'\w\.\w\. ?\w+\s+\s*$', text) == [] 
               and doc not in wrong_endings_list):
                endings_file.write(f'{doc}\n')

