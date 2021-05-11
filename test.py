
import configparser
 
config = configparser.ConfigParser()
config.read('./config.ini',encoding='UTF8')
# print(config.items)
print("config['AAA']['BBB'] : " + config['KeyList']['set_time'])

# print("config['KeyList']: " + config['KeyList'])
