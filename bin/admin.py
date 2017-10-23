import psycopg2
import os

print(os.environ)

conn = psycopg2.connect("dbname=dds7q3a5dl5c45 user=edksigbbpxnyrh password=" +
                        os.environ.get('DATABASE_PASSWORD') + " host=" + os.environ.get('DATABASE_HOST'))


def delete_favorite(text):
    cur = conn.cursor()
    cur.execute("DELETE FROM Tweets WHERE WHERE content='%s'" % text)
    cur.close()

delete_favorite('Forefathers -- finding opportunity, fighting injustice, forging a more perfect union [none]” “we hold these truths to be self-evident, that all men are created equal,” you can see them, because they’ve done outstanding work.')


