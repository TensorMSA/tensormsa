class ChatKnowledgeMemDict:
    """
    class for storing dict data on the django memory 
    for speed up dict search action 
    """
    # cc_id - entitiy_id -value list
    data = {}
    ngram = {}
    synonym = {}
    data_order = {}