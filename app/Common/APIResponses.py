from typing import List
class Responses():

    # for success result
    def success_result(msg):
        context = {
            'result':True,
            'msg' : msg
        }
        return context

    # for failed result
    def failed_result(msg):
        context = {
            'result':False,
            'msg' : msg
        }
        return context 

    # success result with data
    def success_result_with_data(msg, data_name, data):
        context =  {
            'result' : True,
            'msg' : msg,
            data_name: data
        }
        return context
