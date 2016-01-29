###this program will create the dictionary, it tokenizes words, stems with
###nltk and then create correlations between texts with sklearn.
from nltk.corpus import stopwords
from nltk import stem
import re,csv,os
import json

stem_eng=stem.snowball.EnglishStemmer()

##count how many ads in the documents folders
##open the documents with csv library
#reads the wordset for each doc and does lowercase, stemming, stopword and isdigit
def file_read(path):
    with open(path,'r') as f:
        my_json=json.load(f)
        return my_json
        
def postinglist(path):
    for i in file_read(path):
        for j in k.split():
            word=j.strip().lower()
            if word not in stopwords.words('italian') and not word.isdigit():
                word=stem_ita.stem(word)
                words.append({'key':word.encode('utf-8'), 'docs':[docID]})
    return sorted(words, key=lambda k: k['key'])

#########################################INDEXING ALGORITHM
#algorithm for list merging
def list_union(big_list, list2):
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

'''
#create the postinglist for single document and merge it
for i in range(1,fileslist):
    index=list_union(index,postinglist(i))
    if (i%20)==0: print str(i) +" files indexed"


#save dictionary and postinglist to file with tsv format
with open("index/postings.txt", 'w') as p:
    with open("index/dictionary.tsv", 'w') as d:
        c=[int(0)]
        pwriter=csv.writer(p,delimiter="\t")
        dwriter=csv.writer(d,delimiter="\t")
        for i in index:
            pwriter.writerow(c+i['docs'])
            dwriter.writerow(c+[i['key']])
            c[0]+=1


#populate the dictionary with a list of docs, keeping it in memory
index={}
for i in words:
    print i
    if (index.has_key(i[0])):
        index[stem_ita.stem(i[0])].append(i[1])
    else:
        index[stem_ita.stem(i[0])]=[i[1]]

#######################

#populate a dictionary for the frequence of comparison in all the corpus
#with keys of the previous dict
freq_index={}
for i in index.keys():
    freq_index[i]=len(index[i])
'''
