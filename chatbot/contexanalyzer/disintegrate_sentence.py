#CoNLL-U Format
#http://universaldependencies.org/docs/format.html
#https://cs.nyu.edu/grishman/jet/guide/PennPOS.html

def disintegrate_sentence(sentence):
    sentence_temp=sentence

    return None

def sentence_to_vector(sentence):
    sentence_temp=sentence
    return None

def getUpostagStr(pos):
    tagDic = dict()
    tagDic['NNG'] = 'NOUN'
    tagDic['VV'] = 'VERB'
    tagDic['MM'] = 'DET'
    tagDic['SF'] = 'PUNCT'
    if pos in tagDic.keys():
        return tagDic[pos]
    else :
        return pos