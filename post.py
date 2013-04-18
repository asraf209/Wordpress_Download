import urllib2
import json
import utility
import error
import comment



def get(blogname, config):
    
    offset = 0
    blog_saved = False
    total_posts = 0
    insert_posts = []    
    fetched_posts = 0    
    fetch_ok = False
    end_loop = False
    last_update = 0
    latest_post_date = 0        
        
    
    while True:
        
        query = config.api_url + blogname + config.param_post + str(offset)
        
        endcount = offset + config.max_fetch-1
        
        if total_posts >= 1 and endcount+1 > total_posts:            
            endcount = total_posts -1

        if total_posts <= 0:
            error.log_debug("Fetching posts %d-%d from %s" % (offset+1, endcount+1, blogname), 2, config)
        else:
            error.log_debug("Fetching posts %d-%d/%d from %s" % (offset+1, endcount+1, total_posts, blogname), 2, config)
           
            
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
           
                
        if result.has_key('found') and result['found'] != 0 and len(result['posts']) > 0:
            
            if blog_saved == False:
                total_posts = result['found']
                utility.update_blog(blogname, 'total_posts', total_posts) 
                
                latest_post_date = result['posts'][0]['date']                
                latest_post_date_unix = get_unix_timestamp(latest_post_date, result['posts'][0]['modified'])
                
                blog_saved = True
            
                        
            
            last_update_unix = utility.get_last_update_unix(blogname)     # got a dict
            if len(last_update_unix) > 0:
                last_update_unix = last_update_unix['last_update_unix']
            
            ##break
    
        
    
            for post in result['posts']:                
                                
                post_date = get_unix_timestamp(post['date'], post['modified'])
                                
                if last_update_unix == {} or ( last_update_unix <  post_date ):                
                    
                    if utility.is_found(post['ID'], blogname, 'post') is False:
                        post['blog_URL'] = 'http://' + blogname
                        post['date_unix'] = post_date                                  # inserting a new entry to the post, 'date_utc'
                        insert_posts.append(post)
                        fetched_posts += 1
                        
                                    
                elif post_date <= last_update_unix: 
                    error.log_debug("The rest are old post, end fetching", 2, config)
                    #error.log_debug("Fetched %d/%d posts from %s" % (fetched_posts, total_posts, blogname), 2, config)
                    end_loop = True
                    break                                                
                
                
            if insert_posts != []:
                
                for post in insert_posts:
                    error.log_debug("Starting to store post, ID: %d" % (post['ID']), 2, config)
                    
                    done = utility.store(post, 'post', config)
                    
                    if done:
                        #fetched_posts += 1
                        comment.get(blogname, post['ID'], config)
                        #pass
                    else:
                        error.log_debug("Error in fetching post, ID: %d from %s" % (post['ID'], blogname), 1, config)
                        
            insert_posts = []            
                    
                    
            if end_loop:
                if latest_post_date != 0:            
                    utility.update_blog(blogname, 'last_update', latest_post_date)
                    utility.update_blog(blogname, 'last_update_unix', latest_post_date_unix)
                    utility.update_thread(blogname)
                                        
                error.log_debug("Fetched %d/%d posts from %s" % (fetched_posts, total_posts, blogname), 2, config)    
                break


        else:
            error.log_debug("Error Response in fetching posts %d-%d from %s" % (offset+1, endcount+1, blogname), 1, config)

        if total_posts > config.max_fetch:
            offset += config.max_fetch

            
            
        if offset >= total_posts or total_posts <= config.max_fetch:                                    
            
            utility.update_blog(blogname, 'last_update', latest_post_date)
            utility.update_blog(blogname, 'last_update_unix', latest_post_date_unix)
            utility.update_thread(blogname)
            
            error.log_debug("Fetched %d/%d posts from %s" % (fetched_posts, total_posts, blogname), 2, config)
            break
        





def get_unix_timestamp(dt_str1, dt_str2):    
    try:        
        ts = utility.timestamp(dt_str1)
        return ts
    
    except Exception as err:        
        if str(err).find('must be in -1439') != -1:
            new_dt1 = replace_TZ(dt_str1, dt_str2)                        
            try:
                ts = utility.timestamp(new_dt1)     
                return ts
            except Exception as err:
                return utility.timestamp(dt_str1[:19] + '+00:00')        
        else:
            return utility.timestamp(dt_str1[:19] + '+00:00')            



def replace_TZ(dt_str1, dt_str2):    
    str1_dt = dt_str1[:19]
    str2_tz = dt_str2[19:len(dt_str2)]            
    new_dt = str1_dt + str2_tz
    return new_dt