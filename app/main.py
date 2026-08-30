from fastapi import FastAPI
from app.api.routes.projects import router as projects_router    



app = FastAPI(
    title =" PipelineHub API",
    description = "PipelineHub API for managing and deploying machine learning pipelines.",
    version="0.1.0"

)
app.include_router(projects_router)


@app.get("/")
def root():
    return{
        "name":"PipelineHub",
        "version":"0.1.0",
        "status":"running",
    }


@app.get("/health")
def health_check():
    return{"status":"healthy"}