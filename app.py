


import sys
from churn.logger import logger
from churn.exception import CustomException
from churn.entity.config_entity import (DataIngestionConfig,
                                        DataValidationConfig,
                                        DataTransformationConfig)

from churn.pipeline.training_pipeline import TrainingPipeline


try:

    logger.info("Entered into Training Pipeline")

    obj = TrainingPipeline(
        data_ingestion_config=DataIngestionConfig,
        data_validation_config=DataValidationConfig,
        data_transformation_config=DataTransformationConfig
    )

    obj.run_pipeline()

    logger.info("Training Pipeline completed")


except Exception as e:

    raise CustomException(e,sys)