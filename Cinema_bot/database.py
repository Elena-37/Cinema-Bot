import psycopg2
from logger import logger
import json
from config import host, user, password, db_name

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        logger.info(f"Server version: {cursor.fetchone()}")
    
    #создаём бд
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE films(
                title varchar(255) PRIMARY KEY,
                rating_kp float,
                rating_imdb float,
                rating_ivi float,
                max_rating float,
                link_ivi varchar(255),
                link_lordfilms varchar(255),
                description varchar(2000) NOT NULL,
                country varchar(255)[] NOT NULL,
                genres varchar(255)[] NOT NULL,
                type varchar(50) NOT NULL,
                poster varchar(255));"""
        )
        logger.info("Table created successfully")

    #read lordfilm file with films, series and films
    with open("pawuk_films/lord_films.json") as f:
        file_content = f.read()
        film = json.loads(file_content)   
    
    #lordfilms -> database
    with connection.cursor() as cursor:
        for i in range(21604):
            link = str(film[i]['link']).split()[-1][:-1] #link

            name = str(film[i]['name']) #title
            name = name.replace("'", "\"") #in order not to have problems

            poster = film[i]['poster']#poster
            
            #ratings
            if film[i]['rating_kp'] == None:
                rating_kp = 0
            else:
                rating_kp = float(film[i]['rating_kp']) 
            if film[i]['rating_imdb'] == None:
                rating_imdb = 0
            else:
                rating_imdb = float(film[i]['rating_imdb'])

            descr = str(film[i]['description']) #description
            descr = descr.replace("'", "\"") #in order not to have problems

            country = []
            for c in film[i]['country']: #countries
                if c[0] == ' ':
                    c = c[1::]
                country.append(c)
            
            genre = []
            for g in film[i]['genres']: #genres
                if g[0] == ' ':
                    g = g[1::]
                genre.append(g)

            flag = str(film[i]['film_or_series']) #flag

            #check the existance
            result = None
            try:
                cursor.execute("""SELECT * FROM films WHERE title = '{}';""".format(name))
                result = cursor.fetchall()
            except:
                result = None

            #if the key does not exist
            if not result:
                cursor.execute(
                    """INSERT INTO films (title, rating_kp, rating_imdb, max_rating, link_lordfilms, description, country, genres, type, poster) 
                    VALUES ('{}', {}, {}, {}, '{}', '{}', ARRAY{}, ARRAY{}, '{}', '{}');""".format(name, rating_kp, rating_imdb, max(rating_kp, rating_imdb), link, descr, country, genre, flag, poster)
                )
        logger.info("Data was successfully inserted")
    
    #read ivi file with films, series and films
    with open("pawuk_films/ivi_films.json") as f:
        file_content = f.read()
        film = json.loads(file_content)  
    
    #ivi -> database
    with connection.cursor() as cursor:
        for i in range(3848):
            link = str(film[i]['link']).split()[-1][:-1] #link

            name = str(film[i]['name']) #title
            name = name.replace("'", "\"") #in order not to have problems
            
            rating_ivi = film[i]['rating_ivi'] #rating
            if rating_ivi == None:
                rating_ivi = 0
            else:
                rating_ivi = rating_ivi.replace(",", ".")
                rating_ivi = float(rating_ivi)

            descr = str(film[i]['description']) #description
            descr = descr.replace("'", "\"") #in order not to have problems

        
            country = film[i]['country'] #countries
            if type(country) == str:
                country = [country]
            genre = film[i]['genres'] #genres
            if type(genre) == str:
                genre = [genre]
            
            flag = str(film[i]['film_or_series']) #flag

            #check the existance
            result = None
            try:
                cursor.execute("""SELECT * FROM films WHERE title = '{}';""".format(name))
                result = cursor.fetchall()
            except:
                result = None

            if result:
                if result[0][4] < rating_ivi:
                    cursor.execute(
                        """UPDATE films SET link_ivi=('{}'), rating_ivi=({}), max_rating=({}) WHERE title=('{}');""".format(link, rating_ivi, rating_ivi, poster, name)
                    )
                else:
                    cursor.execute(
                        """UPDATE films SET link_ivi=('{}'), rating_ivi=({}) WHERE title=('{}');""".format(link, rating_ivi, name)
                    )
            else:
                cursor.execute(
                    """INSERT INTO films (title, rating_ivi, max_rating, link_ivi, description, country, genres, type, poster) 
                    VALUES ('{}', {}, {}, '{}', '{}', ARRAY{}, ARRAY{}, '{}', '{}');""".format(name, rating_ivi, rating_ivi, link, descr, country, genre, flag, poster)
                )
        logger.info("Data was successfully inserted")
    
    
except Exception:
    logger.warning("Error while working with PostgreSQL")
finally:
    if connection:
        connection.close()
        logger.info("PostgreSQL connection closed")
