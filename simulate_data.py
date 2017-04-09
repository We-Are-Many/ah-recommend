import MySQLdb
from random import randint as ri 
from random import uniform as rf

def connection():
    conn=MySQLdb.connect(host="localhost",user="root", passwd="utkarsh@mit", db="legion")
    cur= conn.cursor()
    return cur, conn

def simulate_data():
    cur, conn = connection()
    name = "FullName"
    username = "username"
    suffix = "@gmail.com"
    location = "location"
    talk_points = "I am an alcoholic"
    for i in xrange(500000):
        q_name = name + str(i)
        q_username = username + str(i)
        email = username + str(i) + suffix
        q_location = location + str(i%50)
        cur.execute("INSERT into user_details values(%s, %s, %s, %s, %s)", (q_username, q_name, email, q_location, talk_points))
        cur.execute("INSERT into user_prefs(user_name) values(%s)", (q_username))
        is_online = str(0)
        cur.execute("INSERT into online_users values(%s, %s)", (q_username, 0))
        cur.execute("INSERT into user_problems values(%s, %s)", (q_username, talk_points))

    conn.commit()
    conn.close()
    cur.close()

def modify_locations():
    cur, conn = connection()
    for i in xrange(500000):
        cur.execute("UPDATE user_details set location=%s where user_name=%s", (("location" + str(i%50)), ("username" + str(i))))
    conn.commit()
    conn.close()
    cur.close()

def simulate_problems():
    problem_list = ['I cannot control myself once I start drinking.', 
                    'I cannot complete a day without 2 bottles of vodka.',
                    'I get wasted every other day.',
                    'I feel like alcohol is taken over my life.',
                    'I cannot imagine my life without scotch.',
                    'I spend all my money on booze.',
                    'My wife will leave me if I don\'t give up drinking.',
                    'I really drink a lot.',
                    'I try to quit drinking but my friends won\'t let me.',
                    'I am alone because of my drinking habits.',
                    'I lost my friends due to my alcohol addiction.',
                    'My health has gone down because I drink too much.',
                    'I might have liver problems because of my drinking habit.',
                    'I just want to open up to someone about my booze addiction.',
                    'I don\'t understand why people have a problem with my drinking.',
                    'I drink more whiskey than I do water.'
                    ]
    return problem_list

def modify_bios():
    problem_list = simulate_problems()
    cur, conn = connection()
    for i in xrange(500000):
        try:
            x, y, z = random.randint(0,15), random.randint(0,15), random.randint(0,15)
            assert x != y != z
        except AssertionError:
            x, y, z = 0, 5, 10
        full_bio = [problem_list[x], problem_list[y], problem_list[z]]
        full_bio = ' '.join(full_bio)
        cur.execute("UPDATE user_details set talk_points=%s where user_name=%s", (full_bio, ("username" + str(i))))
    conn.commit()
    conn.close()
    cur.close


def add_feature_data():
    cur, conn = connection()
    for i in xrange(10):
        alcohol_ai = str(rf(1,200))
        positive = str(rf(1,150))
        negative = str(rf(1,20))
        extra = str(rf(1,300))
        user_name = "username" + str(i) 
        rating_count = str(ri(1,100))
        rating = str(rf(0,5))
        drink = str(ri(1,20))
        alcohol_bk = str(ri(1,20))
        bottle = str(ri(1,20))
        money = str(ri(1,20))
        quit = str(ri(1,20))
        addict = str(ri(1,20))
        problem = str(ri(1,20))
        health = str(ri(1,20))
        cur.execute("INSERT into acc_intents values(%s, %s, %s, %s, %s, %s, %s)", (user_name, alcohol_ai, positive, negative, extra, rating_count, rating))
        cur.execute("INSERT into bio_keywords values(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (user_name, drink, alcohol_bk, bottle, money, quit, addict, problem, health))
    conn.commit()
    cur.close()
    conn.close()



#simulate_data()
#modify_locations()
#modify_bios()
add_feature_data()