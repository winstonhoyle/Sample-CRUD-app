import sqlite3
import pandas as pd


class Database(object):

    DB_LOCATION = './application.db'

    create_table = """
                    CREATE TABLE users (
                    id integer primary key,
                    first_name text,
                    last_name text,
                    phone_number text unique,
                    client_member_id integer unique,
                    account_id integer
                    )
                    """

    def __init__(self):
        self.conn = sqlite3.connect(Database.DB_LOCATION)
        self.cur = self.conn.cursor()
        self.cur.execute("""DROP TABLE IF EXISTS users""")
        self.cur.execute(Database.create_table)

    def load_data(self, df: pd.DataFrame):
        # loading from pandas df to sqlite
        to_db = [
            (
                row.first_name,
                row.last_name,
                row.phone_number,
                row.phone_number,
                row.account_id,
            )
            for row in df.itertuples()
        ]
        try:
            self.execute_many(to_db)
            return True
        except Exception:
            return False

    def close(self):
        self.conn.close()

    def execute(self, data):
        self.cur.execute(
            """INSERT OR IGNORE INTO users VALUES (NULL, ?, ?, ?, ?, ?)""", data,
        )
        self.conn.commit()

    def execute_many(self, data):
        self.cur.executemany(
            """INSERT OR IGNORE INTO users VALUES (NULL, ?, ?, ?, ?, ?)""", data,
        )
        self.conn.commit()

    def delete_user(self, client_member_id: int):
        try:
            self.cur.execute(
                'DELETE FROM users WHERE client_member_id = {}'.format(client_member_id)
            )
            self.conn.commit()
            return True
        except Exception:
            return False

    def update_user(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        client_member_id: int,
        account_id: int,
    ):
        self.cur.execute(
            'SELECT * FROM users WHERE client_member_id = {}'.format(client_member_id)
        )
        if not self.cur.fetchall():
            return {'status': "user doesn't exist use POST /member endpoint"}
        self.cur.execute(
            f'UPDATE users SET first_name="{first_name}", last_name="{last_name}", phone_number="{phone_number}", account_id={account_id} WHERE client_member_id={client_member_id}'
        )
        self.conn.commit()
        return self.get_user(client_member_id=client_member_id)

    def add_user(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        client_member_id: int,
        account_id: int,
    ):
        data = (first_name, last_name, phone_number, client_member_id, account_id)
        self.execute(data)
        # It is a unique value
        return self.get_user(client_member_id=client_member_id)

    def get_user(self, **kwargs):
        # Get values that exist
        user_id = kwargs.get('user_id', None)
        phone_number = kwargs.get('phone_number', None)
        client_member_id = kwargs.get('client_member_id', None)
        account_id = kwargs.get('account_id', None)

        sql_stem = 'SELECT * FROM users where '

        if user_id:
            sql = sql_stem + 'id =' + str(user_id)
        if phone_number:
            sql = sql_stem + 'phone_number = ' + str(phone_number)
        if client_member_id:
            sql = sql_stem + 'client_member_id = ' + str(client_member_id)
        if account_id:
            sql = sql_stem + 'account_id = ' + str(account_id)

        self.cur.execute(sql)
        users = {'users': []}
        for user in self.cur.fetchall():
            data = {}
            data['id'] = user[0]
            data['first_name'] = user[1]
            data['last_name'] = user[2]
            data['phone_number'] = user[3]
            data['client_member_id'] = user[4]
            data['account_id'] = user[5]
            users['users'].append(data)
        return users
