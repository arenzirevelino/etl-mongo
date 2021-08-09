# etl using airflow from local to MongoDB on Atlas Cluster

Hi, in here I still learn about Airflow but for this I try to create ETL from sample result query from sample DB [Chinook DB](https://www.sqlitetutorial.net/sqlite-sample-database/), transform result to json format and load it into MongoDB on Atlas Cluster (Cloud). 

## I am using:
1. Python 3.9
2. Apache Airflow
3. pipenv 
4. Pymongo
5. MongoDB (Cloud) on Atlas Cluster

## step-by-step
1. create project directory, setup environment and setup airflow for this project. for detail step-by-step you can check my previous project **airflow-etl** repo in here: https://github.com/arenzirevelino/airflow-etl
2. after that install pymongo library using : `pipenv install pymongo`
3. you can setup free cluster on mongoDB by follow step-by-step from this link https://docs.atlas.mongodb.com/tutorial/deploy-free-tier-cluster/

## Result
