import psycopg2
from config import host, user, password, db_name
from logger import logger

#get top-10 by country
class country_info():
    def get_by_country(query):

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
                                    WHERE array_position(country , '{}') IS NOT NULL AND LENGTH(title) <= 21
                                    ORDER BY max_rating DESC""".format(str(query)))
                    result = cursor.fetchall()
                    logger.info("Raws have been found")
                except:
                    result = None
                    logger.info("No raws have been found")

            logger.warning("Error while working with PostgreSQL")
        finally:
            if connection:
                connection.close()
                logger.info("PostgreSQL connection closed")
            
        if not result:
            logger.info("No films from this country have been found")
            return 0, f"Такой страны у меня нет", []

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

        logger.info("Top from this country have been created successfully")
        return 1, list_of_strings, keyboard_info
