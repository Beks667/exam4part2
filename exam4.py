import config 
import psycopg2


def executor(method):
    def wrapper (*args,**kwargs):
        args[0].cursor = args[0].connection.cursor()
        rec = method(*args,**kwargs)
        args[0].cursor.close()
        return rec

    return wrapper


class DbConnection:
    def __init__(self):
        self.connection = psycopg2.connect(dbname = config.DBNAME,user=config.USER,password = 'password123',port = config.PORT)
        self.connection.autocommit = True
        self.create_table()

    @executor
    def CreateTable(self):
        try:
            create_table_command = "CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, username VARCHAR (50) UNIQUE, name varchar(100), age integer NOT NULL)"
            self.cursor.execute(create_table_command)
        except:
            print("table creation failed or table already exists")

    @executor
    def all(self):
        query_command="SELECT * FROM users;"
        self.cursor.execute(query_command)
        users = self.cursor.fetchall()
        return users
    
    @executor
    def get(self, par):
        find_command = f"SELECT * FROM users WHERE {par};"
        self.cursor.execute(find_command)
        found_record = self.cursor.fetchall()
        return found_record

    @executor
    def filter(self, par):
        filter_command = f"SELECT * FROM users ORDER BY {par}"
        self.cursor.execute(filter_command)
        found_record = self.cursor.fetchall()
        return found_record


class CharField:
    def __init__(self,char,max_len):
        self.char = char 
        self.max_len = max_len
        if len(char)>max_len:
            raise Exception(f'Length must be less then{self.max_len}')
        
    def __str__(self):
        return self.char

class TextField:
    def __init__(self,text):
        self.text = text

    def __str__(self):
        return self.text

class IntegerField:
    def __init__(self,intgr):
        self.int = intgr
        if not isinstance(intgr,int):
            raise ValueError('Value must be integer')

class User:
    def __init__(self,user,name,age):
        self.user = CharField(user,max_len=50)
        self.name = CharField(name,max_len=50)
        self.age = IntegerField(age)
        self.posts = []
    
    def __str__(self):
        return self.user

class Post:
    def __init__(self,title,body,author):
        self.title = CharField(title, max_length=10)
        self.body = TextField(body)
        self.author = author
        self.author.posts.append(self)
    
    def __str__(self):
        return f'Author: {self.author}\nTitle: {self.title}\n{self.body}'

if __name__ =='__name__':
    db = DbConnection()
    print(db.all())
    print(db.filter('name'))
    print(db.get('id=1'))