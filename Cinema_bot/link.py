import psycopg2
from config import host, user, password, db_name
from logger import logger

#get info about film: poster, name, description, ratings
class link():
    def get_link(query):
        
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
        
        urls = {}
        if result[0][5] != None:
            urls["ivi"] = result[0][5]
        if result[0][6] != None:
            urls["Lordfilm"] = result[0][6]

        logger.info("Link has been goten")
        return urls
