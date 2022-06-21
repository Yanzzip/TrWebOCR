import re
import json

def is_key_words(question):
    '''
    判断是否是关键词
    '''
    
    if '血红蛋白' in question and '平均' not in  question :
        return True , '血红蛋白'
    for valid_str in ['白细胞', '红细胞']:
        if valid_str in question and '平均' not in question  and '数' in question :
            return True , valid_str + '数'
    for valid_str in ['中性粒细胞','淋巴细胞']:
        if valid_str in question and '比'  in  question :
            return True , valid_str + '百分比'
    return False , ''

def del_noise_words(question):
    '''
    删除识别中的噪声词
    '''
    for valid_str in ['l','!','f']:
        if valid_str in question:
            print(question)
            question=question.replace(valid_str, '')
            print(question)
    return question 

def del_noise_list(wordlist):
    '''
    删除列表中的噪声词
    '''
    print(len(wordlist))
    while '' in wordlist:
        wordlist.remove('')
    print(len(wordlist))
    return wordlist

def extract_info(wordlist):
    '''
    从词列表中提取需要的信息
    '''
    del_noise_list(wordlist)
    print(wordlist)
    wpair={}
    wlen = len(wordlist)
    for i in range(wlen):
        isTrue , keyword = is_key_words(wordlist[i])
        if isTrue : 
            npair={}
            print(wordlist[i+1])
            npair['Value']=float(wordlist[i+1])
            
            if('-' in wordlist[i+2] ):
                wordlist[i+2] = del_noise_words(wordlist[i+2])
                LH=wordlist[i+2].split('-')
                print(LH)
                npair['Lvalue']=float(LH[0])
                npair['Hvalue']=float(LH[1])
                if(npair['Value']>npair['Hvalue']):
                     npair['Level']='H'
                elif(npair['Value']<npair['Lvalue']):
                     npair['Level']='L'
                else:
                     npair['Level']='E'
                     
            elif('-' in wordlist[i+3] ):
                wordlist[i+3] = del_noise_words(wordlist[i+3])
                LH=wordlist[i+3].split('-')
                print(LH)
                npair['Lvalue']=float(LH[0])
                npair['Hvalue']=float(LH[1])
                if(npair['Value']>npair['Hvalue']):
                     npair['Level']='H'
                elif(npair['Value']<npair['Lvalue']):
                     npair['Level']='L'
                else:
                     npair['Level']='E'
            wpair[keyword]=npair
                
    return wpair

def extract_json(textlist):
    puretext = []
    for i in textlist:
        puretext.append(i[1])
    return puretext
    