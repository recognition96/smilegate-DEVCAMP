import pymysql

class DataBase:
    def __init__(self):
        print("--DB--")

    def get_cursor(self):
        self.DB = pymysql.connect(
            user='userId',
            passwd='userPwd',
            host='127.0.0.1',
            db='dbName',
            charset='utf8'
        )
        return self.DB.cursor(pymysql.cursors.DictCursor)

    def select_user_by_id(self, uid):
        qry = f"""SELECT *
                  FROM user
                  WHERE user_id = '{uid}'
               """

        cursor = self.get_cursor()
        cursor.execute(qry)
        result = cursor.fetchall()

        self.DB.commit()
        self.DB.close()

        return result

    def select_all_users(self):
        qry = f"""SELECT *
                  FROM user
               """

        cursor = self.get_cursor()
        cursor.execute(qry)
        result = cursor.fetchall()

        self.DB.commit()
        self.DB.close()

        return result

    def insert_user(self, user_data):
        qry = f"""INSERT INTO user(user_id, password, grade)
                  VALUES("{user_data['id']}", "{user_data['pswd']}", '1')
              """

        cursor = self.get_cursor()
        cursor.execute(qry)
        self.DB.commit()
        self.DB.close()

    def update_user_auth(self, user_id):
        qry = f"""UPDATE user
                  SET grade = IF(grade = '0', '1', '0')
                  WHERE user_id = '{user_id}'
              """

        cursor = self.get_cursor()
        cursor.execute(qry)
        self.DB.commit()
        self.DB.close()

    def delete_user(self, user_id):
        qry = f"""DELETE FROM user
                  WHERE user_id = '{user_id}'
              """

        cursor = self.get_cursor()
        cursor.execute(qry)
        self.DB.commit()
        self.DB.close()


if __name__ == '__main__':
    db = DataBase()
    result = db.select_user_by_id('admin')
    if not result:
        print(result[0]['user_id'], result[0]['password'])
