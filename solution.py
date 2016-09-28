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
    #print entities
    for entity,id in entities.iteritems() :
      if self.topic(id) :
        text = (self.topic(id))[0].get('text', None)
        print entity, text
        entitiesObj.append((entity,id,text))
    #print entitiesObj
    #return (entity,meaning)
    return entitiesObj

  def relation(self, q1, q2 ) :
    try:
      d1 = self.search(q1,complete = True)
      if d1.get('notable',None) :
        notable1 = d1.get('notable').get('name',None)
      d2 = self.search(q2,complete = True)
      if d2.get('notable',None) :
        notable2 = d2.get('notable').get('name',None)
      if notable1 == notable2 :
        print "q1 and q2 are %s" %(notable1)
        return      
    except Exception,e:
      print e
      print "Failed to find a relation"
    print "No relation between %s %s" %(q1,q2)


  def search(self,query,complete = False) :
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {'query': query,'key': self.api_key}
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    entities = []
    for result in response['result']:
       #if result['score'] > 500 :
       #  print result
       if complete :
          return result
       return (result['name'].strip(),result['mid'])
 
    if complete :
       return None 
    return (None,None)

  def topic(self,topic_id) :
    service_url = 'https://www.googleapis.com/freebase/v1/topic'
    params = {'key': self.api_key,'filter': 'suggest'}
    url = service_url + topic_id + '?' + urllib.urlencode(params)
    topic = json.loads(urllib.urlopen(url).read())

    for property in topic['property']:
      if topic['property'].get('/common/topic/notable_for',None) :
        return topic['property']['/common/topic/notable_for']['values']
      else :
        return None
      print property + ':'
      for value in topic['property'][property]['values']:
        print ' - ' + value['text']
 
  def readTweets(self) :
    import MySQLdb

    db = MySQLdb.connect("localhost","root","toor","twitter" )
    cursor = db.cursor()
    tweets = []
    try:
      cursor.execute("SELECT * from tweets")
      for x in cursor :
        (id,text,timestamp) = x
        tweets.append(x)
        print text
      db.commit()
    except:
      pass
      db.rollback()
    db.close()
    return tweets

  def process(self) :
    tweets = self.readTweets()
    for tweet in tweets :
      id,text,timestamp = tweet
      text = "Deepika Padukone portrays the titular protagonist, a Bengali architect living in New Delhi, and Amitabh Bachchan plays her hypochondriac father."
      print self.parse(text)
      break
      
  

if __name__ == "__main__" :
  sem = SemanticBase()
  sentence = "Deepika Padukone portrays the titular protagonist, a Bengali architect living in New Delhi, and Amitabh Bachchan plays her hypochondriac father."
  #sem.ngrams(sentence,2)
  #print sem.search("Deepika Padukone", complete = True)
  #print sem.search("Yuvraj Singh")
  #sem.topic("/m/028lkr") # /m/028lkr #/m/02hrh1q
  sem.parse(sentence)
  #sem.relation("Yuvraj Singh", "Sachin Tendulkar")
  #sem.readTweets() 
  #sem.process()
