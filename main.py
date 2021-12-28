import random
import lyricsgenius
import tweepy
import os

api_keys = {
    'CONSUMER_KEY': os.getenv('CONSUMER_KEY'),
    'CONSUMER_SECRET': os.getenv('CONSUMER_SECRET'),
    'ACCESS_TOKEN': os.getenv('ACCESS_TOKEN'),
    'ACCESS_SECRET': os.getenv('ACCESS_SECRET'),
    'GENIUS_TOKEN': os.getenv('GENIUS_TOKEN')
}

songs = ["ENCINO", "BEN CARSON", "MICHIGAN", "INFATUATION", "BREAKFAST", "MOSSCLIFF", 
"CONTACTS", "PALACE", "FLIP MO", "HOME", "COTTON HOLLOW", "POISON", "LOST IN LOVE", 
"HEAT", "GOLD", "STAR", "BOYS", "2PAC", "FAKE", "BANK", "TRIP", "SWIM", "BUMP", "CASH", 
"MILK", "FACE", "WASTE", "GUMMY", "QUEER", "JELLO", "TEETH", "SWAMP", "TOKYO", "JESUS", 
"CHICK", "JUNKY", "FIGHT", "SWEET", "GAMBA", "SUNNY", "SUMMER", "BOOGIE", "ZIPPER", 
"JOHNNY", "LIQUID", "STUPID", "BLEACH", "ALASKA", "HOTTIE", "SISTER/NATION", "RENTAL", 
"STAINS", "TEAM", "1999 WILDFIRE", "1998 TRUMAN", "1997 DIANA", "NEW ORLEANS", "THUG LIFE", 
"BERLIN", "SOMETHING ABOUT HIM", "WHERE THE CASH AT", "WEIGHT", "DISTRICT", "LOOPHOLE", 
"TAPE", "J'OUVERT", "HONEY", "VIVID", "SAN MARCOS", "TONYA", "FABRIC", "NO HALO", "SUGAR", 
"BOY BYE", "HEAVEN BELONGS TO YOU", "ST. PERCY", "IF YOU PRAY RIGHT", "DEARLY DEPARTED", 
"I BEEN BORN AGAIN", "GINGER", "BIG BOY", "LOVE ME FOR LIFE", "VICTOR ROBERTS", "BUZZCUT", 
"CHAIN ON", "COUNT ON ME", "BANKROLL", "THE LIGHT", "WINDOWS", "I'LL TAKE YOU ON", 
"OLD NEWS", "WHAT'S THE OCCASION?", "WHEN I BALL", "DON'T SHOOT UP THE PARTY", "DEAR LORD", 
"THE LIGHT PT. II", "PRESSURE / BOW WOW", "SEX", "JEREMIAH (RMX)", "JEREMIAH (ORIGINAL)", 
"CANNON", "Dirt", "MVP"]

def get_song_lyrics():
    genius = lyricsgenius.Genius(api_keys["GENIUS_TOKEN"])
    song = random.choice(songs)
    lyrics = genius.search_song(song, "BROCKHAMPTON").lyrics
    lines = lyrics.split('\n')

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