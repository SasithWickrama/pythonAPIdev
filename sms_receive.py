import logging
import sys
import cx_Oracle
import smpplib.gsm
import smpplib.client
import smpplib.consts
from smpplib.command import SubmitSMResp
# if you want to know what's happening
logging.basicConfig(level='DEBUG')

client = smpplib.client.Client('10.68.198.100', 5019)

def dbconnOssRpt(self):
    try:
        hostname = '172.25.1.172'
        port = '1521'
        service = 'clty'
        user = 'OSSPRG'
        password = 'PRGOSS456'

        dsn_tns = cx_Oracle.makedsn(hostname, port, service_name=service)
        conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
        return conn
    except Exception as e:
        print("Exception : %s" % e)
        return e
            
    
def capture(msg, source_addr):
    source_addr= str(str(source_addr).replace("b", "")).replace("'", "")
    msg= str(str(msg).replace("b", "")).replace("'", "")
   
    print(str(source_addr)+' '+str(msg))
    conn = dbconnOssRpt(self="")
    c = conn.cursor()
    sql = "INSERT INTO OSSPRG.SMS_REPLYMSGS (RECEIVE_NO, RECEIVE_SMSMSG, RECEIVE_TIME,RECEIVE_ST) VALUES ( :RECEIVE_NO,:RECEIVE_SMSMSG,sysdate,:RECEIVE_ST)"
    with conn.cursor() as cursor:
        cursor.execute(sql, [source_addr, msg,"pybkend"])
        conn.commit()
  
       
             
def handle_deliver_sm(pdu):
    
    sys.stdout.write('delivered PDU {}\n'.format(pdu.short_message))
    sys.stdout.write('delivered PDU {}\n'.format(pdu.source_addr))
    capture(pdu.short_message,pdu.source_addr)
    return 0 # cmd status for deliver_sm_resp

client.set_message_received_handler(lambda pdu: handle_deliver_sm(pdu))

client.connect()
client.bind_transceiver(system_id='oss_in', password='QGH!8]np')

client.listen()

    


