from arango import ArangoClient
from user.config import settings


client = ArangoClient(hosts=settings.DATABASE_URL)

sys_db = client.db('_system', username='root', password=settings.DATABASE_PASSWORD)


if not sys_db.has_database(settings.DATABASE_NAME):
    sys_db.create_database(settings.DATABASE_NAME, users=[
        {'username': settings.DATABASE_USER, 'password': settings.DATABASE_PASSWORD, 'active': True}
    ])

db = client.db(settings.DATABASE_NAME, username=settings.DATABASE_USER, password=settings.DATABASE_PASSWORD)