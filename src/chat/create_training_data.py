import pandas
import sqlite3


def execute():
    source_database = 'RC_2010-05.db'

    connection = sqlite3.connect(source_database)
    limit = 5000
    last_unix = 0
    current_length = limit
    counter = 0
    test_done = False
    while current_length == limit:
        dataframe = pandas.read_sql("""
                                    SELECT * FROM parent_reply 
                                    WHERE unix > ? and parent NOT NULL
                                    ORDER BY unix ASC
                                    LIMIT ?
                                    """, connection, params=(last_unix, limit))

        last_unix = dataframe.tail(1)['unix'].values[0]
        current_length = len(dataframe)
        if not test_done:
            with open("test.from", 'a', encoding='utf8') as file:
                for content in dataframe['parent'].values:
                    file.write(content + '\n')
            with open("test.to", 'a', encoding='utf8') as file:
                for content in dataframe['comment'].values:
                    file.write(content + '\n')

            test_done = True
        else:
            with open("train.from", 'a', encoding='utf8') as file:
                for content in dataframe['parent'].values:
                    file.write(content + '\n')
            with open("train.to", 'a', encoding='utf8') as file:
                for content in dataframe['comment'].values:
                    file.write(content + '\n')

        counter +=1
        if counter % 20 == 0:
            print(counter * limit + 'rows complited so far')
