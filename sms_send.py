import logging
import sys

import smpplib.gsm
import smpplib.client
import smpplib.consts
from smpplib.command import SubmitSMResp
# if you want to know what's happening
logging.basicConfig(level='DEBUG')

text= """ඔබට සුභ දවසක්  
තොරතුරු තාක්ෂණ පර්ෂදය
"""

# Two parts, GSM default / UCS2, SMS with UDH
parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(u'helloo')

client = smpplib.client.Client('10.68.198.100', 5019)

# Print when obtain message_id
client.set_message_sent_handler(
    lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.__dict__)))
    
          
# Handle delivery receipts (and any MO SMS)
def handle_deliver_sm(pdu):
        sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id))
        sys.stdout.write('delivered {}\n'.format(pdu.__dict__))
        return 0 # cmd status for deliver_sm_resp

client.set_message_received_handler(lambda pdu: handle_deliver_sm(pdu))

client.connect()
client.bind_transceiver(system_id='oss', password='MabL@z8/')


for part in parts:
    pdu = client.send_message(
        source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
        source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
        # Make sure it is a byte string, not unicode:
        source_addr='SLTMOBITEL',

        dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
        dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        # Make sure these two params are byte strings, not unicode:
        destination_addr='0710959907',
        short_message=part,

        data_coding=encoding_flag,
        esm_class=msg_type_flag,
        registered_delivery=True,
    )
    print(pdu.sequence)
    print(pdu.status)
    print(pdu.sm_length)
    
# Enters a loop, waiting for incoming PDUs

client.listen()

    


