

from dataclasses import dataclass



@dataclass
class DataIngestionArtifact:

    raw_file_path:str
    train_file_path:str
    test_file_path:str


@dataclass
class DataValidationArtifact:

    validation_status:bool
    drift_report_file_path :str
    drft_status:bool

@dataclass

class DataTransformationArtifact:

    preprocess_file_path : str 
    trasformed_train_file_path : str 
    transformed_test_file_path : str 

@dataclass
class ModelTrainerArtifcat:

    fl_score:float
    recall:float
    precision:float
    model_trained_obj_path:str
    accuracy_score:float