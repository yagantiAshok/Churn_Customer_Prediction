

from pathlib import Path
import os 

project_name = "churn"

list_of_files=[


    f"{project_name}/__init__.py",
    f"{project_name}/config/__init__.py",
    f"{project_name}/config/scheame.yaml",
    f"{project_name}/config/model.yaml",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/confif_entity.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_training.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/pipeline/predicting_pipeline.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/externel_connections/__init__.py",
    f"{project_name}/externel_connections/connection.py",
    "Dockerfile",
    "setup.py",
    "app.py",
    "testing.py",
    ".dockerignore"


]



for filepath in list_of_files:

    path = Path(filepath)

    file_dir, file_name = os.path.split(path)


    if file_dir!="":
        
        os.makedirs(file_dir,exist_ok=True)
    
    if  (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):

        with open(filepath,"w") as file:

            pass
    else:

        print(f"file_path {filepath} alreay exists")

