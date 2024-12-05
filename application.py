from fastapi import FastAPI, Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import numpy as np
import pandas as pd
from src.pipeline.predict_pipeline import CustomData
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictionPipline


app = FastAPI()


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


 
@app.api_route("/predictdata", methods=["GET", "POST"])
async def predict_data(request: Request, 
    gender: str = Form(None),
    ethnicity: str = Form(None),
    parental_level_of_education: str = Form(None),
    lunch: str = Form(None),
    test_preparation_course: str = Form(None),
    reading_score: int = Form(None),
    writing_score: int = Form(None)):
    if request.method == "GET":
        return templates.TemplateResponse("home.html", {"request": request})
    elif request.method == "POST":
        if None in [gender, ethnicity, parental_level_of_education, lunch, test_preparation_course, reading_score, writing_score]:
            return templates.TemplateResponse(
                "home.html",
                {"request": request, "error": "All fields are required."}
            )
        
        data = CustomData(
            gender=gender,
            race_ethnicity=ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score
        )
        pred_data=data.get_data_as_DataFrame()
        print(pred_data)
        predict_pipeline = PredictionPipline()

        results = predict_pipeline.predict(pred_data)

        return templates.TemplateResponse("home.html", {"request": request,"results":results[0]})
 

if __name__== "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000) 