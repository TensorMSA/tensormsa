class ChatKnowledgeMemDict:
    """
    class for storing dict data on the django memory 
    for speed up dict search action 
    """
    # cc_id - entitiy_id -value list
    ngram = {}
    ngram_order = {}
    ngram_conf = {}
    data = {}
    data_conf = {}
    data_order = {} #ordered proper_noun
    synonym = {}
    conf = {}