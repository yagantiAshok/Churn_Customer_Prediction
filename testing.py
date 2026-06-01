



# import os 

# path = "ashok"

# print(os.path.dirname(path))

# print(os.path.getsize("notebook/app.py"))
import sys

from churn.logger import logger

from churn.exception import CustomException

logger.info("Exception handling")

try:

    a = 1

    b = 0

    print(a/b)

except Exception as e:
    raise CustomException(e,sys)


        


