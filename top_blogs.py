#!/usr/bin/python

import re
import urllib2
import classes


def getLink(itemBlock):	
	link = re.findall("<link>.+</link>", itemBlock)
	line = link[0]
	s = len("<link>")
	e = len(line) - len("</link>")
	link = line[s:e].strip()
	link = link.split('/')[2]	
	return link



def get_popular_sites():	
	try:
		url_list = []
		config = classes.config()
		source = urllib2.urlopen(config.popular_blogs_url)
		body = source.read()
				
		startPos = body.find('<channel>')
		if startPos != -1:
			endPos = body.find('</channel>', startPos+9)
			if endPos != -1:
				dataBlock = body[startPos+9:endPos]
						
				rstart = 0
				rend = 0
				
				while rstart != -1:
					rstart = dataBlock.find('<item>', rend)
					if rstart != -1:
						rend =  dataBlock.find('</item>', rstart+6)
						if rend != -1:
							
							item = dataBlock[rstart+6:rend]							
							
							if item.find('<title>') != -1:
								try:									
									link = getLink(item)								
									url_list.append(link)									
									
								except Exception as err:
									error.log_debug(err, 1, config)
									error.log_debug("Error parsing link in get_popular_sites()", 1, config)
				##
				return url_list
			
		else:
			[]
					
	except Exception as err:
		error.log_debug(err, 1, config)
		error.log_debug("Error in get_popular_sites()", 1, config)
		

