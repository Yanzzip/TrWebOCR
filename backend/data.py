import re
import json

def is_key_words(question):
    '''
    判断
    '''
    
    if '血红蛋白' in question and '平均' not in  question :
        return True , '血红蛋白'
    for valid_str in ['白细胞', '红细胞']:
        if valid_str in question and '平均' not in question and '压' not in question and len(question) <= 8  :
            return True , valid_str + '数'
    if  '中性' in question and '比' in  question :
         return True , '中性粒细胞百分比'
    if  '中性' in question and '%' in  question :
         return True , '中性粒细胞百分比'
    if  '淋巴' in question and '比' in  question :
        return True , '淋巴细胞百分比'
    if  '淋巴' in question and '%' in  question :
        return True , '淋巴细胞百分比'

    return False , ''

def is_key_words_order(question):
    '''
    判断
    '''
    
    if 'WBC' in question :
        return True , '白细胞数量'
    for valid_str in ['NEUT%','GRAN%']:
        if valid_str in question  :
            return True , '中性粒细胞百分比'
    for valid_str in ['LYM%','LYMPH%']:
        if valid_str in question  :
            return True , '淋巴细胞百分比'
    if 'RBC' in question :
        return True , '红细胞数量'
    if 'HGB' in question :
        return True , '血红蛋白'
    
    return False , ''


def del_noise_words(question):
    '''
    删除识别中的噪声词
    '''
    for valid_str in ['l','!','f','%','|','忄']:
        if valid_str in question:
            print(question)
            question=question.replace(valid_str, '')
            print(question)
    return question 

def del_range_noise_words(question):
    '''
    删除范围识别中的噪声词
    '''
    
    question = question.replace('=','-')
    question = question.replace('~','-')
    question = question.replace('~ ','-')
    question = question.replace('- ','-')
    question = question.replace('L',' ')
    if ' ' in question:
        List =question.split(' ')
        for i in List:
            if '-' in i:
                return i
    
    return question 

def del_noise_list(wordlist):
    '''
    删除列表中的噪声词
    '''
    print(len(wordlist))
    while '' in wordlist:
        wordlist.remove('')
    while ' ' in wordlist:
        wordlist.remove(' ')
    while '忄' in wordlist:
        wordlist.remove('忄')
    while 'f' in wordlist:
        wordlist.remove('f')
    while '!' in wordlist:
        wordlist.remove('!')
    while 'l' in wordlist:
        wordlist.remove('l')
    while '|' in wordlist:
        wordlist.remove('|')    
    print(len(wordlist))
    return wordlist

def determine_order(wordlist):
    '''
    判断英文缩写与项目名称的顺序
    '''
    wlen = len(wordlist)
    for i in range(wlen-1):
        if '白细胞' in wordlist[i] and 'WBC' in wordlist[i+1]:
            return True
    return False



def extarct_info(wordlist):
    '''
    判断问题是否是关于手术费用
    '''
    del_noise_list(wordlist)
    print(wordlist)
    wpair={}
    wlen = len(wordlist)
    isOrder = determine_order(wordlist)
    print(isOrder)
    for i in range(wlen):
        if isOrder:
            isTrue , keyword = is_key_words_order(wordlist[i])
            print('isO')
        else: 
            isTrue , keyword = is_key_words(wordlist[i])
        if isTrue : 
            npair={}
            print(wordlist[i])
            print(wordlist[i+1])
            npair['Value']=float(del_noise_words(wordlist[i+1]))            
            if('-' in wordlist[i+2] or '~' in wordlist[i+2] ):
                wordlist[i+2] = del_noise_words(wordlist[i+2])
                print( wordlist[i+2])
                LH=del_range_noise_words(wordlist[i+2]).split('-')
                while '' in LH:
                    LH.remove('')
                print(LH)
                npair['Lvalue']=float(LH[0])
                npair['Hvalue']=float(LH[1])
                if(npair['Value']>npair['Hvalue']):
                     npair['Level']='H'
                elif(npair['Value']<npair['Lvalue']):
                     npair['Level']='L'
                else:
                     npair['Level']='E'
                     
            elif('-' in wordlist[i+3] or '~' in wordlist[i+3] ):
                wordlist[i+3] = del_noise_words(wordlist[i+3])
                LH=del_range_noise_words(wordlist[i+3]).split('-')
                while '' in LH:
                    LH.remove('')
                npair['Lvalue']=float(LH[0])
                print(LH[1])
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
    