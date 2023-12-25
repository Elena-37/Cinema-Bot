from logger import logger
import psycopg2
from config import host, user, password, db_name

#get info about film: poster, name, description, ratings
class film_info():
    def get_by_title(msg):
        if type(msg) == str:
            query = msg
        else:
            query = msg.text
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
                                    WHERE title = ('{}')""".format(str(query)))
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
            
        if not result:
            logger.info("No film with this title have been found")
            return None, f"Такого фильма у меня нет. Проверь, что название введено правильно", None
        else:
            url = result[0][-1]
            d = result[0][7]
            descr = d.split('.')
            description = ''
            for i in range(min(5, len(descr))):
                description = description + descr[i] + '.'

            film = f"🍿Название: {result[0][0]} \n Описание: {description} \n ✨Рейтинг: {result[0][4]}"
            
            logger.info("Film with this title has been found!")
            return result[0][0], film, url