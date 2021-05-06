import psutil
import time
import sqlite3
import config
import threading


def dbExecute(in_mb,out_mb,start_time,end_time):
    conn = sqlite3.connect(config.set_sqldb_name)
    cur = conn.cursor()
    sql = 'INSERT INTO network_usage_data(in_mb,out_mb,start_time,end_time) VALUES (?,?,?,?)'
    # cur.execute(sql,(1,0.23,'2020-04-01 00:00:00.000', '2020-04-01 00:00:00.000'))
    cur.execute(sql,(in_mb,out_mb,start_time,end_time)) 
    conn.commit() 
    conn.close()

def net_usage(inf = config.set_eth_name): #change the inf variable according to the interface
    
    net_stat = psutil.net_io_counters(pernic=True)[inf]
    net_in_1 = net_stat.bytes_recv
    net_out_1 = net_stat.bytes_sent
    start_time = time.localtime()
    start_time_str = "%04d/%02d/%02d %02d:%02d:%02d" % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec)
    time.sleep(config.set_time) ## TIME SETTING 1 = 1SEC
    net_stat = psutil.net_io_counters(pernic=True)[inf]
    net_in_2 = net_stat.bytes_recv
    net_out_2 = net_stat.bytes_sent
    net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
    net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)
    end_time = time.localtime()
    end_time_str = "%04d/%02d/%02d %02d:%02d:%02d" % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec)
    dbExecute(net_in,net_out,start_time_str,end_time_str)
    # print(f"Current net-usage:\nIN: {net_in} MB/s, OUT: {net_out} MB/s")
    


def dbCreate():
    conn = sqlite3.connect(config.set_sqldb_name) 
    cur = conn.cursor() 
    conn.execute('CREATE TABLE network_usage_data(id INTEGER PRIMARY KEY AUTOINCREMENT, in_mb REAL, out_mb REAL, start_time TEXT, end_time TEXT)') 
    # cur.executemany( 'INSERT INTO network_usage_data VALUES (?, ?, ?, ?, ?)', 
    #                 [
    #                     (1001, 1, 0.23,'2020-04-01 00:00:00.000', '2020-04-01 00:00:00.000'),
    #                     (1001, 0.12, 0.23,'2020-04-01 00:00:00.000', '2020-04-01 00:00:00.000'), 
    #                     (1001, 0.12, 0.23,'2020-04-01 00:00:00.000', '2020-04-01 00:00:00.000'),  
    #                     (1001, 0.12, 0.23,'2020-04-01 00:00:00.000', '2020-04-01 00:00:00.000'), 
    #                     (1001, 0.12, 0.23,'2020-04-01 00:00:00.000', '2020-04-01 00:00:00.000'), 
                        
    #                 ] 
    #                 ) 
    conn.commit() 
    conn.close()

    
    
def selete():
    conn = sqlite3.connect(config.set_sqldb_name) 
    cur = conn.cursor() 
    cur.execute("SELECT * FROM network_usage_data") 
    rows = cur.fetchall() 
    for row in rows: 
        print(row) 
    conn.close()

while True:
    try:
        dbCreate()
        net_usage()
        selete()
    except:
        net_usage()
        selete()
