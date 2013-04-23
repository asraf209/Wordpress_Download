import urllib2
import json
import utility
import error



def get(blogname, post_id, config):
    
    offset = 0
    blog_saved = False
    total_comments = 0
    #insert_comments = []    
    fetched_comments = 0
    fetch_ok = False
    #end_loop = False
    last_update = 0
    latest_post_date = 0
    
        
    while True:
        
        query = config.api_url + blogname + '/posts/' + str(post_id) + config.param_comment + str(offset)        
        
        endcount = offset+config.max_fetch-1
        
        if total_comments >= 1 and endcount+1 > total_comments:            
            endcount = total_comments -1

        if total_comments <= 0:
            error.log_debug("Fetching comments %d-%d from %s post_id:%d" % (offset+1, endcount+1, blogname, post_id), 2, config)
        else:
            error.log_debug("Fetching comments %d-%d/%d from %s post_id:%d" % (offset+1, endcount+1, total_comments, blogname, post_id), 2, config)
    
            
        for i in range(0,config.max_fetch_attempts):
            result = utility.fetch(query, config)
            if result != {}:
                fetch_ok = True 
                break
            else:
                error.log_debug("Fetching failure, try again", 1, config)
                
        if fetch_ok == False:
            error.log_debug("Fail after several attempts, " + query, 1, config)
            break
    
                
        if result.has_key('found') and result['found'] != 0 and len(result['comments']) > 0:
    
            total_comments = result['found']                        
                    
            for comment in result['comments']:
                
                #comment['date_unix'] = utility.get_unix_timestamp(comment['date'])
                comment['date_unix'] = get_unix_timestamp(comment['date'])
                
                done = utility.store(comment, 'comment', config)
                
                if done:
                    fetched_comments += 1
                            
            
        else:
            error.log_debug("Error Response in fetching comments %d-%d from %s post_id:%d" % (offset+1, endcount+1, blogname, post_id), 1, config)

        if total_comments > config.max_fetch:
            offset += config.max_fetch
            
        if offset >= total_comments or total_comments <= config.max_fetch:                                                
            error.log_debug("Fetched %d/%d comments from %s post_id:%d" % (fetched_comments, total_comments, blogname, post_id), 2, config)
            break
        





def get_unix_timestamp(dt_str):    
    try:        
        ts = utility.timestamp(dt_str)
        return ts    
    except Exception as err:        
        fix_invalid_date(dt_str)
        
        
        
def fix_invalid_date(dt_str):       # handle datetime with wrong TZ or date older than 1970-01-01
    try:
        return utility.timestamp(dt_str[:19] + '+00:00')
    except Exception as err:
        return utility.timestamp('1970-01-01T00:00:00+00:00')