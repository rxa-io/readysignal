import config
import configparser
import pymysql

config = configparser.ConfigParser()
config.read('config_local.py')

try:
    connection = pymysql.connect(    
        host=config['CREDENTIALS']['HOST'],
        user=config['CREDENTIALS']['USERNAME'],
        password=config['CREDENTIALS']['PASSWORD'],
        database='readysignal'
    )
    print('Connection to database successful.')
except pymysql.MySQLError as err:
    print("""Please set configuration parameters in readysignal/config_local.py, e.g.
                        PASSWORD = 'password1234'
                        USERNAME = 'johndoe'
                        HOST =  'host.url' """)
