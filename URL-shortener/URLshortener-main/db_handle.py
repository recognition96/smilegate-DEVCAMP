import pymysql

class DataBase:
    def __init__(self):
        print("--DB--")

    def get_cursor(self):
        self.DB = pymysql.connect(
            user='root',
            passwd='3542',
            host='127.0.0.1',
            db='server',
            charset='utf8'
        )
        return self.DB.cursor(pymysql.cursors.DictCursor)

    def select_id_by_url(self, url):
        qry = f"""SELECT id
                  FROM domains D
                  WHERE D.origin="{url}"
              """

        cursor = self.get_cursor()
        cursor.execute(qry)
        result = cursor.fetchone()
        self.DB.commit()
        self.DB.close()

        return result

    def select_url_by_id(self, idx):
        qry = f"""SELECT origin
                  FROM domains D
                  WHERE D.id={idx}
              """

        cursor = self.get_cursor()
        cursor.execute(qry)
        result = cursor.fetchone()
        self.DB.commit()
        self.DB.close()

        return result

    def insert_url(self, url):
        qry = f"""INSERT INTO domains(origin, count)
                  VALUES("{url}", 1)
                  ON DUPLICATE KEY 
                  UPDATE count = count + 1, last_input_time = CURRENT_TIMESTAMP
              """

        cursor = self.get_cursor()
        cursor.execute(qry)
        self.DB.commit()
        self.DB.close()

    def select_top5_url(self):
        qry = """SELECT origin, count, last_input_time
                 FROM domains
                 ORDER BY count DESC
                 LIMIT 5
              """

        cursor = self.get_cursor()
        cursor.execute(qry)
        result = cursor.fetchall()
        self.DB.commit()
        self.DB.close()

        return result
