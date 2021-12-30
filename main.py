import random
import lyricsgenius
import tweepy
import os
import re

api_keys = {
    'CONSUMER_KEY': os.getenv('CONSUMER_KEY'),
    'CONSUMER_SECRET': os.getenv('CONSUMER_SECRET'),
    'ACCESS_TOKEN': os.getenv('ACCESS_TOKEN'),
    'ACCESS_SECRET': os.getenv('ACCESS_SECRET'),
    'GENIUS_TOKEN': os.getenv('GENIUS_TOKEN')
}

song_file = open("songs.txt", "r")
read_songs = song_file.readlines()
songs = list(map(lambda s: s.strip(), read_songs))

def get_song_lyrics():
    genius = lyricsgenius.Genius(api_keys["GENIUS_TOKEN"])
    song = random.choice(songs)
    lyrics = genius.search_song(song, "BROCKHAMPTON").lyrics.replace("EmbedShare URLCopyEmbedCopy", "")
    lines = lyrics.split('\n')
    lines[-1] = re.sub('[0-9]+', '', lines[-1])

    filtered_empty_lines = filter(lambda line: line != "", lines)
    filtered_verse_titles = filter(lambda line: "[" not in line, filtered_empty_lines)
    filtered_lines = list(filtered_verse_titles)

    random_num = random.randrange(0, len(filtered_lines)-1)
    tweetable_lyric = filtered_lines[random_num] + "\n" + filtered_lines[random_num+1]
    tweetable_lyric = tweetable_lyric.replace("\\", "")

    return tweetable_lyric, song

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