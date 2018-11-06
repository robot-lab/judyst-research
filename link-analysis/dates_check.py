import json
import re
with open('Decision files\DecisionHeaders.json', 'r', encoding='utf-8') as fh:
    headersdict = json.load(fh)
with open('DecisionHeaders_dict.txt', 'w', encoding='utf-8') as file:
    file.write(str(headersdict))
researchdict = headersdict
with open('unused_docs.txt', 'r+', encoding='utf-8') as unused_file:
    unused_list = [header.rstrip('\n') for header in unused_file]
for undoc in unused_list:
    undoc = re.sub(r'.*(?=К)', r'', undoc)
    undoc = re.sub(r'\.txt', r'', undoc)
    undoc = re.sub(r'_', r'/', undoc)
for doc in researchdict:
    if doc in unused_list:
        researchdict.pop(doc)
print(len(researchdict))
with open('DatesCheck.json', 'r', encoding='utf-8') as jsonfile:
    datedict = json.load(jsonfile)
#print(datedict)
for doc in datedict:
    if (researchdict[doc]['release_date'] != datedict[doc]):
        print(f"{researchdict[doc]['release_date']}, {datedict[doc]}, {doc}")