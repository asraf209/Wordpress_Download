#!/usr/bin/python

import os
import sys
import time
import datetime
import classes
import top_blogs
import blog
import post
import utility
import error


def main():
    
    config = classes.config()
    utility.connect()
                    
            
    if len(sys.argv) >= 2:
        
        if sys.argv[1] == '-test':
            print "Testing..."
            post.get("blackadventurescomic.com", config)
            
            
        elif sys.argv[1] == '-thread' and len(sys.argv) >= 4:
            
            thread_id = int(sys.argv[3])
            config.thread_id = thread_id
            
            blogsites = utility.get_blogsites(thread_id)
            
            error.log_debug("Running the %d/%d thread...." % (thread_id, config.max_thread-1), 2, config)
            
            for blogname in blogsites:
                blogname = blogname['URL']
                blogname = blogname.split('/')[2]                
                post.get(blogname, config)
            
            error.log_debug("End of the %d/%d thread." % (thread_id, config.max_thread-1), 2, config)
            
            
                
        elif sys.argv[1] == '-reset':
            utility.reset_thread()
            print "Reset Done."
            
        elif sys.argv[1] == '-stat':
            utility.get_stat()
        
        
            
    else:
        error.log_debug("\n\nStarting.. %s" % (datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S GMT")), 2, config)
        error.log_debug("Getting all popular wordpress blogs..", 2, config)
        
        blogs = top_blogs.get_popular_sites()
        
        
        error.log_debug("Creating indexes..", 2, config)
        utility.create_index()
        
        
        time.sleep(10)
        
        
        for blogname in blogs:
            error.log_debug("%s" % (blogname), 2, config)
            blog.get(blogname, config)
                                        
        
        '''
        error.log_debug("Assigning threads..", 2, config)
        utility.assign_thread()
        
        
        
        error.log_debug("Starting threads..", 2, config)
        
        for i in range(0, config.max_thread):        
            os.system("./main.py -thread -tid %s > /dev/null &" % (str(i)))
            time.sleep(2)
        '''    
            

if __name__ == '__main__':
    main()