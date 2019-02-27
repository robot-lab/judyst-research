import web_crawler as wc
import link_analysis as la
import neuronet
import sys
from link_analysis._KsrfParser import KsrfParser
from link_analysis.link_handler import _NnDelPattern, _sentenceSeparator
import os
import json
from time import time
from link_analysis._CodeParsers import _get_next_dec_for_link_checking
sys.path.insert(0, '..\\judyst-main-web-service')
from celery.data import ModelData


SUPERTYPE = 'КСРФ'


def init_wc():
    model = ModelData()
    return wc.DatabaseWrapper("db_source", model)


def get_headers(dataSource):
    with open("headers.json", 'rt', encoding="utf-8") as f:
        analyzingJsonHeaders = json.loads(f.read())
    analyzingDecisionsHeaders = la.converters.convert_to_class_format(
        analyzingJsonHeaders, la.models.Header)
    with open("КС_РФ_DecisionHeaders.json", 'rt', encoding="utf-8") as f:
        fullJsonHeaders = json.loads(f.read())
    fullDecisionsHeaders = la.converters.convert_to_class_format(
        fullJsonHeaders, la.models.Header)
        
    return fullDecisionsHeaders, analyzingDecisionsHeaders


def get_links_by_regex(doc_id, headers, source, parser):
    text = source.get_data(doc_id, wc.DataType.DOCUMENT_TEXT)
    if text is None:
        return []
    sentenceMatchObjects = list(_sentenceSeparator(text))
    parsed = parser.parse(
                    headers[doc_id], sentenceMatchObjects,
                    headers, "КСРФ", None)
    allCleanLinks = {}
    for h in parsed:
        if h in allCleanLinks:
            allCleanLinks[h].extend(parsed[h])
        else:
            allCleanLinks[h] = parsed[h]

    return allCleanLinks


def get_links_by_net(doc_id, network, get_mask, token_vocab, tag_vocab):
    text = source.get_data(doc_id, wc.DataType.DOCUMENT_TEXT)
    if text is None:
        return []
    return neuronet.check_text(text, network, get_mask, token_vocab, tag_vocab)


def regex_test(analyzing_headers, headers, source, parser, out_dict):
    startTime = time()
    for key in analyzing_headers:
        out_dict[key] = get_links_by_regex(key, headers, source,
                                           parser)
    endTime = time()
    return endTime - startTime


def network_test(analyzing_headers, headers, source, nernet, get_mask, token_vocab,
                tag_vocab, out_dict):
    start_time = time()
    for key in analyzing_headers:
        out_dict[key] = get_links_by_net(key, nernet, get_mask,
                                         token_vocab, tag_vocab)
    end_time = time()
    return end_time - start_time
    



def get_average_test_time(test,  iter_count, out_dict, **kwargs):
    sum_time = 0
    for i in range(iter_count):
        sum_time += test(**kwargs, out_dict=out_dict)
    return sum_time / iter_count


class SourceImitator:
    texts = {}

    def __init__(self, *args, **kwargs):
        headers = kwargs["headers"]
        source = kwargs["source"]
        for key in headers:
            self.texts[key] = source.get_data(key, wc.DataType.DOCUMENT_TEXT)

    def get_data(self, key, type):
        return self.texts[key]


if __name__ == "__main__":
    print("Starting...")
    source = init_wc()
    print("Source received. Getting headers")
    full_headers, analyzing_headers = get_headers(source)
    print("Headers received.  Getting parser")
    parser = KsrfParser()
    print("Parser received. Restoring network...")
    model_path = "..\\judyst-research\\model.ckpt"
    data_path = '..\\judyst-research\\data'
    nernet, get_mask, token_vocab, tag_vocab = neuronet.restore(model_path,
                                                                data_path)
    print("network restored. Making source imitator...")
    fake_source = SourceImitator(headers=analyzing_headers, source=source)

    print("Source imitator has maked. Running regex tests...")
    links = {}
    average_time = get_average_test_time(regex_test, 100, links,
                                         headers=full_headers,
                                         analyzing_headers=analyzing_headers,
                                         source=fake_source,
                                         parser=parser)
    links = la.converters.convert_dict_list_cls_to_json_serializable_format(links)
    with open("regex_time.txt", 'wt', encoding="utf-8") as f:
        f.write(f'{average_time}')
    with open("regex_results.json", 'wt', encoding="utf-8") as f:
        f.write(json.dumps(links))
    links = {}
    average_time = get_average_test_time(network_test, 100, links,
                                         headers=full_headers,
                                         analyzing_headers=analyzing_headers,
                                         source=fake_source, nernet=nernet,
                                         get_mask=get_mask,
                                         token_vocab=token_vocab,
                                         tag_vocab=tag_vocab)
    with open("network_time.txt", 'wt', encoding="utf-8") as f:
        f.write(f'{average_time}')
    with open("network_results.json", 'wt', encoding="utf-8") as f:
        f.write(json.dumps(links))
    print("benchmark completed")