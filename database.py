import mysql.connector as sql

#Create a server/database? ish? 
#which handles i/o and all the things 

class Database:

    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = database
        self.db_conn = None
        self.db_cursor = None

    def connect_to_database(self):
        self.db_conn = sql.connect(
                                    host = self.host,
                                    user = self.user,
                                    password = self.passwd,
                                    database = self.db
                                    )

        if self.db_conn == None:
            return False  #Connection Failed
        else:
            self.db_cursor = self.db_conn.cursor()
            return True  #ConnECted!@!
            

    def add_post(self, values):
        if self.db_conn != None:
            self.db_cursor.execute(f"INSERT INTO POSTS (title, content, category) VALUES{values}")
            self.db_conn.commit()
            data = self.db_cursor.fetchall()
            
            if data == []: 
                return []
        else:
            return False

       

    def get_all_post(self):
        if self.db_conn != None:
            self.db_cursor.execute("SELECT * FROM POSTS")
            data_columns = self.db_cursor.fetchall()
            
            self.db_cursor.execute("DESCRIBE POSTS")
            data_headers = [desc[0] for desc in self.db_cursor.fetchall()]
            data_headers.append("tags")

            self.db_cursor.execute(f"SELECT id FROM POSTS")
            post_id = [id[0] for id in self.db_cursor.fetchall()]
           
            full_list = []  ##the whole list of tags
            for ids in post_id:
                self.db_cursor.execute(f"SELECT * FROM post_tags WHERE post_id = {ids}") ##getting ids of tags from post_tags 
                tag_id_list = [tag_id[1] for tag_id in self.db_cursor.fetchall()]        ##which is then used to find tag names
                
                tags_list = []

                for tag_ids in tag_id_list:
                    self.db_cursor.execute(f"SELECT * FROM TAGS WHERE id = {tag_ids}")
                    tag = self.db_cursor.fetchall()[0][0]
                    tags_list.append(tag)

                full_list.append(tags_list)

            for posts in range(len(full_list)):
                data_columns[posts] = data_columns[posts] + tuple([full_list[posts]])

            return [dict(zip(data_headers,i)) for i in data_columns]
        else:
            return False

    def get_post(self, post_id):
        if self.db_conn != None:
            self.db_cursor.execute(f"SELECT * FROM POSTS WHERE id={post_id}")
            data_columns = self.db_cursor.fetchall()
            
            self.db_cursor.execute("DESCRIBE POSTS")
            data_headers = [desc[0] for desc in self.db_cursor.fetchall()]
            data_headers.append("tags")
            
            self.db_cursor.execute(f"SELECT * FROM post_tags WHERE post_id={post_id}")
            data_tag_id = [tag_id[1] for tag_id in self.db_cursor.fetchall()]
            
            tag_list = []
            for tag in data_tag_id:
                self.db_cursor.execute(f"SELECT * FROM TAGS WHERE id={tag}")
                tag_list.append([name[1] for name in self.db_cursor.fetchall()])

            data_columns[0] = data_columns[0] + tuple(tag_list)

            return [dict(zip(data_headers,i)) for i in data_columns]
        else:
            return False


    def get_keyword_post(self, word):
        if self.db_conn != None:
            self.db_cursor.execute(f"SELECT * FROM POSTS WHERE title LIKE '%{word}%' OR content LIKE '%{word}%' OR category LIKE '%{word}%'")
            data_columns = self.db_cursor.fetchall()
        
            self.db_cursor.execute("DESCRIBE POSTS")
            data_headers = [desc[0] for desc in self.db_cursor.fetchall()]

            return [dict(zip(data_headers,i)) for i in data_columns]
        else:
            return False


    def update_post(self, post_id, changed_data, no_of_fields):
        if no_of_fields == 3:
            cmd = f"UPDATE POSTS SET title='{changed_data["title"]}' , content='{changed_data["content"]}' , category='{changed_data["category"]}' WHERE id={post_id}"
        if no_of_fields == 2:
            if changed_data['title'] == None:
                cmd =  f"UPDATE POSTS SET  content='{changed_data["content"]}' , category='{changed_data["category"]}' WHERE id={post_id}"
            elif changed_data['content'] == None:
                cmd =  f"UPDATE POSTS SET  title='{changed_data["title"]}' , category='{changed_data["category"]}' WHERE id={post_id}"
            elif changed_data['category'] == None:
                cmd = f"UPDATE POSTS SET  title='{changed_data["title"]}' , content='{changed_data["content"]}' WHERE id={post_id}"
        if no_of_fields == 1:
            if changed_data["title"] != None:
                cmd =  f"UPDATE POSTS SET  title='{changed_data["title"]}' WHERE id={post_id}"
            elif changed_data["content"] != None:
                cmd = f"UPDATE POSTS SET  content='{changed_data["content"]}' WHERE id={post_id}"
            elif changed_data["category"] != None:
                cmd = f"UPDATE POSTS SET  category='{changed_data["category"]}' WHERE id={post_id}"

        if self.db_conn != None:
            self.db_cursor.execute(cmd)
            self.db_conn.commit()
            data_columns = self.db_cursor.fetchall()
            if data_columns == []:
                return True 
            else:
                return False


    def delete_post(self, post_id):
         if self.db_conn != None:
            self.db_cursor.execute(f"SELECT * FROM POSTS WHERE id={post_id}")
            data_columns = self.db_cursor.fetchall()
            if data_columns == []:  ##checks if the post exists or not
                return 0  ##returns 2 as a err handling thingy
            else:
                self.db_cursor.execute(f"DELETE FROM POSTS WHERE id={post_id}")
                self.db_conn.commit()   #commits the deletion
                return 1
         else:
            return False

       



