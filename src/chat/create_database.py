import sqlite3
import json
from datetime import datetime
from sqlite3.dbapi2 import Cursor, Connection

source_file_name = 'RC_2010-05'
sql_transaction = []

connection: Connection = sqlite3.connect('{}.db'.format(source_file_name))
cursor: Cursor = connection.cursor()


def execute():
    create_table()
    row_counter = 0
    paired_rows = 0

    with open('C:\workspace\Ace\{}'.format(source_file_name), buffering=1000) as file:
        for row in file:
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            comment_id = row['name']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']

            parent_data = find_parent(parent_id)

            if acceptable(body):
                if score >= 5:
                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score:
                        if score >= existing_comment_score:
                            sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc,
                                                       score)

                    else:
                        if parent_data:
                            sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc,
                                                  score)
                            paired_rows +=1
                        else:
                            sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score)

                if row_counter % 100000 == 0:
                    print('Rows read: {}, Paired rows: {}, Time: {}'.format(row_counter, paired_rows, str(datetime.now())))

def transaction_builder(sql):
    global sql_transaction
    sql_transaction.append(sql)

    if len(sql_transaction) > 1:
        cursor.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                cursor.execute(s)
            except Exception as e:
                print ('Error during executing transaction', str(e))
        connection.commit()

        sql_transaction = []


def sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score):
    try:
        sql = """
        INSERT INTO parent_reply  
        (comment_id, parent_id, parent, comment, subreddit, unix, score)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(sql, (comment_id, parent_id, parent_data, body, subreddit, created_utc, score))
    except Exception as e:
        print ('sql insert has parent', e)


def sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score):
    try:
        sql = """
        INSERT INTO parent_reply  
        (comment_id, parent_id, comment, subreddit, unix, score)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        cursor.execute(sql, (comment_id, parent_id, body, subreddit, created_utc, score))
    except Exception as e:
        print ('sql insert no parent', str(e))


def sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc, score):
    try:
        sql = """
        UPDATE parent_reply SET comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? 
		WHERE parent_id = ?;
		"""
        cursor.execute(sql, (comment_id, parent_data, body, subreddit, created_utc, score, parent_id))

    except Exception as e:
        print('replace_comment', e)


def acceptable(data):
    if len(data.split(' ')) > 50 or len(data) < 1:
        return False
    elif len(data) > 1000:
        return False
    elif data == '[deleted]' or data == '[removed]':
        return False
    else:
        return True


def find_existing_score(parent_id):
    try:
        sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(parent_id)
        cursor.execute(sql)
        result = cursor.fetchone()

        if result != None:
            return result[0]
        else:
            return False

    except Exception as e:
        print("find_parent", e)
        return False


def format_data(data):
    data = data.replace("\n", " newlinechar ")
    data = data.replace("\r", " newlinechar ")
    data = data.replace('"', "'")

    return data


def find_parent(parent_id):
    try:
        sql = """
        SELECT comment FROM parent_reply WHERE comment_id = '{}' 
        LIMIT 1
        """.format(parent_id)
        cursor.execute(sql)
        result = cursor.fetchone()

        if result != None:
            return result[0]
        else:
            return False

    except Exception as e:
        print("find_parent", e)
        return False


def create_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS parent_reply
        (parent_id TEXT PRIMARY KEY
        , comment_id TEXT UNIQUE
        , parent TEXT
        , comment TEXT
        , subreddit TEXT
        , unix INT
        , score INT)
        """)
