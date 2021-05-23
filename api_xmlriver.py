import json
import os
import xml.dom.minidom
import xml.etree.cElementTree as ET

import requests

from setting import API_PARAMS, API_URL
import time

def process_node(node, result, oneline_sitelinks_name = 'title'): #приложение яндекс такси
    for child in node.childNodes:
        if child.nodeType!=child.TEXT_NODE:
            if child.nodeName in ['passages', 'faqsnippet']:
                result2 = list()
                for child2 in child.childNodes:
                    if child2.nodeType!=child2.TEXT_NODE and len(child2.childNodes) > 0:
                        result2.append(child2.childNodes[0].nodeValue.replace(u'\xa0', u' '))
                result.update({child.nodeName:result2})
            elif child.nodeName == 'oneline_sitelinks':
                result2 = list()
                for child2 in child.childNodes:
                    for child3 in child2.childNodes:
                        if child3.nodeName == oneline_sitelinks_name:
                            result2.append(child3.childNodes[0].nodeValue)
                result.update({'oneline_sitelinks':result2})
            elif child.nodeName == 'extendedpassage':
                result.update({'extended_passage':True})
            elif child.nodeName in ['url', 'title', 'snippet', 'cachelink'] and len(child.childNodes):
                value = child.childNodes[0].nodeValue
                if value.find('\n\t') != -1: continue
                result.update({child.nodeName:value})
    return result

def process_group(doc, base, oneline_sitelinks_name = 'title'):
    grouping = doc.getElementsByTagName('group')
    zero_position = doc.getElementsByTagName('zeroposition')
    base_group = list()
    base.update({"items":base_group})
    for group in grouping:
        result = {'position':group.getAttribute('id'), 'extended_passage':False}
        process_node(group.getElementsByTagName('doc')[0], result, oneline_sitelinks_name = oneline_sitelinks_name)
        base_group.append(result)
    if zero_position and len(zero_position):
        print(zero_position[0].getElementsByTagName('url')[0].childNodes[0].nodeValue) #.getAttribute('url').nodeValue
        return zero_position[0].getElementsByTagName('url')[0].childNodes[0].nodeValue
    return ''

def process2(path):
    base = dict()
    with open(path, encoding='UTF-8') as f: contents = f.read()
    doc = xml.dom.minidom.parseString(contents)
    doc.normalize()
    url = process_group(doc, base, oneline_sitelinks_name = 'url')
    return base, url

def process(path):
    with open(f'{path}\\result.xml', encoding='UTF-8') as f: contents = f.read()
    base = dict({
        'local_result':False,
        'knowledge_graph':False,
        'applications':False,
        'bottom_ads':0
    })
    doc = xml.dom.minidom.parseString(contents)
    doc.normalize()

    if doc.getElementsByTagName('localresultsplace'): base.update({"local_result":True})
    if doc.getElementsByTagName('applications'): base.update({"applications":True})


    topads = doc.getElementsByTagName('topads')
    if topads and len(topads):
        base.update({"top_ads":len(topads[0].getElementsByTagName('query'))})

    bottom_ads = doc.getElementsByTagName('bottomads')
    if bottom_ads and len(bottom_ads):
        base.update({"bottom_ads":len(bottom_ads[0].getElementsByTagName('query'))})
    
    if doc.getElementsByTagName('knowledge_graph'):
        base.update({"knowledge_graph":True})
    zero_position = doc.getElementsByTagName('zeroposition')
    if zero_position and len(zero_position):
        result = dict()
        base.update({"zero_position":result})
        process_node(zero_position[0], result)
    
    related_guestions = doc.getElementsByTagName('question')
    if related_guestions and len(related_guestions):
        result = dict()
        base.update({"related_guestions":result})
        process_node(related_guestions[0], result)
    
    related_searches = doc.getElementsByTagName('relatedSearches') # query
    if related_searches and len(related_searches):
        result = dict()
        base.update({"related_searches":result})
        process_node(related_searches[0], result)
        

    process_group(doc, base)

    with open(f'{path}\\result.json', "w", encoding='UTF-8') as f:
        f.write(json.dumps(base, indent=4, ensure_ascii=False))

def generation(path, q, filename = 'result'):
    if not os.path.exists(path): os.makedirs(path)
    with open(f"{path}\\{filename}.xml", 'w', encoding='UTF-8') as f: 
        API_PARAMS.update({'query':q})
        while 1:
            result_xml = requests.get(API_URL, params=API_PARAMS, timeout = 300).text
            if result_xml.find('Выполните перезапрос. Ответ от поисковой системы не получен.') != -1:
                time.sleep(1)
                continue
            elif result_xml.find('Нет свободных каналов для сбора данных. Попробуйте позже.') != -1:
                time.sleep(1)
                continue
            break
        dom = xml.dom.minidom.parseString(result_xml) # or xml.dom.minidom.parseString(xml_string)
        result = dom.toprettyxml()
        f.write(result)
    return result


    #editXML('result.xml')
    
