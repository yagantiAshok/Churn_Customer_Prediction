

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
