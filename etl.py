from datetime import time
import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Process the song file to insert data into the specific data model for analysis
    @param cur: the database cursor
    @param filepath: the path to the song file
    """

    # open song file
    df = pd.read_json(filepath, type='series')

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data = list(song_data.values)
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = list(artist_data.values)
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Process the log file to insert data into the specific data model for data analysis
    @param cur: psycopg2 connection cursor
    @param filepath: the path to the log file
    """ 

    # open log file 
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NestSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time record
    time_values = [
        t,
        t.dt.hour,
        t.dt.day,
        t.dt.weekofyear,
        t.dt.month,
        t.dt.year,
        t.dt.weekday
    ]
    column_labels = [
        'timestamp',
        'hour',
        'day',
        'weekofyear',
        'month',
        'year',
        'weekday'
    ]
    time_dict = dict(zip(column_labels, time_values))
    time_data = pd.DataFrame(time_dict)

    for i, row in time_data.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_data = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_data = user_data.drop_duplicates().dropna()

    # insert user record
    for i, row in user_data.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay record
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fechone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(song_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Read all the files in 'filepath' and call the 'func' function
    @param cur: the database server
    @param conn: the database connection
    @param filepath: the path to the data directory
    @param func: the function (process songs or logs)
    """

    # get all files matching extensions from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))
    
    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def insert_songs_and_logs():
    """
    Insert songs and logs to our custom database.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=myatnoe")
    cur = conn.cursor()

    process_data(cur, conn, filepath='./data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='./data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()