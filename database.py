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
                                    password = self.passwd
                                    )

        if self.db_conn == None:
            return False  #Connection Failed
        else:
            self.db_cursor = self.db_conn.cursor()
            return True  #ConnECted!@!
            

    def add_post(self):
        pass

    def get_all_post(self) --> dict:
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

            return [dict(zip(data_headers,i)) for i in range(len(data_columns))]
        else:
            return False


    def get_keyword_post(self):
        pass

    def update_post(self):
        pass

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

       



