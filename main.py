# import pymongo

# # Provide the mongodb localhost url to connect python to mongodb.
# client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

# # Database Name
# dataBase = client["neurolabDB"]

# # Collection  Name
# collection = dataBase['Products']

# # Sample data
# d = {'companyName': 'iNeuron',
#      'product': 'Affordable AI',
#      'courseOffered': 'Machine Learning with Deployment'}

# # Insert above records in the collection
# rec = collection.insert_one(d)

# # Lets Verify all the record at once present in the record with all the fields
# all_record = collection.find()

# # Printing all records present in the collection
# for idx, record in enumerate(all_record):
#      print(f"{idx}: {record}")

from default.logger import logging
from default.exception import DefaultException
from default.utils import get_collection_as_dataframe
import sys,os
from default.entity import config_entity,artifact_entity
from default.components.data_ingestion import DataIngestion
from default.components.data_validation import DataValidation
from default.components.model_evaluation import ModelEvaluation
from default.components.model_trainer import ModelTrainer
from default.components.model_pusher import ModelPusher
from default.components.data_transformation import DataTransformation



if __name__=="__main__":
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()
          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          print(data_ingestion.initiate_data_ingestion())
          data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
          print("************starting data validation***********")
          
          # data validation
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
          data_validation_artifact=data_validation.initiate_data_validation()
          print("************ data validation completed***********")

          # data transformation
          data_transformation_config=config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation=DataTransformation(data_transformation_config=data_transformation_config, data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact=data_transformation.initiate_data_transformation()


         
           # model trainer
          print("************starting model training***********") 
          model_trainer_config =config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
          model_trainer= ModelTrainer(model_trainer_config=model_trainer_config,
           data_transformation_artifact=data_transformation_artifact)
          model_trainer_artifact=model_trainer.initiate_model_trainer()
          print("************model training completed***********")


          # model evaluation
          print("************starting model evaluation***********")
          model_eval_config =config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
          model_eval= ModelEvaluation(model_eval_config=model_eval_config,
           data_ingestion_artifact=data_ingestion_artifact,
            data_transformation_artifact=data_transformation_artifact, 
            model_trainer_artifact=model_trainer_artifact)
          model_eval_artifact=model_eval.initiate_model_evaluation()
          print("************ model evaluation completed***********")


          # model pusher
          print("************pushing model***********")
          model_pusher_config=config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
          model_pusher=ModelPusher(model_pusher_config=model_pusher_config,
          data_transformation_artifact=data_transformation_artifact,
          model_trainer_artifact=model_trainer_artifact)
          model_pusher_artifact=model_pusher.initiate_model_pusher()
          print("************model pushing completed***********")

     except Exception as e:
          print(e)     

from default.pipeline.training_pipeline import start_training_pipeline
from default.pipeline.batch_prediction import start_batch_prediction

file_path="/config/workspace/UCI_Credit_Card.csv"
print(__name__)
if __name__=="__main__":
     try:
          #start_training_pipeline()
          output_file = start_batch_prediction(input_file_path=file_path)
          print(output_file)
     except Exception as e:
          print(e)
