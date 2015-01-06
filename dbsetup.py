#dbsetup.py
#Michael Kaminsky

import sqlite3
import os.path

class DBSetup(object):
    """
    Class to serve as a container for setting up the db for the rap generator
    """
    def __init__(self):

        print "DBSetup object created"
        defaultloc = "/usr/local/sqlite"

    def DBDestroy(self, dbloc = None):
        """
        Method to destroy existing sqlite database
        """
    
        defaultloc = "/usr/local/sqlite"

        if dbloc is None:
            if os.path.exists(defaultloc + '/rapgenerator.db'):
                os.remove(defaultloc + '/rapgenerator.db')
                return "Database " + defaultloc + '/rapgenerator.db' + " successfully destroyed"
            else:
                return "No rapgenerator.db database at "+ defaultloc
        else:
            if os.path.exists(dbloc + '/rapgenerator.db'):
                os.remove(dbloc + '/rapgenerator.db')
                return "Database " + dbloc + '/rapgenerator.db' + " successfully destroyed"
            else:
                return "No rapgenerator.db database at "+ dbloc

    def DBCreate(self, dbloc = None):
        """
        Method to create a new database.
        Check to see if the db exists already. If not, create it.
        """
    
        defaultloc = "/usr/local/sqlite"

        if dbloc is None:
            print("No dbloc provided. Creating db at " + defaultloc)
            if not os.path.exists(defaultloc):
                os.makedirs(defaultloc)
                conn=sqlite3.connect(defaultloc+'/rapgenerator.db')


                print "Database created and opened succesfully at " + defaultloc + 'rapgenerator.db'
            else:
                if not os.path.exists(defaultloc+'/rapgenerator.db'):
                    conn=sqlite3.connect(defaultloc+'/rapgenerator.db')
                    print "Database created and opened succesfully"
                else:
                    return "ERROR: A rapgenerator db already exists at " + defaultloc
        else:
            if not os.path.exists(dbloc):
                os.makedirs(dbloc)
                conn=sqlite3.connect(dbloc+'/rapgenerator.db')
                print "Database created and opened succesfully"
            else:
                if not os.path.exists(dbloc+'/rapgenerator.db'):
                    conn=sqlite3.connect(dbloc+'/rapgenerator.db')
                    print "Database created and opened succesfully"
                else:
                    return "ERROR: A rapgenerator db already exists at " + dbloc

        conn.text_factory = str
        c = conn.cursor()
        c.execute(' DROP TABLE IF EXISTS songs; ')
        c.execute(' CREATE TABLE songs (id integer primary key, title text, artist text); ')
        c.execute(' DROP TABLE IF EXISTS lyrics; ')
        c.execute(' CREATE TABLE lyrics (id integer primary key, title_id integer, lyrics text, lastword text, rhymesyls text); ')
        conn.close()
