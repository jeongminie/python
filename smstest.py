# import requests

# def send_sms(sms_data):
 	
#     # 발급 받은 유저 아이디 대신 넣기
#     user_id = sms_data['user_id']
    
#     # 발급 받은 시크릿 코드 넣기
#     secure = sms_data['secure']
    
#     # 보내는 사람 폰 번호 : cafe24에서 발신번호 인증 받아야 사용 가능
#     ad = sms_data['operatorInfo']['phoneNumber']
    
#     # 받는 사람 폰 번호 
#     rphone = sms_data['advertiserInfo']['phoneNumber']

#     host = 'https://sslsms.cafe24.com/sms_sender.php'
#     msg = sms_data['msg']
#     # msg_url = sms_data['msg_url']
#     # link_id = sms_data['link_id']
#     ad_arr = ad.split('-')
#     # msg_url = msg_url + link_id


#     if (len(ad_arr) > 0):
#         sphone1 = ad_arr[0]
#         sphone2 = ad_arr[1]
#         sphone3 = ad_arr[2]

#         value = (msg)

#         params = {
#             'user_id': user_id,
#             'secure': secure,
#             'mode': '1',
#             'sphone1': sphone1,
#             'sphone2': sphone2,
#             'sphone3': sphone3,
#             'rphone': rphone,
#             'smsType': 'L',
#             'msg': value,
#             'testflag':'Y'
#         }
#         #
#         #보내긔!!!
#         print(params)
#         # result = requests.post(host, params)

#         data = {}
#         for key, value in params.items():
#             if isinstance(value, str):
#                 value = value.encode('euckr')
#                 if key == 'msg':
#                     value = value[:90].decode('euckr', 'ignore').encode('euckr')
#             data[key] = value
            
#         response = requests.post(host, params)
     
#     print(response)
#     return response

# sms_data = {
#     'user_id': 'jeongminie',
#     'secure': 'c2ba3351ce861875ea59562350ec07c9',
#     'operatorInfo': {
#     'phoneNumber': '010-2511-6861'
# },
#   'advertiserInfo': {
#   		'phoneNumber': '010-2511-6861'
#   },
#     'msg': 'test'
# }

# send_sms(sms_data)

import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP
if __name__ == "__main__":

    # set api key, api secret
    api_key = "NCSRFMHDTQYIKPZP"
    api_secret = "PXNQNRPPTFIG6HTWL6XOH5GTC34SKDLV"

    ## 4 params(to, from, type, text) are mandatory. must be filled
    params = dict()
    params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
    params['to'] = '01025116861' # Recipients Number '01000000000,01000000001'
    params['from'] = '01025116861' # Sender number
    params['text'] = 'test' # Message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()