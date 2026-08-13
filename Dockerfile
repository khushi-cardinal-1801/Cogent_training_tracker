#base image
FROM python:3.9-slim

#working directory
WORKDIR /app
#copy
COPY . /app     

#run
RUN pip install -r requirements.txt
#port
EXPOSE 8000


#command
CMD ["uvicorn", "main:obj", "--host", "0.0.0.0", "--port", "8000","--reload"]