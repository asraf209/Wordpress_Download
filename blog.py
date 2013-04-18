#!/usr/bin/python

import utility
import error
import datetime


def get(blogname, config):
			
	fetch_ok = False
		
	query = config.api_url + blogname + config.param_blog
	
	for i in range(0, config.max_fetch_attempts):				
		result = utility.fetch(query, config)		
		if result != {}:
			fetch_ok = True			
			break
		else:
			error.log_debug("Fetching failure, try again", 1, config)
			
	if fetch_ok == False:
		error.log_debug("Fail after several attempts, skip this section", 1, config)
		return			
	
	result['thread_id'] = config.thread_id_newcomer						# -2
	result['entry_time'] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S GMT")		# GMT	
			
		
	utility.store(result, 'blog', config)	
		
	