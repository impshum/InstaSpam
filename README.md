## InstaSpam on PythonEverywhere

Daily postings to Instagram on PythonEverywhere.

![](title.jpg)

### Instructions

-   Create a free account on PythonEverywhere
-   Open up a bash console on PythonEverywhere
-   Run this script in the bash console you just opened on PythonEverywhere


    wget https://raw.githubusercontent.com/impshum/InstaSpam/master/install.sh && sh install.sh

-   Upload images to `images` folder
-   Fill out `posts.txt` with all your captions referencing your images
-   Schedule a task to run the daily script on PythonEverywhere


    python3 /home/YOURUSERNAME/run.py

### Posts 101

Make sure you keep to the format in posts.txt or you'll probably break everything.

    ---meta1.jpg
    Stuff 1

    ---meta2.jpg
    Stuff 2

    Down here!

    ---meta3.jpg
    Stuff 3

    Down here!

    #hashtags

    ---meta4.jpg
    Stuff 4

    Down here!

    And down here!

    #hashtags

### Script Help

-   Parses `posts.txt` and adds new posts to an SQLite database
-   Ignores duplicate captions
-   Works through posts until they've all been uploaded
-   `posts.txt` can be cleared and filled with new posts after update
-   Doesn't harm any kittens


    usage: run.py [-h] [-u] [-a] [-t] [-c] [-d]

    optional arguments:
      -h, --help    show this help message and exit
      -u, --update  Update from text file
      -a, --all     Print all DB
      -t, --test    Test mode
      -c, --config  Change user/pass
      -d, --delete  Delete DB

### Notes

If you lose your account it's on you!

* * *

BTC - 1AYSiE7mhR9XshtS4mU2rRoAGxN8wSo4tK
