import sqlite3

exists = False

'''
Simply closes the db connection.
'''
def close_connection(conn):
    conn.close()

'''
Simply shows all available content in the movies db.
'''
def show_movie_table():
    # establish connection
    # if the file does not exist, it will create it for us
    conn = sqlite3.connect('watch_list.db')

    # create a cursor to execute commands
    c = conn.cursor()
    
    try:
        c.execute("SELECT title FROM movies")
        print(c.fetchall())
    except Exception as e:
        print(e)
    finally:
        # close the connection
        close_connection(conn)


''' 
Responsible for adding the movie results into the database.
@param {dict} table The table of values (title: 'Title', cast: 'cast', etc)
'''
def add_into_table(c, table):
    title = table['title']
    synopsis = table['synopsis']
    cast = ''.join(table['cast'])
    rotten = table['rotten_rating']
    audience = table['audience_rating']

    try:
        # add info into table; check that the entry (title) is not already in the table!
        c.execute("SELECT * FROM movies WHERE title=?", (table['title'],))
        if len(c.fetchall()) > 0:
            print('Title already exists in database.')
            global exists
            exists = True
            return

        # do NOT use {}.format(), as this is susceptible to SQL injection attacks!
        c.execute("INSERT INTO movies(title, synopsis, cast, rotten, audience) VALUES (?, ?, ?, ?, ?)", (title, synopsis, cast, rotten, audience))
        # this could simplified: c.execute("INSERT INTO movies VALUES (:title, :synopsis, :cast, :rotten, :audience)", (table['title'], etc)
    except Exception as e:
        print(e)
        print('Unable to perform insertion.')
    
'''
Handles the default query of creating the table and adding the movie passed in.
@param: {dict} table The table of values representing the movie
'''
def handle_query(table):
    global exists
    # establish connection
    # if the file does not exist, it will create it for us
    conn = sqlite3.connect('watch_list.db')

    # create a cursor to execute commands
    c = conn.cursor()
    error = False
    # attempt table creation
    try:
        # attempt to create the table...we will get an error if we do this more than once
        # hence the try-catch
        c.execute("""CREATE TABLE movies (
                    title text,
                    synopsis text,
                    cast text,
                    rotten, text,
                    audience text
                    )""")
        
    except sqlite3.OperationalError as e:
        print('Table already exists. Simply adding to it.')
    except Exception as e:
        print(e)
        close_connection(conn)
    
    # try to insert movie information 
    try:
        # add into table
        add_into_table(c,table)
        # commit/save changes
        conn.commit()
    except Exception as e:
        error = True
        print(e)
    finally:
        close_connection(conn)

    if not error and not exists:
        print('{} was successfully added to the table.'.format(table['title']))
        exists = False
    else:
        print('Unable to add {} to the table.'.format(table['title']))
