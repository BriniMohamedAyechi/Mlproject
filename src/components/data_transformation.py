import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.utils import save_object


@dataclass
class DataTransformationConfig:    
    preprocessor_obj_file_path = os.path.join('artifcats',"preporcessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This function is responsible for data Transformation
        """
        try:
            num_features=['reading_score', 'writing_score']
            cat_features=['gender', 
                          'race_ethnicity', 
                          'parental_level_of_education',
                          'lunch',
                          'test_preparation_course']
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("Scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info("Numerical columns completed")
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False)),

                ]
            )
            logging.info("Categorical columns encoding completed")

            preprocessor=ColumnTransformer(
                [
                    ("numerical_pipline",num_pipeline,num_features),
                    ("cateogrical_pipline",cat_pipeline,cat_features)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read Test and Train data Completed")

            logging.info("Obtaining preporcessing object")

            pre_processor_obj = self.get_data_transformer_object()

            target_column ="math_score"
            num_features=['reading_score', 'writing_score']

            input_feature_train_df = train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df=train_df[target_column]
            input_feature_test_df = test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df = test_df[target_column]

            logging.info(f"Applying preprocessing object on training dataFrame and Testing DataFrame")

            input_feature_train_transformed = pre_processor_obj.fit_transform(input_feature_train_df)
            input_feature_test_transformed = pre_processor_obj.fit_transform(input_feature_test_df)
            
            train_arr= np.c_[input_feature_train_transformed,np.array(target_feature_train_df)]
            test_arr= np.c_[input_feature_test_transformed,np.array(target_feature_test_df)]

            logging.info("Saved Preporcessing Object")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=pre_processor_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException (e,sys)
