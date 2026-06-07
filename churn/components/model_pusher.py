

import sys
from churn.logger import logger
from churn.exception import CustomException
from churn.entity.s3_estimator import s3estimator
from churn.entity.config_entity import ModelPusherConfig
from churn.entity.artifact_entity import ModelPusherArtifact,ModelEvaluationArtifact


class ModelPusher:

    def __init__(self,model_pusher_config:ModelPusherConfig,
                      model_evalutaion_artifact:ModelEvaluationArtifact,
                      s3_estimator = s3estimator):
        
        self.model_pusher_config = model_pusher_config
        self.model_evaluation_artifcat = model_evalutaion_artifact

        self.s3_estimator :s3estimator  = s3_estimator(bucket_name=self.model_pusher_config.bucket_name,model_path=self.model_pusher_config.s3_key_path)


    
    def initiate_model_pusher(self)->ModelPusherArtifact:

        try:

            logger.info("Entered into initiate model pusher function")

            
            # upload model in aws s3 bucket

            self.s3_estimator.savemodel(from_file=self.model_evaluation_artifcat.trained_model_path,to_filename=self.model_pusher_config.s3_key_path)


            model_pusher_artifact = ModelPusherArtifact(
                bucket_name= self.model_pusher_config.bucket_name,
                s3_key_name= self.model_pusher_config.s3_key_path
            )

            return model_pusher_artifact


        except Exception as e:

            raise CustomException(e,sys)

