## Sparkify Data Modeling

### Purpose 

Sparkify, a startup, wants to analyze their data on their online music streaming app but they don't have an easy way to query their data which resides in a directory of JSON logs on user activity on the app, as well as directory with JSON metadata on the songs in their app. And therefore, create a Postgres database with tables designed to optimize queries on song play analysis. 


### Datasets

##### Song Datset: 
It is a subset of [Million Song Dataset](http://millionsongdataset.com). Each file in the dataset is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID.

##### Log Dataset:
This dataset contains user activity logs and is generated by [Event Simulator](https://github.com/Interana/eventsim) based on the songs in the dataset above.

### Database Schema Design

Using the song and log datasets, Star Schema is created and this includes the following tables.

##### Fact Table:
1. songplays - records in log data associated with song plays

##### Dimension Tables:
1. users - users in the log file
2. songs - songs in the music data
3. artists - artists in the music data
4. time - timestamps of records in songplays

### ETL Pipeline

An ETL pipeline, `etl.py` is building which collects data from JSON files and then inserts them into the respective tables. 

## Getting Started

### Prerequisites

- python 3.7
- PostgreSQL
- psycopg2 (python library)

### How to run

Clone the repository into a local machine using

```sh
git clone https://github.com/cherish-noe/sparkify-data-modeling
```
Follow the steps to extract and load the data into the data model.

1. Run `create_tables.py` to create/ reset the tables
2. Next,run `etl.py` to extract and load the data into the database
3. With `test.ipynb`, check the data has successfully loaded into the database 

<br>
<i> This is a project from Udacity Data Engineering Nanodegree Program. </i>
