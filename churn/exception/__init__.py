

import sys


def error_details__(error_message,error_details:sys):

    _,_,exc_tb = error_details.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno

    message = f"Error Occured in Script [{file_name}] and line number [{line_no}] and error meassage is [{str(error_message)}]"

    return message

class CustomException(Exception):

    def __init__(self,error,error_details:sys):

        super().__init__(error)

        self.error_detailed_message = error_details__(error_message=error,error_details=error_details)

    def __str__(self):

        return self.error_detailed_message

