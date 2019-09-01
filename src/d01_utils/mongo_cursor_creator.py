import pymongo

def mongo_cursor():
    """
    open up a mongo cursor for curly_profiles in the Naturaly_curly_db and query the db for all the signatures and return a list of unique signatures

    Keyword arguments:
    none
    """
    # create cursor
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    curlydb = myclient['Naturaly_Curly_db']
    curly_collection = curlydb['curly_profiles']

    # Access all the unique items and store them to a list
    query_1 = curly_collection.find({})
    test = []
    for x in query_1:
        test.append(x['signature'])

    # This is the number of total unique entire in the database
    unique_sigs = list(set(test))

    return unique_sigs
