import pymongo
from pymongo import Connection
import error
import urllib2
import json
import classes
import time
import os
from random import randrange
from dateutil.parser import parse
import time
from dateutil import tz



config = classes.config()

def connect():
    i = 0
    #while True:
    while i < config.max_fetch_attempts:
        try:
            db_connection = Connection(config.db_host, config.db_port)
            global db
            db = db_connection[config.db_name]
            if config.auth:
                db.authenticate(config.db_user, config.db_passwd)
                
            break

        except Exception, e:
            error.log_debug(e, 1, config)
            time.sleep(2)
            i += 1


def create_index():
    try:
        collection_blog = db[config.db_table_blog]
        collection_post = db[config.db_table_post]
        collection_comment = db[config.db_table_comment]
                
        collection_blog.ensure_index(config.blog_uni_key, background=True)
        collection_post.ensure_index(config.post_uni_key, background=True)
        collection_comment.ensure_index(config.comment_uni_key, background=True)
        
    except Exception, e:
        error.log_debug(e, 1, config)
        error.log_debug('Error in creating index', 1, config)
        return False


def assign_thread():
    try:
        collection = db[config.db_table_blog]        
        
        blogs = collection.find({'thread_id':config.thread_id_newcomer})
        
        for item in blogs:
            thread_id = randrange(0, config.max_thread)
            item['thread_id'] = thread_id
            collection.update({'URL':item['URL']}, item)
            
    except Exception, e:
        error.log_debug(e, 1, config)
        error.log_debug('Error in assigning thread', 1, config)


def update_thread(blogname):
    url = 'http://' + blogname    
    try:
        collection = db[config.db_table_blog]        
        collection.update({'URL':url},{"$set": {'thread_id':config.thread_id_done}})
        
    except Exception, e:
        error.log_debug(e, 1, config)
        error.log_debug('Error in updating thread', 1, config)


def fetch(query, config):    
    try:
        data = urllib2.urlopen(query).read()        
        jsondata = json.loads(data)
                
        return jsondata
        
    except Exception, e:
        error.log_debug(e, 1, config)
        error.log_debug('Error in fetching from ' + query, 1, config)
        return {}


def store(data, type, config):    
    try:
        if type == "blog":            
            collection = db[config.db_table_blog]                                        
            collection.update({'URL':data['URL']}, {"$set":data}, True, safe=True)            
                
        elif type == "post":            
            collection = db[config.db_table_post]            
            collection.insert(data, safe=True)            
            
        elif type == "comment":
            collection = db[config.db_table_comment]            
            collection.insert(data, safe=True)            
                            
        return True
            
            
    except Exception, e:            
        #connect()
        error.log_debug(e, 1, config)
        error.log_debug('Error in storing ' + type + ', ID:' + str(data['ID']), 1, config)
                                
        e = str(e)
        
        if type == 'post' and ( e.find("'.'") != -1 or e.find("'$'") != -1 ):               # removing dot('.') and dollar('$') from key
            #key = e.split("\'")[1]
            error.log_debug('Trying to replace "." or "$" with "_" in key and reinsert' + ', ID:' + str(data['ID']), 1, config)                        
            if remove_dot_and_dollar_from_key(data, config):
                return True

        
    return False



def remove_dot_and_dollar_from_key(data, config):
    try:                
        for key in ['tags', 'categories', 'attachments']:
            for k in data[key].keys():
                if k.find(".")!=-1 or k.find("$")!=-1:
                    temp = data[key][k]
                    old_key = k
                    new_key = old_key.replace('.', '_')
                    new_key = new_key.replace('$', '_')
                    del data[key][old_key]
                    data[key][new_key] = temp                    
                            
        collection = db[config.db_table_post]            
        collection.insert(data, safe=True)        
        
        return True
    
    except Exception, e:                    
        error.log_debug(e, 1, config)
        error.log_debug('Error in removing dot from key, ID:' + str(data['ID']), 1, config)
        
    return False



def is_found(id, blogname, type):    
    for i in range(0,config.max_fetch_attempts):
        try:
            if type == "blog":
                blog_url = 'http://' + blogname
                collection = db[config.db_table_blog]
                res = collection.find_one({'URL':blog_url}, timeout=False)
                
            elif type == "post":
                blog_url = 'http://' + blogname
                collection = db[config.db_table_post]                
                res = collection.find_one({'ID':id, 'blog_URL':blog_url}, timeout=False)                        # newly added
            
            if res is None:
                return False
            else:
                return True
            
        except Exception, e:            
            error.log_debug(e, 1, config)
            error.log_debug('Error in is_found ' + type + ', try again', 1, config)
        
    return False




def get_last_update_unix(blogname):    
    for i in range(0,config.max_fetch_attempts):
        try:
            URL = 'http://' + blogname            
            collection = db[config.db_table_blog]                            
            res = collection.find_one({'URL':URL}, {'last_update_unix':1, '_id':0}, timeout=False)
            return res                            
            
        except Exception, e:            
            error.log_debug(e, 1, config)
            error.log_debug('Error in get_last_update_unix ' + ', try again', 1, config)
        
    return {}



def get_blogsites(thread_id):
    try:
        collection = db[config.db_table_blog]
        if thread_id >= 0:
            return collection.find({'thread_id':thread_id}, {'URL':1, '_id':0}, timeout=False)
        else:
            return {}
    
    except Exception, e:
        error.log_debug(e, 1, config)
        error.log_debug('Error in getting blogsites for thread %d' % (thread_id), 1, config)
        return {}



def update_blog(blogname, key, value):    
    try:
        URL = 'http://' + blogname
        collection = db[config.db_table_blog]
        collection.update({'URL':URL},{"$set":{key:value}})
        
    except Exception, e:
        error.log_debug(e, 1, config)
        error.log_debug('Error in updating blog', 1, config)



def timestamp(dt_str):
    GMT = tz.gettz('UTC')
    utc = parse(dt_str).astimezone(GMT)
    timestamp = time.mktime(utc.timetuple())    
    return timestamp



def reset_thread():
    try:
        collection = db[config.db_table_blog]
        collection.update({}, {"$set": {'thread_id':-1}}, multi = True)
            
    except Exception, e:
        error.log_debug(e, 1, config)
        error.log_debug('Error in resetting thread', 1, config)        
    
    
    
def get_stat():
    try:
        collection = db[config.db_table_blog]
        
        for i in range(0, config.max_thread):
            count = collection.find({'thread_id':i}).count()
            print "thread_%d has %d sites remaining" % (i, count)
            
    except Exception, e:
        error.log_debug(e, 1, config)
        error.log_debug('Error in getting status', 1, config)




