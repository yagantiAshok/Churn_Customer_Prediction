
import os
import sys
from config_box import ConfigBox
from ensure import ensure_annotations
from churn.exception import CustomException
from churn.logger import logger
import numpy as np
import joblib
import yaml
from pathlib import Path
from typing import Any



@ensure_annotations

def read_yaml(file_path:str)->ConfigBox:

    try:

        with open(file_path,"r") as file:

            data = yaml.safe_load(file)
        
        data = ConfigBox(data)

        logger.info(f"yaml file {file_path} successfully loaded into config box Object")

        return data

    
    except Exception as e:

        raise CustomException(e,sys)

@ensure_annotations

def write_yaml(file_path:str,data:dict)->None:

    try:

        # dir_name = os.path.dirname(file_path)

        # os.makedirs(dir_name,exist_ok=True)

        Path(file_path).parent.mkdir(parents=True,exist_ok=True)


        with open(file_path,"w")  as file:

            yaml.dump(data,file,default_flow_style=False)
        
        logger.info(f" Succesfully data saved into yaml file {file_path}")

    except Exception as e:

        raise CustomException(e,sys)
    
@ensure_annotations

def save_data_to_numpy(file_path:str,data:Any)->None:

    try:

        Path(file_path).parent.mkdir(parents=True,exist_ok=True)


        np.save(file_path,data)

        logger.info(f"saved data into numpy format {file_path}")

    except Exception as e:

        raise CustomException(e,sys)


@ensure_annotations

def extract_data_from_nuumpy(file_path:str)->np.ndarray:

    try:

        data = np.load(file_path)
        
        logger.info(f"Collected numpy data {file_path}")
        
        return data
    
    except Exception as e:

        raise CustomException(e,sys)

@ensure_annotations
def save_model(file_path:str,data:Any)->None:

    try:

        Path(file_path).parent.mkdir(parents=True,exist_ok=True)


        joblib.dump(data,filename=file_path)
        
        logger.info(f"Model saved at {file_path}")

    
    except Exception as e:

        raise CustomException(e,sys)
    
@ensure_annotations
def load_model(file_path:str)->Any:

    try:

        data = joblib.load(file_path)
        
        logger.info(f"Model loaded from {file_path}")
        
        return data
        
    except Exception as e:

        raise CustomException(e,sys)
    

@ensure_annotations

def create_directories(folders:list[str],verbose:True)->None:

    for folder in folders:

        try:
            path = Path(folder)

            path.mkdir(parents=True,exist_ok=True)
            
            if verbose:

                logger.info(f"File created at {folder}")
        
        except Exception as e:

            raise CustomException(e,sys)

@ensure_annotations

def create_folder_path(folder:str):

    try:

        path = Path(folder)

        path.parent.mkdir(parents=True,exist_ok=True)

        logger.info(f"Fodler is created at {folder}")


    except Exception as e:
        raise CustomException(e,sys)