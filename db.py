import psycopg2

from config import host, user, password, db_name


# Переделать функцию под коннект и асинхрон
def connect_to_db():
    global connection
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
        )
        connection.autocommit = True

        print('[INFO] PostgreSQL connection success')

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)


def disconnect_from_db():
    connection.close()
    print('[INFO] PostgreSQL connection closed')


async def get_data(data):
    with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Directions" WHERE payment = '{data['payment']}' AND direction = '{data['direction']}' AND vacancies != 'Нет' AND vacancies != 'нет';"""
            )

            return cursor.fetchall()


if __name__ == '__main__':
    connect_to_db()
