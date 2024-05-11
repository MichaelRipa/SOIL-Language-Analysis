# /usr/bin/env python3

import os
import re
import epitran
from nltk import sent_tokenize

epi = epitran.Epitran('deu-Latn')

def clean_sents_pipeline():
    for filename in os.listdir():
        if 'raw_paz' in filename:
            f = open(filename,'r')
            raw = f.read()
            f.close()
            sents = filter_sents(sent_tokenize(clean_pdf(raw),'german'))
            new_filename = re.sub('raw','clean',filename)
            f_new = open(new_filename,'w')
            for s in sents:
                f_new.write(s + '\n')
            f_new.close()                
            print(new_filename + ' finished!')
    
def _open_cleaned_sents():
    sents = []
    for filename in os.listdir():
        if 'clean_paz' in filename:
            f = open(filename,'r')
            raw = f.read()
            sents += raw.split('\n')
            f.close()
    return sents
         
def ipa_sents_pipeline():
    for filename in os.listdir():
        if 'clean_paz' in filename:
            f = open(filename,'r')
            raw = f.read()
            f.close()
            sents = raw.split('\n')
            ipa_sents = [epi.transliterate(s) for s in sents]
            new_filename = re.sub('clean','ipa',filename)
            f_new = open(new_filename,'w')
            for s in ipa_sents:
                f_new.write(s + '\n')
            f_new.close()                
            print(new_filename + ' finished!')
    

def _second_filter_pipeline():
    for filename in os.listdir():
        if 'clean_paz' or 'ipa_paz' in filename:
            f = open(filename,'r')
            raw = f.read()
            f.close()
            sents = raw.split('\n')
            f_new = open(filename,'w')
            for s in sents:
                if len(s.split(' ')) > 4:
                    if re.findall('([0-9] ){3,}',s) == []:
                        f_new.write(s + '\n')
            f_new.close()                
            print(filename + ' finished!')
    
    print('Done!')

def get_all_data(ipa=True):
    all_data = ''
    if ipa:
        for cur_file in os.listdir():
            if 'ipa' in cur_file:
                f = open(cur_file,'r',encoding='utf-8')        
                all_data += re.sub('\n',' ',f.read())
                f.close()
    return all_data                
