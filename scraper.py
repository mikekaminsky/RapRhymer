#scraper.py
execfile("dbupdate.py")
execfile("dbsetup.py")


#db = DBSetup()
#db.DBDestroy()
#db.DBCreate()

db = DBUpdate()

ArtistList = [
            'RZA',
            'GZA',
            'wu tang clan',
            'nicki minaj',
            'big sean',
            'lupe fiasco',
            'future',
            'andre 3000',
            'kendrick lamar',
            'schoolboy q',
            'eminem',
            'wiz khalifa',
            'nas',
            'rick ross',
            ]

db.AddSongs(ArtistList)
db.AddLyrics()
