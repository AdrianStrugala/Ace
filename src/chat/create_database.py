import sqlite3 as sql
import json
from datetime import datetime
import configparser
from . import comment_model

config = configparser.ConfigParser()
config.read('config.ini')

db = config['CHAT']['DB_NAME']
source_file = config['CHAT']['SOURCE_FILE_NAME']

sql_transaction = []

def Execute():
    create_table()
    row_counter = 0

    print(f"Fetching data from {source_file}:")
    with open(f'./chat/temp/{source_file}', buffering=1000) as file:
        for row in file:

            row_counter += 1
            row = json.loads(row)
            acutal_comment = comment_model.Comment

            acutal_comment.parent_id = row['parent_id']
            acutal_comment.comment_id = row['name']
            acutal_comment.body = format_data(row['body'])
            acutal_comment.created_utc = row['created_utc']
            acutal_comment.score = row['score']
            acutal_comment.subreddit = row['subreddit']

            acutal_comment.parent_data = find_parent(acutal_comment.parent_id)
            acutal_comment.parent_data = format_data(acutal_comment.parent_data)

            if acceptable(acutal_comment.body):
                if acutal_comment.score >= 5:
                    insert_update_comment(acutal_comment)

                if row_counter % 100000 == 0:
                    print(f'Rows read: {row_counter}, Time: {str(datetime.now())}')

def transaction_builder(sql_command):
    global sql_transaction
    sql_transaction.append(sql_command)

    if len(sql_transaction) > 500:
        with sql.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute('BEGIN TRANSACTION')
            for s in sql_transaction:
                try:
                    cursor.execute(s)
                except Exception as e:
                    print ('Error during executing transaction ' + str(e) + '. String: ' + s )
            conn.commit()
        conn.close()

        sql_transaction = []

def insert_update_comment(comment):
    try:
        sql_insert = f"""        
                INSERT OR IGNORE INTO parent_reply(comment_id, parent_id, parent, comment, subreddit, unix, score)
                VALUES ('{comment.comment_id}', '{comment.parent_id}', '{comment.parent_data}', '{comment.body}', '{comment.subreddit}', {comment.created_utc}, {comment.score});        
                """

        sql_update= f"""
                UPDATE parent_reply     
                SET comment_id = '{comment.comment_id}', parent = '{comment.parent_data}', comment = '{comment.body}', subreddit = '{comment.subreddit}', unix = {comment.created_utc}, score = {comment.score}
                WHERE parent_id = '{comment.parent_id}' AND {comment.score} > (SELECT score FROM parent_reply WHERE parent_id = '{comment.parent_id}')        
                """

        transaction_builder(sql_insert)
        transaction_builder(sql_update)

    except Exception as e:
        print ('Error during inserting and updating chat database: ', e)


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
        with sql.connect(db) as conn:
            sql_command = f"""SELECT score FROM parent_reply WHERE parent_id = '{parent_id}' LIMIT 1"""
            c = conn.cursor()
            c.execute(sql_command)
            result = c.fetchone()
        conn.close()

        if result != None:
            return result[0]
        else:
            return 0

    except Exception as e:
        print("find existing score", e)
        return 0


def format_data(data):
    data = data.replace("\n", " newlinechar ")
    data = data.replace("\r", " newlinechar ")
    data = data.replace('"', "'")
    data = data.replace("'", "''")

    return data


def find_parent(parent_id):
    try:
        with sql.connect(db) as conn:
            sql_command = f"""
                SELECT comment FROM parent_reply WHERE comment_id = '{parent_id}' 
                LIMIT 1
                """
            c = conn.cursor()
            c.execute(sql_command)
            query_result = c.fetchone()
        conn.close()

        if query_result != None:
            return query_result[0]
        else:
            return ""

    except Exception as e:
        print("Find parent:", e)
        return ""


def create_table():
    with sql.connect(db) as conn:
        sql_command = """
            CREATE TABLE IF NOT EXISTS parent_reply
            (parent_id TEXT PRIMARY KEY
            , comment_id TEXT UNIQUE
            , parent TEXT
            , comment TEXT
            , subreddit TEXT
            , unix INT
            , score INT)
            """
        c = conn.cursor()
        c.execute(sql_command)
    conn.close()