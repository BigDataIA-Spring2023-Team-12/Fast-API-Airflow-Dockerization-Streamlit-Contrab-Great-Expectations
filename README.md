# Decoupling Streamlit Application(Streamlit-FastAPI-Airflow-GreatExpectations-Contrab-Dockerization)


## About 

We previously focused on web scrapping the geospatial data from GOES and NEXRAD AWS buckets to build a streamlit application for data exploration that leverages publicly available data and makes it easier for data analysts to download and work on. <br>
In the scope of this project, <br>
We have decoupled the streamlit application into two microservices, Streamlit and Fast API.<br>
Furthermore, we have dockerized the services and also used Airflow to author workflows as DAGs of tasks to be executed.



## Links
* Codelab Documentation - [Codelab](https://codelabs-preview.appspot.com/?file_id=1CwPu13u5ciGguLL0QcZjw2f8TZfOqSlW74EaKc7tRBE/#2)
* GitHub Organization - [GitHub](https://github.com/BigDataIA-Spring2023-Team-12)
* Streamlit Application - [Streamlit]()



## LEARNINGS/TECH USED
Streamlit<br>
AWS<br>
SQLite<br>
Great-Expectations<br>
Pytest<br>
AirFlow<br>
FastAPI<br>
Docker<br>
Contrab<br>
Git (Version Control)<br>
Documentation on Codelabs<br>


## Process Flow
We have decoupled our streamlit application into two microservices: Streamlit and FastAPI

Streamlit -

1. Implemented login page and allow authenticated users to interact with the dashboard
2. Send RestAPI calls to FastAPI endpoints and display the returned response.
3. Created a user with username: damg7245 password: spring2023 for reviewer login

FastAPI -

1. Created endpoints as per the use case
2. Checked the response code for all the endpoints

Airflow -

Created DAGs to:

1. Scrape the metadata of the AWS bucket on daily basis using Crontab
2. Populate the scrapped metadata in to the database
3. Export all the metadata of the database into a csv file
4. Run Great Expectation data quality report.



---
## Team Members
1. Harsh Shah - NUID: 002704406 - (shah.harsh7@northeastern.edu)
2. Parva Shah - NUID: 002916822 - (shah.parv@northeastern.edu)
3. Dev Shah - NUID: 002978981 - (shah.devs@northeastern.edu)



## Undertaking

> WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK
**Contribution**: 
*   Harsh Shah &emsp; :`33.33%`
*   Parva Shah &emsp; :`33.33%`
*   Dev Shah &emsp;   :`33.33%`







