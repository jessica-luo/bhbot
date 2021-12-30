import random
import lyricsgenius
import tweepy
import os
import re
import textwrap

api_keys = {
    'CONSUMER_KEY': os.getenv('CONSUMER_KEY'),
    'CONSUMER_SECRET': os.getenv('CONSUMER_SECRET'),
    'ACCESS_TOKEN': os.getenv('ACCESS_TOKEN'),
    'ACCESS_SECRET': os.getenv('ACCESS_SECRET'),
    'GENIUS_TOKEN': os.getenv('GENIUS_TOKEN'),
    'CENSOR': os.getenv('CENSOR')
}

song_file = open("songs.txt", "r")
read_songs = song_file.readlines()
songs = list(map(lambda s: s.strip(), read_songs))

def get_song_lyrics():
    genius = lyricsgenius.Genius(api_keys["GENIUS_TOKEN"])

    # choose random song from songs.txt
    rand_song = random.choice(songs)

    # remove punctuation from song
    remove_slashes = rand_song.replace('/', ' ')
    remove_extra_spaces = ' '.join(remove_slashes.split())
    song = re.sub(r'[^\w\s]', '', remove_extra_spaces).replace(' ', '-')

    # turn song into url 
    lyrics = genius.lyrics(None, 'https://genius.com/Brockhampton-' + song + '-lyrics', True)

    # remove footer
    lyrics_replace_footer = lyrics.replace("EmbedShare URLCopyEmbedCopy", "")
    lines = lyrics_replace_footer.split('\n')
    lines[-1] = re.sub('[0-9]+', '', lines[-1])

    # remove empty lines
    filtered_empty_lines = filter(lambda line: line != "", lines)

    # break lines at 140 characters
    shorten_lines = map(lambda line: textwrap.fill(line, width=140, break_long_words=False), filtered_empty_lines)
    filtered_lines = "\n".join(list(shorten_lines)).split("\n")

    # choose 2 random lines to tweet
    random_num = random.randrange(0, len(filtered_lines)-1)
    tweetable_lyric = filtered_lines[random_num] + "\n" + filtered_lines[random_num+1]
    tweetable_lyric = tweetable_lyric.replace("\\", "").replace(api_keys["CENSOR"], '****')

    return tweetable_lyric, rand_song

def main():
    auth = tweepy.OAuthHandler(
        api_keys['CONSUMER_KEY'],
        api_keys['CONSUMER_SECRET']
    )

    auth.set_access_token(
        api_keys['ACCESS_TOKEN'],
        api_keys['ACCESS_SECRET']
    )

    twitter = tweepy.API(auth)
    tweetable_lyric, song = get_song_lyrics()
    status = twitter.update_status(tweetable_lyric)
    bio = twitter.update_profile(description="@BRCKHMPTN LYRICS. CURRENTLY: " + song)

    return tweetable_lyric, song

main()
