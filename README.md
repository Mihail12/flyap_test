# Done Task description
The task have been  done for approximately 4 hours
1.5 hours for models and it save logic
45 minutes for full django admin
1.5 for api with is query (Right query to db took much time for the point)
~45 mins for tests and docker configuration

## To start project you need docker and docker-compose
`docker-compose up -d`
and after it build you will able to see http://127.0.0.1:8000 index page   
  
to start tests you need 
`docker exec -it flyap_spasenko_test pytest`

# Flyaps Python test task

## Brief
You have to implement minimalistic Django application with admin interface and one REST endpoint.
Important: before starting implementation you should read carefully [Requirements](#requirements) paragraph and do the task accordingly to it. 

## Description

### General

Module should be designed for analysis of discount conditions between partner companies.

Notion 1 - Discount Agreement (Agreement)  
Notion 2 - Period of agreement (Period)  
Notion 3 - Company  
Notion 4 - Country  
Notion 5 - Responsible person (Negotiator)

Agreement has start and stop date, company agreement concluded with, responsible person - negotiator, debit and credit turnover (export/import).

Period - start and stop date, status - described below.  
One agreement can have several periods inside.  
Inside agreement periods should not intersect.  
Agreement start date could be earlier than start date of the earliest period (but not vice versa) as well as agreement stop date could be later than stop date of the latest period (but not vice versa).  

Company - title, country.  

Country - 3-alpha iso code, name  

Negotiator - user who is responsible for agreement. Should be a django user as well.  

Status - state of a period. Could be: New, Active, Reconciliation, Closed  

### Admin interface 

Each object should be represented in Django admin.
You need to provide search, filters etc guided by your understanding of usability.
Agreement should display Periods with tabular inline.


### UI

On the index page there should be link to the django admin only.


### API

You have to implement API for [agreement calendar](https://drive.google.com/file/d/11f_AthRwxbIM-SOxsGpd3yR0jihexla7/view?usp=sharing).

Number displayed in a month block means number of agreements that are closing this month.
Agreement is closing this month if stop date of latest period is in this month.

/agreements/calendar/ - sample JSON response:
```json
{
      2017: [0, 0, 0, 0, 0, 0, 0, 0, 12, 1, 0, 5],
      2018: [1, 0, 0, 4, 0, 0, 0, 1, 7, 10, 0, 4]
}
```
2017 and 2018 are years.
Arrays - index means month number, digit - number of closing agreements.

Endpoint should support following filters: country, negotiator, company.
For example: ?country=1,2,7&negotitator=4,8
Number is an id of an object.

## Requirements

### General
- Provide fixtures that contain test data: several agreements with several periods

### Will be a plus
- Unit tests

### Coding style
- Code should correspond to industrial standards: pep8, pylint et al.

### Results
- You need to provide information about hours spent on this task, preferrably with split by subtasks.


