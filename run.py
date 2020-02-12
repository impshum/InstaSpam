from PIL import Image
import sqlite3
from sqlite3 import Error
import time
import os
import argparse
import configparser


parser = argparse.ArgumentParser(
    description='InstaSpam v2.0 (by u/impshum)',
    epilog="If you lose your account it's on you!")

parser.add_argument(
    '-u', '--update', help='Update from text file', action='store_true')
parser.add_argument(
    '-a', '--all', help='Print all DB', action='store_true')
parser.add_argument(
    '-t', '--test', help='Test mode', action='store_true')
parser.add_argument(
    '-c', '--config', help='Change user/pass', action='store_true')
parser.add_argument(
    '-d', '--delete', help='Delete DB', action='store_true')
args = parser.parse_args()

update_mode = True if args.update else False
all_mode = True if args.all else False
test_mode = True if args.test else False
config_mode = True if args.config else False
delete_mode = True if args.delete else False


def instaspam(instauser, instapass, upload_image, upload_caption):
    if test_mode:
        return True
    else:
        from instabot import Bot
        import logging
        bot = Bot()
        bot.logger.setLevel(logging.WARNING)
        bot.login(username=instauser, password=instapass)
        bot.upload_photo(upload_image, caption=upload_caption)
        if bot.api.last_response.status_code == 200:
            return True


def crop_image(file):
    counter = 0
    file = f'images/{file}'
    img = Image.open(file)
    new_size = 1080, 1080
    width, height = img.size
    if width > height:
        delta = width - height
        left = int(delta / 2)
        upper = 0
        right = height + left
        lower = height
    else:
        delta = height - width
        left = 0
        upper = int(delta / 2)
        right = width
        lower = width + upper
    img = img.crop((left, upper, right, lower))
    img.thumbnail(new_size, Image.ANTIALIAS)
    fname = os.path.basename(file)
    cropped_image = f'data/{fname}'
    img.save(cropped_image)
    img.close()
    return cropped_image


def db_connect(db_file):
    try:
        conn = sqlite3.connect(db_file)
        create_table = """CREATE TABLE IF NOT EXISTS instaspam (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            image TEXT NOT NULL,
                            caption TEXT NULL,
                            published INTEGER NULL
                            );"""
        conn.execute(create_table)
        return conn
    except Error as e:
        print(e)
    return None


def check_text_data(conn, cur):
    with open('posts.txt') as f:
        text_posts = f.read()

    new_posts = 0
    n = '\n'
    for post in text_posts.split('---')[1:]:
        image = post.split(n)[0]
        caption = post.replace(image, '').replace(n * 2, n * 3).strip()
        image = image.strip()

        cur.execute(
            "SELECT * FROM instaspam WHERE image='{}' AND caption='{}';".format(image, caption))
        if not len(cur.fetchall()):
            conn.execute(
                "INSERT INTO instaspam (image, caption) VALUES (?, ?);", (image, caption))
            conn.commit()
            new_posts += 1

    return new_posts


def get_post(conn, cur, instauser, instapass):
    now = int(time.time())

    cur.execute(
        "SELECT * FROM instaspam WHERE published IS NULL ORDER BY ID LIMIT 1;")
    row = cur.fetchone()
    if row:
        id = row[0]
        image = row[1]
        caption = row[2]
        if not test_mode:
            image = crop_image(image)

        if instaspam(instauser, instapass, image, caption):
            conn.execute(
                "UPDATE instaspam SET published = {} WHERE id = {}".format(now, id))
            conn.commit()
            if not test_mode:
                os.remove(f'{image}.REMOVE_ME')

            print(f'Success!\n\n{image}\n{caption}')
        else:
            print(f'FAIL!\n\n{image}\n{caption}')

    else:
        if not check_text_data(conn, cur):
            print('ran out of posts')
        else:
            get_post(conn, cur, instauser, instapass)


def get_all_posts(cur):
    cur.execute("SELECT * FROM instaspam ORDER BY ID;")
    rows = cur.fetchall()
    for row in rows:
        print(row)


def delete_db(db_file):
    delete = input('Delete DB (Y/n)? ')
    if delete.lower() in ['y', 'ye', 'yes']:
        os.remove(db_file)
        print('DB deleted')
    quit()


def main():
    config = configparser.ConfigParser()
    config_file = 'data/conf.ini'
    db_file = 'data/posts.db'
    first_run = False

    if not os.path.isfile(config_file) or config_mode:

        while 1:
            instauser = input('Username: ')
            instapass = input('Password: ')
            if len(instauser) and len(instapass):
                save = input('Save (Y/n)? ')
                if save.lower() in ['y', 'ye', 'yes']:
                    break
                else:
                    quit()

        config.add_section('SETTINGS')
        config['SETTINGS']['instauser'] = instauser
        config['SETTINGS']['instapass'] = instapass
        with open(config_file, 'w+') as f:
            config.write(f)
        print('Login details saved')
        if not config_mode:
            first_run = True

    config.read(config_file)
    instauser = config['SETTINGS']['instauser']
    instapass = config['SETTINGS']['instapass']

    conn = db_connect(db_file)
    cur = conn.cursor()

    if delete_mode:
        delete_db(db_file)
    elif update_mode:
        new_posts = check_text_data(conn, cur)
        print(f'{new_posts} new posts')
    elif all_mode:
        get_all_posts(cur)
    elif first_run:
        new_posts = check_text_data(conn, cur)
        print(f'{new_posts} new posts')
        get_post(conn, cur, instauser, instapass)
    else:
        get_post(conn, cur, instauser, instapass)

    conn.close()


if __name__ == '__main__':
    main()
