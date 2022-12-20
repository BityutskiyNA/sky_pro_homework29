import csv
import io

import psycopg2

dsn = {
    'dbname': 'ad_database',
    'user': 'POSTGRES',
    'password': 'POSTGRES',
    'host': 'localhost',
    'port': 5432,
    'options': '-c search_path=public',
}


def load_ad(cursor):
    data = []
    with open('ad.csv', encoding='utf-8') as csv_f:
        for row in csv.DictReader(csv_f):
            data.append(
                (
                    row['Id'],
                    row['name'],
                    row['author_id'],
                    row['price'],
                    row['description'],
                    row['is_published'],
                    row['image'],
                    row['category_id'],
                )
            )


    args = ','.join(cursor.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s)", item).decode() for item in data)
    cursor.execute(f"""
           INSERT INTO public.ads_ad (id, name, author_id, price, description, is_published, image, category_id)
           VALUES {args}
           """)


def load_user(cursor):
    data = []
    with open('user.csv', encoding='utf-8') as csv_f:
        for row in csv.DictReader(csv_f):
            data.append(
                (
                    row['id'],
                    row['first_name'],
                    row['last_name'],
                    row['username'],
                    row['password'],
                    row['role'],
                    row['age'],
                    row['location_id'],
                )
            )

    args = ','.join(cursor.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s)", item).decode() for item in data)
    cursor.execute(f"""
              INSERT INTO public.user_user (id, first_name, last_name, username, password, role, age, location_id)
              VALUES {args}
              """)


def load_category(cursor):
    data = []
    with open('category.csv', encoding='utf-8') as csv_f:
        for row in csv.DictReader(csv_f):
            data.append(
                (
                    row['id'],
                    row['name'],
                )
            )

    args = ','.join(cursor.mogrify("(%s, %s)", item).decode() for item in data)
    cursor.execute(f"""
               INSERT INTO public.category_category (id, name)
               VALUES {args}
               """)


def load_location(cursor):
    data = []
    with open('location.csv', encoding='utf-8') as csv_f:
        for row in csv.DictReader(csv_f):
            data.append(
                (
                    row['id'],
                    row['name'],
                    row['lat'],
                    row['lng'],
                )
            )

    args = ','.join(cursor.mogrify("(%s, %s, %s, %s)", item).decode() for item in data)
    cursor.execute(f"""
               INSERT INTO public.user_location (id, name, lat, lng)
               VALUES {args}
               """)


with psycopg2.connect(**dsn) as conn, conn.cursor() as cursor:
    load_category(cursor)
    load_location(cursor)
    load_user(cursor)
    load_ad(cursor)
