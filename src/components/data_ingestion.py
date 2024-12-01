import os
import sys
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str= os.path.join("artifcats","train.csv")
    test_data_path: str= os.path.join("artifcats","test.csv")
    raw_data_path: str= os.path.join("artifcats","data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    def initiate_data_ingestion(self):
        logging.info("Entred the data ingestion Componenet or method")
        try:
            df = pd.read_csv("notebook\data\stud.csv")
            logging.info("Read The data set as DataFrame")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train Test Split initiated")

            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion is completed")

            return (
                self.ingestion_config.train_data_path, 
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
