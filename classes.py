class config:
    
    def __init__(self):

        self.debug = True
        self.debug_file_name = 'debug_log'

        #self.db_host = '129.105.126.34'
        self.db_host = 'localhost'
        self.db_port = 27017        
        self.auth = False
        #self.db_user = 'yxi389'
        #self.db_passwd = 'yxi389'
        
        self.db_name = 'voxsup-twitter'
        self.db_table_blog = 'wordpress_popular_blogs'
        self.db_table_post = 'wordpress_posts'
        self.db_table_comment = 'wordpress_comments'
        
        self.blog_uni_key = 'URL'
        self.post_uni_key = 'ID'
        self.comment_uni_key = 'ID'

        self.popular_blogs_url = 'http://botd.wordpress.com/topsites-en.xml'
        self.param_blog = '/?pretty=1'        
        self.param_post = '/posts/?pretty=1&offset='
        self.param_comment = '/replies/?pretty=1&offset='
                
        self.api_url = 'https://public-api.wordpress.com/rest/v1/sites/'
        
        self.max_fetch = 20
        self.max_thread = 5
        self.max_fetch_attempts = 3
        self.max_store_attempts = 3

        self.thread_id = 0
        
        self.thread_id_done = -1
        self.thread_id_newcomer = -2
            
