import requests,json

import json
import urllib


class SemanticBase() :
  def __init__(self) :
     self.api_key = open(".freebase_api_key").read()

  def ngrams(self,input, n):
    input = input.split(' ')
    output = []
    for i in range(len(input)-n+1):
      output.append(input[i:i+n])
    print output
    return output

  # It will give the entites present in the sentence. 
  def parse(self,sentence) :
    bigrams = self.ngrams(sentence,2)
    trigrams = self.ngrams(sentence,3)
    entities = []
    for gram in bigrams+trigrams :
       temp = self.search(" ".join(gram))
       for entity in temp  :
         if entity not in entities :   
           entities.append(entity)
    print entities

  def search(self,query) :
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {'query': query,'key': self.api_key}
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    entities = []
    for result in response['result']:
       if result['score'] > 500 :
         print result['name'] + ' (' + str(result['score']) + ')'
         entities.append(result['name'].strip())
         print result
         break
    return entities

  def topic(self,topic_id) :
    service_url = 'https://www.googleapis.com/freebase/v1/topic'
    params = {'key': self.api_key,'filter': 'suggest'}
    url = service_url + topic_id + '?' + urllib.urlencode(params)
    topic = json.loads(urllib.urlopen(url).read())

    for property in topic['property']:
      print property + ':'
      for value in topic['property'][property]['values']:
        print ' - ' + value['text']
  

if __name__ == "__main__" :
  sem = SemanticBase()
  sentence = "Deepika Padukone portrays the titular protagonist, a Bengali architect living in New Delhi, and Amitabh Bachchan plays her hypochondriac father."
  #sem.ngrams(sentence,2)
  #sem.search("Deepika Padukone")
  #sem.topic("/m/02hrh1q")
  sem.parse(sentence)
  
