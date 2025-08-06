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
            self.db_cursor.execute(f"INSERT INTO POSTS VALUES{values}")
            self.db_conn.commit()
            data = self.db_cursor.fetchall()
            
            if data == []: 
                return True 
        else:
            return False

       

    def get_all_post(self):
        if self.db_conn != None:
            self.db_cursor.execute("SELECT * FROM POSTS")
            data_columns = self.db_cursor.fetchall()
            
            self.db_cursor.execute("DESCRIBE POSTS")
            data_headers = [desc[0] for desc in self.db_cursor.fetchall()]

            return [dict(zip(data_headers,i)) for i in range(len(data_columns))]
        else:
            return False

    def get_post(self, post_id):
        if self.db_conn != None:
            self.db_cursor.execute(f"SELECT * FROM POSTS WHERE id={post_id}")
            data_columns = self.db_cursor.fetchall()
            
            self.db_cursor.execute("DESCRIBE POSTS")
            data_headers = [desc[0] for desc in self.db_cursor.fetchall()]
            data_headers = data_headers.append("tags")
            
            self.db_cursor.execute(f"SELECT * FROM post_tag WHERE post_id={post_id}")
            data_tag_id = [tag_id[1] for tag_id in self.db_cursor.fetchall()]
            
            tag_list = []
            for tag in range(len(data_tag_id)):
                self.db_cursor.execute(f"SELECT * FROM TAGS WHERE id={tag}")
                tag_list = tag_list.append(name[1] for name in self.db_cursor.fetchall())

            data_columns[0] = data_columns[0] + tuple([tag_list])

            return [dict(zip(data_headers,i)) for i in range(len(data_columns))]
        else:
            return False


    def get_keyword_post(self, word):
        if self.db_conn != None:
            self.db_cursor.execute(f"SELECT * FROM POSTS WHERE title LIKE '%{word}%' OR content LIKE '%{word}%' OR category LIKE '%{word}%'")
            data_columns = self.db_cursor.fetchall()
        
            self.db_cursor.execute("DESCRIBE POSTS")
            data_headers = [desc[0] for desc in self.db_cursor.fetchall()]

            return [dict(zip(data_headers,i)) for i in range(len(data_columns))]
        else:
            return False


    def update_post(self, post_id, changing_field, updated_field):
        if type(updated_field) == str:
            cmd = f"UPDATE POSTS SET {changing_field} = '{updated_field}' WHERE id={post_id}"
        else: 
            cmd = f"UPDATE POSTS SET {changing_field} = {updated_field} WHERE id={post_id}"
        if self.db_conn != None:
            self.db_cursor.execute(cmd)
            self.db_conn.commit()
            data_columns = self.db_cursor.fetchall()
            if len(data_columns) == 0:  ##checks if the post exists or not
                return 2                ##returns 2 as a err handling thingy
            else:
                self.db_cursor.execute(f"DELETE FROM POSTS WHERE id={post_id}")
                self.db_conn.commit()   #commits the deletion

        else:
            return False


    def delete_post(self, post_id):
         if self.db_conn != None:
            self.db_cursor.execute(f"SELECT * FROM POSTS WHERE id={post_id}")
            data_columns = self.db_cursor.fetchall()
            if len(data_columns) == 0:  ##checks if the post exists or not
                return 2                ##returns 2 as a err handling thingy
            else:
                self.db_cursor.execute(f"DELETE FROM POSTS WHERE id={post_id}")
                self.db_conn.commit()   #commits the deletion

         else:
            return False

       



