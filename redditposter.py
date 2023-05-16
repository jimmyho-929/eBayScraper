import praw
import time

# create the Reddit client
reddit = praw.Reddit(client_id='LUn27nTVIoFYJFm36tG_Rg',
                     client_secret='o01WQeaxLx4Ks3kw_fnBUJwBTveWIg',
                     user_agent='howmuchdoyoulovemeonascaleof0to1', #originally initialized as howmuchdoyoulovemeonascaleof10o1 accidentally
                     username='nicetomeetyou2021',
                     password='') #use the existing password

# choose the subreddit
subreddit = reddit.subreddit('RedditWritesSeinfeld')

# create the message
title = "Ever notice how your dog's behavior changes when you put on different shoes?"
text = "You're at home in your slippers, your dog is relaxed: slippers mean bedtime. But you put on your running shoes, and its go-time. Something's up- maybe play-time. It's like they have a sixth sense for shoes. But you put on your dress shoes, and your dog looks at you like you've betrayed them. Where are you going without me? And then you leave, and they're at the window, staring out, contemplating their existence. It's like, Hey, I'm just going to work. You know, the place that pays for your kibble. But they don't get it. To them, shoes are the window to the soul. Or rather, the door to the outside. And it's not just dogs. Cats? They don't care. You could be wearing clown shoes and they'd still just look at you with that judgmentalstare, like, Do you have any idea how ridiculous you look? It's a whole different world, folks. Shoe-world. Where the type of shoe you wear determines your whole relationship with your pet. It's a tough walk to tread."

# post the message
subreddit.submit(title, selftext=text)

# sleep for 24 hours
time.sleep(24 * 60 * 60)
