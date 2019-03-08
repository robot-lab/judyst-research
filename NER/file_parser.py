import json
import re
import numpy as np


def repl(m):
    symb = m.group(0)
    if re.match(r'[^\s-]', symb):
        return' ' + symb + ' '
    else:
        return symb

def groupEqualElements(array):
    groups = dict()
    if len(array) > 1:
        unique, indices = np.unique(array,True,axis=0)
        if len(unique) > 1:
            for i in indices:
                groups.update({i: np.array([], dtype=int)})
            for j in range(len(array)):
                for i in indices:
                    if np.array_equal(array[j], array[i]):
                        groups.update({i:np.append(groups.get(i),j)})
        else:
            groups.update({0: np.array([i for i in range(len(array))], dtype=int)})
    else:
        groups.update({0: np.array([0], dtype=int)})
    return groups

def loadData():
    # len(sourceData)=16483
    sourceData = []
    with open("C:\\Users\\stron\\PycharmProjects\\word2vec\\cleanLinks.jsonlines",encoding='utf-8') as f:
        dic = dict(json.loads(f.readline(),encoding='utf-8'))
        sourceData.append(dic)
        current = 0
        for jsonline in f.readlines():
            line = dict(json.loads(jsonline))
            if line['doc_id_from'] == sourceData[current]['doc_id_from']:
                sourceData[current]['positions_list'].extend(line['positions_list'])
            else:
                current = current+1
                sourceData.append(line)
        with open("C:\\Users\\stron\\PycharmProjects\\word2vec\\sourceData.txt", 'w', encoding='utf-8') as fileWriter:
            fileWriter.writelines(json.dumps(source) for source in sourceData)
    return sourceData



def formDataset(filename, sourceData):
    print("formDataset started")
    data=[]
    if filename=="train":
        data=sourceData[0:(len(sourceData)*4)//5]
    if filename=="test":
        data=sourceData[(len(sourceData)*4)//5:(len(sourceData)*4)//5+len(sourceData)//10]
    if filename=="valid":
        data=sourceData[(len(sourceData)*4)//5+len(sourceData)//10:len(sourceData)]

    with open(filename+".txt",'w',encoding='utf-8') as writeFile:
        writeFile.write("-DOCSTART- O\n")
        for k in range(len(data)):
            print("k=",k)
            with open('Decision_files/'+('_').join(data[k]["doc_id_from"].split('/'))+'.txt',encoding='utf8') as file:
                for line in file:
                    line_array=list(line)
                    positions=data[k]['positions_list']
                    contextes = np.zeros((len(positions),2),dtype=int)
                    referencies = np.zeros(len(positions),dtype='<U1000')
                    for j in range(len(positions)):
                        contextes[j]=np.array([ positions[j]['context_start'],positions[j]['context_end']])
                        referencies[j]=u""+("").join((line_array[positions[j]['link_start']:positions[j]['link_end']]))
                    groups = groupEqualElements(contextes)
                    for groupIndices in groups.values():
                        context = u""+('').join(line_array[positions[groupIndices[0]]['context_start']:positions[groupIndices[0]]['context_end']])
                        unsplittedContext = re.sub(r'[^a-яА-ЯёЁ0-9]', repl, context)
                        tokens = unsplittedContext.split()
                        tags = ['O' for _ in range(len(tokens))]
                        for ref in np.take(referencies,groupIndices,axis=0):
                            ref = ref.split()
                            indices = [x for x in range(len(tokens)) if tokens[x:x + len(ref)] == ref]
                            if len(indices)== 1:
                                tags[indices[0]]='B-REF'
                                tags[indices[0]+1:indices[0] + len(ref)] = ['I-REF' for _ in range(len(ref)-1)]
                        for token, tag in zip(tokens, tags):
                            writeFile.write(token + " : " + tag+"\n")
                        writeFile.write("\n")
    print("formDataset ended")



