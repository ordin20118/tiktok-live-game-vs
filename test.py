import json


test_str = '{"code":1,"user_id":"6991823491326886914","unique_id":"haneul22222","nickname":"하늘2","comment":"아 형 미안해","profile_img":"https://p16-sign-sg.tiktokcdn.com/aweme/100x100/tos-alisg-avt-0068/92097a0350690f1167e752a0db17c7c6.webp?x-expires=1666069200&x-signature=cWO%2FJAEgQmANxYae%2ByTYWjfUiWk%3D"}'


try:
    msg_obj = json.loads(test_str)
    print("[[ Message Object ]]")                    
    print(msg_obj)
except Exception as e:
    print("[error]:%s" % e)
    raise