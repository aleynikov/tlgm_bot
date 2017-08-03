from gmusicapi import Mobileclient
import config


class Client(object):
    def __init__(self):
        self.client = Mobileclient()
        self.client.login(config.gmusic['email'], config.gmusic['password'], Mobileclient.FROM_MAC_ADDRESS)

    def search_songs(self, query_str):
        song_hits = self.client.search(unicode(query_str), 8)['song_hits']
        songs = []
        for song_hit in song_hits:
            songs.append({
                'title': song_hit['track']['title'],
                'artist': song_hit['track']['artist'],
                'album': song_hit['track']['album'],
                'nid': song_hit['track']['nid']
            })

        return songs

    def get_song_url(self, song_nid):
        song_id = 'T{0}'.format(song_nid)
        return self.client.get_stream_url(song_id)