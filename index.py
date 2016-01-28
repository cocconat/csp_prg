###this program will create the dictionary, it tokenizes words, stems with
###nltk and then create correlations between texts with sklearn.
from nltk.corpus import stopwords
from nltk import stem
import re,json,os
from pymongo import MongoClient
from lxml import etree
import time

##count how many ads in the documents folders
myPath = '/Users/ale/Documents/university/sistemi_complessi/database/aps-dataset-metadata-2013/'
##open the documents with csv library
class indexer():
    def __init__(self, folders_path):
        self.path=folders_path
        self.language="english"
        self.stemmer=stem.snowball.EnglishStemmer()
        self.index=None
        self.inverse_index=None
        self.db_instance()

#create an instance of mongodb
    def db_instance(self):
        client=MongoClient('localhost', 27017)
        if client.test_database:
            db=client.get_database('dict')
            self.index=db['index']
            self.inverse_index=db['inverse_index']
            #error list it's for those user resulting missing to followers retrieve
        else: raise  

#run over folders and pass each file to index_builder postinglist
    def files_getter(self, path):
        for dirName, subdirList, files in os.walk(path):
            for file_id in files:
                if file_id[0] != '.':
                    yield dirName, file_id
#                self.postinglist (dirName, file_id)


    def detag(self,text):
        while "<span" in text:
            start=text.find("<span")
            end=text.find("</span>")+len("</span>")
            my_xml=text[text.find("<span")+len("<span"):text.find("</span>")]
            my_xml=my_xml.replace(" ","") 
            text=text[:start]+ my_xml.lower()+ text[end:]
        return text

    
#it reads the file and get each field, has to be tuned!
    def file_read(self, dirName, file_id):
        with open(dirName+'/'+file_id,'r') as f:
            json_file=json.load(f)
#id
            metadata['id']   =self.json_file['id']

#title
            metadata['title']=self.title_process(json_file['title']['value'])
###date
            metadata['date'] =self.date_process(json_file['date'])
#pacs
            if json_file.has_key('classificationSchemes'):
                metadata['pacs']=self.json_file['classificationSchemes']['pacs'][0]['id']
        return metadata

    def date_process(self,date):
        my_time=time.strptime(date, "%Y-%m-%d")
        return {"y":my_time.tm_year,"m":my_time.tm_mon, "d":my_time.tm_mday}
 
    def title_process(self,text):
        words=[]
        text=self.detag(text)
        for word in text.split():
            word=word.strip().lower()
            if word not in stopwords.words(self.language) and not word.isdigit():
#                word=self.stemmer.stem(word)
                words.append(word.encode('utf-8'))
            return words


#it reads the the file and does lowercase, stemming, stopword and isdigit

    def postinglist(self,path=self.path):
        words=[]
        for dirName, file_id in files_getter(path):
            metadata=self.file_read(dirName, file_id)
            self.index.insert({"metadata":metadata,\
                                "id":metadata['id']})
    print notags



###miss the part for the inverse index, that is from article:[words],date to word:[dates] or word:[articles]
#it should be done similar to list_union but with database mongod,
#I think db.create_index and find_and_modify methods of pymongo should be used!
###enjoy!


    def list_union(self, big_list, list2):
        j=0
        k=0
        while j < len(big_list) and k < len(list2):
            while (k)<len(list2) and big_list[j]['key'] == list2[k]['key']:
                #print "primo caso "+big_list[j]['key']
                big_list[j]['docs'].__iadd__(list2[k]['docs'])
                k+=1
                while (k)<len(list2) and big_list[j]['key'] == list2[k]['key']:
                    big_list[j]['docs'].__iadd__(list2[k]['docs'])
                    k+=1
                j+=1

            while k< len(list2) and big_list[j]['key']>list2[k]['key']:
                #print "second caso "  +big_list[j]['key'] +list2[k]['key']
                big_list.insert(j,list2[k])
                k+=1
                while k< len(list2) and str(list2[k-1]['key'])==str(list2[k]['key']):
                    big_list[j]['docs'].__iadd__(list2[k]['docs'])
                    k+=1
                j+=1

            while j< len(big_list) and k< len(list2) and big_list[j]['key']<list2[k]['key'] :
                j+=1
                #print "terzo caso "+list2[k]['key']

        while j==len(big_list) and k< len(list2):
            big_list.insert(j,list2[k])
            k+=1
            while (k)<len(list2) and big_list[j]['key'] == list2[k]['key']:
                k+=1
            j+=1

        list2=[]
        return big_list



