#--data_path /Users/suhit-k/MS_PhD_Admission/Law_AI/DELSumm/docs --prep_path ./out
#!/usr/bin/python3

# This program take input as base dir and scan all files inside dir 
# convert the text files in json structure and copy in prep_path dir.
import argparse

import sys, os
import nltk
import json

parser = argparse.ArgumentParser() # used to take pogram input argument
parser.add_argument('--data_path', type = str, help = 'Folder containing documents to be summarized')
parser.add_argument('--prep_path',  type = str, help = 'Path to store the prepared data in json format')


args = parser.parse_args()  # separate out arguments 

BASEPATH = args.data_path 
writepath = args.prep_path


separator = "\t" # kept tab as separator

FILES = []
FILES2 = os.listdir(BASEPATH)  # get list  of all files inside base dir. 
for f in FILES2:
        FILES.append(f) # copy name of file in array FILES
DATA_FILES = {}
for F in FILES:
    ifname = os.path.join(BASEPATH,F) # create absolete path for every file
    
    #print(F)
    fp = open(ifname,'r') # open file for read mode
    dic = {}
    for l in fp: # for every line in file
        try:
            wl = l.split(separator) #line contains word which came in wl array
            CL = wl[1].strip(' \t\n\r') #stripped of any leading or trailing whitespace
            TEXT = wl[0].strip(' \t\n\r') #stripped of any leading or trailing whitespace
            TEXT = TEXT.replace("sino noindex makedatabase footer start url", "")
            if TEXT: # below code will add one by one word in dic
                if dic.__contains__(CL)==True:
                    temp = dic[CL]
                    temp.append(TEXT)
                    dic[CL] = temp
                else:
                    dic[CL] = [TEXT]
        except Exception as e:
            print(e)
    
    f_d = {}
    for cl,sentences in dic.items():
        temp = []
        for s in sentences:
            tokens = nltk.word_tokenize(s)  # tokenize everything 
            t = (s,tokens,nltk.pos_tag(tokens)) #tagging of every word based on its verb, noun etc.
            temp.append(t) 
        f_d[cl] = temp

    DATA_FILES[F.split('.txt')[0].strip(' \t\n\r')] = f_d
    print('Complete {}'.format(F))

with open(writepath+'prepared_data.json','w') as legal_f: # write as json in specified location
    json.dump(DATA_FILES,legal_f,indent=4)
