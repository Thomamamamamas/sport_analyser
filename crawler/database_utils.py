import mysql
import platform
import mysql.connector

class Db():
    def __init__(self):
        if platform.system() == 'Darwin':
            self.passwd = 'Zbeubzbeub'
        elif platform.system() == 'Windows':
            self.passwd = '12345'
        self.host = "localhost"
        self.username = "root"
        
        self.database = 'football'

def connect_to_database(s_db):
    
    try:
        db = mysql.connector.connect(
            host = s_db.host,
            user = s_db.username,
            passwd = s_db.passwd,
            database= s_db.database
        )
        print("Connection à la base de données réussie")
        return db
    except:
        print("Connection à la base de données échouée")
        return None

def truncate_table(db, s_db, table_name):
    if db == None:
        db = connect_to_database(s_db)
    cursor = db.cursor()
    cursor.execute("TRUNCATE TABLE %s" % (table_name))
    db.commit()
    cursor.close()

def drop_table(db, s_db, table_name):
    if db == None:
        db = connect_to_database(s_db)
    cursor = db.cursor(buffered=True)
    try:
        cursor.execute("DROP TABLE IF EXISTS %s" % (table_name))
    except:
        print("Can't drop %s because table doesn't exist" % (table_name))
    db.commit()
    cursor.close()

def configure_table(db, s_db, table_name, column_name):
    if db == None:
        db = connect_to_database(s_db)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (table_name, column_name[0]))
    for i in range(1, len(column_name)):
        try:
            if 'FOREIGN KEY' in column_name[i]:
                cursor.execute("ALTER TABLE %s ADD %s" % (table_name, column_name[i]))
            else:
                cursor.execute("ALTER TABLE %s ADD COLUMN %s" % (table_name, column_name[i]))  
            db.commit()
        except:
            print("Column %s déjà créer dans la table %s, arret de la configuration de la table ..." % (column_name[i], table_name))
            db.commit()
            break
    db.commit()
    cursor.close()

def database_fetchone(cursor, procedure):
    data = 0
    
    cursor.execute(procedure)
    try:
        data = cursor.fetchone()[0] 
    except:
        data = 0
    return data

def database_fetchall(cursor, procedure):
    data = []

    cursor.execute(procedure)
    try:
        tmp = cursor.fetchall()
        for i in range(len(tmp)):
            data.append(tmp[i][0])
    except:
        print("LA requete ne renvoie rien")
    return data


def database_fetchall_everything(cursor, procedure):
    data = []

    cursor.execute(procedure)
    try:
        data = cursor.fetchall()
    except:
        print("LA requete ne renvoie rien")
    return data

def database_execute_many(cursor, procedure, procedure_data):
    data = []
    cursor.executemany(procedure, procedure_data)
    try:
        print(cursor.fetchmany(42))
        data = cursor.fetchmany(42)
    except:
        print("LA requete ne renvoie rien")
    return data