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
    return output

  # It will give the entites present in the sentence along with their meaning. 
  def parse(self,sentence) :
    bigrams = self.ngrams(sentence,2)
    trigrams = self.ngrams(sentence,3) 
    entities = {}
    entitiesObj = []
    for gram in bigrams+trigrams :  # consider unigrams as well.
       (temp,id) = self.search(gram)
       if temp and temp not in entities.keys() :
          entities[temp]  = id
    print entities
    for entity,id in entities.iteritems() :
      text = (self.topic(id))[0].get('text', None)
      entitiesObj.append((entity,id,text))
    print entitiesObj
    #return (entity,meaning)
   
  def relation(self) :
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    query = [{'id': None, 'name': None, 'type': '/astronomy/planet'}]
    params = { 'query': json.dumps(query), 'key': self.api_key }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    for planet in response['result']:
      print planet['name']


  def search(self,query) :
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {'query': query,'key': self.api_key}
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    entities = []
    for result in response['result']:
       if result['score'] > 500 :
         #print result['name'] + ' (' + str(result['score']) + ')'
         #print result
         return (result['name'].strip(),result['mid'])
         break
    return (None,None)

  def topic(self,topic_id) :
    service_url = 'https://www.googleapis.com/freebase/v1/topic'
    params = {'key': self.api_key,'filter': 'suggest'}
    url = service_url + topic_id + '?' + urllib.urlencode(params)
    topic = json.loads(urllib.urlopen(url).read())

    for property in topic['property']:
      return topic['property']['/common/topic/notable_for']['values']
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
  
