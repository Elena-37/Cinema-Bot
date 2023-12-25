import psycopg2
from config import host, user, password, db_name
from logger import logger

#get top-10 by genre
class genre_info():
    def get_by_genre(query):
        query = query.capitalize()
        
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
                
            with connection.cursor() as cursor:
                result = None
                try:
                    cursor.execute("""SELECT * FROM films
                                    WHERE array_position(genres , '{}') IS NOT NULL AND LENGTH(title) <= 21
                                    ORDER BY max_rating DESC""".format(str(query)))
                    result = cursor.fetchall()
                    logger.info("Raws have been found")
                except:
                    result = None
                    logger.info("No raws have been found")

        except Exception:
            logger.warning("Error while working with PostgreSQL")
        finally:
            if connection:
                connection.close()
                logger.info("PostgreSQL connection closed")
            
        if result == None:
            logger.info("No films of this genre have been found")
            return f"Такого жанра у меня нет"

        else:
            if (len(result) >= 10):
                t = 10
            else:
                t = len(result)
                
            list_of_strings = ""
            keyboard_info = []
        
            for i in range(t):
                if i == 9:
                    film = f"{i + 1}. 🍿Название: {result[i][0]}\n      ✨Рейтинг: {result[i][4]} \n\n"
                else:
                    film = f"{i + 1}. 🍿Название: {result[i][0]}\n    ✨Рейтинг: {result[i][4]} \n\n"
                list_of_strings = list_of_strings + film
                keyboard_info.append(result[i][0])
            
            logger.info("Top of this genres have been created successfully")
            return list_of_strings, keyboard_info
        