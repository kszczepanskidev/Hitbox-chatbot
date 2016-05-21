def clear_song_name(song):
    song = song.replace('&apos;', '\'')
    song = song.replace('&amp;', '&')
    song = song.replace('- Lyrics', '')

    song = song.replace('[OFFICIAL]', '')
    song = song.replace('[OFFICIAL VIDEO]', '')
    song = song.replace('[OFFICIAL MUSIC VIDEO]', '')

    song = song.replace('[Official]', '')
    song = song.replace('[Official Video]', '')
    song = song.replace('[Official Music Video]', '')

    song = song.replace('[Lyrics]', '')
    song = song.replace('[Lyrics Video]', '')
    song = song.replace('[Lyrics]', '')
    song = song.replace('[Lyrics video]', '')

    song = song.replace('[ORIGINAL]', '')
    song = song.replace('[ORIGINAL VIDEO]', '')
    song = song.replace('[ORIGINAL MUSIC VIDEO]', '')

    song = song.replace('[Original]', '')
    song = song.replace('[Original Video]', '')
    song = song.replace('[Original Music Video]', '')
    song = song.replace('[Uncensored]', '')

    song = song.replace('(OFFICIAL)', '')
    song = song.replace('(OFFICIAL VIDEO)', '')
    song = song.replace('(OFFICIAL MUSIC VIDEO)', '')

    song = song.replace('(Official)', '')
    song = song.replace('(Official Video)', '')
    song = song.replace('(Official Music Video)', '')

    song = song.replace('(Lyrics)', '')
    song = song.replace('(Lyrics Video)', '')
    song = song.replace('(Lyrics)', '')
    song = song.replace('(Lyrics video)', '')

    song = song.replace('(ORIGINAL)', '')
    song = song.replace('(ORIGINAL VIDEO)', '')
    song = song.replace('(ORIGINAL MUSIC VIDEO)', '')

    song = song.replace('(Original)', '')
    song = song.replace('(Original Video)', '')
    song = song.replace('(Original Music Video)', '')
    song = song.replace('(Uncensored)', '')
    return song
