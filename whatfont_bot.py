import praw
from fontrecog import font_recog
import time
import os
import pickle
from bs4 import BeautifulSoup
import requests
import argparse
from utils import load_commented, img_url_parser


def authenticate():
    """
    Basic PRAW auth
    """
    print('Starting Bot ....')
    print ('Authenticating ....')
    reddit = praw.Reddit('whatfontbot', user_agent = 'WhatFontBot ')

    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


# Mode 1
def summon_bot(reddit, subredd, commented):

    print("Analyzing comments on r/{}".format(subredd))
    for comment in reddit.subreddit(subredd).comments(limit= 25):
        if '!whatfont' in comment.body and comment.submission.id not in commented and comment.submission.is_video == False:
            post_url = comment.submission.url
            post_urlcheck = img_url_parser(post_url)
            parsed_selftext = img_url_parser(comment.submission.selftext_html)

            # check if submission link links to an image url
            if post_urlcheck != None:
                print(' \'!whatfont\' comment found in comment {} in image linked post {}.'.format(comment.id, comment.submission.id))
                img_url = post_url

                # bot_reply replies and returns updated commented list with already commented ids
                commented = bot_reply(comment, img_url, commented)

            # Check if submission selftext has a link to an image url
            elif parsed_selftext != None:
                print('!whatfont comment found in comment {} in regular text post {} ... '.format(comment.id, comment.submission.id))
                img_url = parsed_selftext

                #bot_reply replies and  returns updated commented list with already commented ids
                commented = bot_reply(comment, img_url, commented)

            # No image link was found anywhere
            else:
                print('No image found !!! ....')
                #maybe reply message with no image found


def bot_reply(comment, img_url, commented):

    # Font recognition using Whatfontis API
    recog_fonts = font_recog(img_url)

    #check if recognized fonts is an empty list or None.
    if recog_fonts :

        print('The fonts found are: {}'.format(', '.join(recog_fonts)))

        ## Comment
        message = "These are the most similar fonts I could find: {}.".format(', '.join(recog_fonts))
        message += "\n\n*** "
        message += "\n\n ^(I am a bot)"

        #I use [Whatfontis](https://www.whatfontis.com) API
        #and  you can  check my code [here](https://wwww.github.com/pggmrt/whatfont-bot)
        print("\n Posting comment ...")
        comment.reply(message)

        ##Write submission id to "commented" pickle
        commented.append(comment.submission.id)
        with open('commented.pkl', 'wb') as fp:
            pickle.dump(commented, fp)

        print( "Writing post ID to file")
    else:
        ## maybe reply message telling no fonts were found .

        print('No fonts could be found')
        print ("Writing post ID to file ....")
        ## Add submission id to the commented list to avoid returning here
        commented.append(comment.submission.id)
        with open('commented.pkl', 'wb') as fp:
            pickle.dump(commented, fp)

    # Return updated list of commented post ids
    return commented

# =====================================================

# Mode2
def autosearch_bot(reddit,subredd):

    #filter out r/depression r/suicidewatch
    #for submission in reddit.subreddit(subredd).search(search_query, sort="new", limit=11):
    ##etc

    return None
# etc.




# =============================================================================

def main():

    MODE = 1   # 1 or 2

    #CLI Parser
    ap =argparse.ArgumentParser()
    #ap.add_argument('-m', '--mode', required= True, help = 'Path to image')
    ap.add_argument('-s', '--sub', required=True, type=int, help= 'Subreddit')
    args = vars(ap.parse_args())

    # Start Bot
    reddit = authenticate()
    #subreddit = "bot_testing2"
    subreddit = args["sub"]
    commented = load_commented()
    while True :
        try:
            if MODE == 1:
                summon_bot(reddit, subreddit, commented)

            elif MODE == 2:
                autosearch_bot(reddit, subreddit, commented)

            print("sleeping for 30 seconds ...")
            time.sleep(30)

        except Exception as err:
            print ("Error found: {}".format(err))
            print ("\n Sleeping for 30 seconds now")
            time.sleep(30)


# =============================================================================
if __name__ == '__main__':
    main()
