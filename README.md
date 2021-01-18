# Ecstatic Paradox Website

This document is created for the aid of any developer who may join during the development and also for our own future references to API and other stuffs.
<br> **Created with :sparkling_heart:**

**IMPORTANT: Keep the commit messages short and informative.Proper Commit Convention may be updated in future. Read this [Article at freeCodeCamp](https://www.freecodecamp.org/news/writing-good-commit-messages-a-practical-guide/) and also try to follow this [Emoji Convention](https://gist.github.com/parmentf/035de27d6ed1dce0b36a)**

## Setup Process

Can be configured for local development easily via Docker.

**Requirements**
  - Docker
  - docker-compose
  
**Commands**
`docker-compose up --build`
Then Check https://localhost .  
If docker is not available, then Pipenv can be used.
**Requirements**
  - pip3
  - pipenv `Can be installed by pip install pipenv`

**Commands**
Run `pipenv install --dev` to install dependencies then run `pipenv run python manage.py migrate` to migrate local database, then run `pipenv run python manage.py runserver` to run the localserver.

## Frontend

**NOTE: Visit Backend for API references and use guide.**

### 1. Home
Homepage contains basic introductory stuffs [EDIT THIS]

### 2. Programs

### 3. Publications

### 4. Courses

### 5. Projects

### 6. About Us

### 7. Log in 

### 8. Dashboard

## Backend
**Dependencies** 
  - Django
  - django_rest_framework
  - wagtail

### Models Overview
**NOTE: Use CamelCase for model name and snake_case for fields name**
  + **`django.contrib.auth.models.User`**
    Used for the mainly for authentication purposes, OnetoOne extended with `Profile` model. Stores 
    - First Name
    - Last Name
    - Username
    - Email
    - Password
  + **`Profile`**
    Stores additional informations about individual members mainly to be viewes in member profile:
     - Picture
     - Contact Number
     - Institution
     - Facebook Profile
     - LinkedIn Profile
     - Country
     - Address
     - Department
     - Spectrum `ManytoMany field with **Spectrum** model`
     - Additional Information `Bio type discription to show on Member Profile`
  + **`Attendance`**
    - Date
    - Member `Foreign Key of **User** model`
    - Status `Boolean either Attended(True) or On Leave(False)`
    - Remarks `Information about why the person was on leave`
  + **`Absentee`**
    Stores the reasons for being absent of absentee member.
    - Date `Date the person was absent`
    - Member
    - Remarks
  + **`Notice`**
    - Date
    - Issuer `Foreign Key with` **`django.contrib.auth.models.User`**
    - Description
    - Attachment
    - Is Pinned
    - Expiry DateTime
    - Is expired `Boolean`
  + **`Project`**
  Only Certain Group will have authorization to add Project
    - Title
    - Overview `Short Paragraph info about Project`
    - Start Date
    - End Date
    - Thumbnail `Image Field`
    - Description `Complete Detail About Project`
    - Is Highlighted
    - Is Completed
  + **`Meeting`**
  Stores meeting minute.
    - Date
    - Title
    - Duration
    - Overview
    - Minute
  + **`Document`**
  Stores company documents.
    - Title
    - Date
    - Type
    - Overview
    - Attachment
 + **`Article`**
    - Title
    - Author
    - Date Published
    - Is Published
    - Content
 + **`Blog`**
    - Title
    - Author
    - Date Published
    - Is Published
    - Content
 + **`Webinar`** **`Symposium`** **`Talk Shows`** **`Conference`**
  - Title
  - Description
  - Thumbnail
  - Youtube_link
  - Registration_form
 + **`Research Paper`**
    - Title
    - Author
    - Date Published
    - Is Published
    - Content 
 
 
### Authentication System
**Model:** `django.contrib.auth.models.User`
+ Registration of users will be manually verified by administration.  
+ Authorizations will be given by dividing the users into specific permission groups.
  - Superuser
  - General member
  - HR .. etc [needs discussion]() 


### Attendence System
**Model:** `Attendance`
  - Attendance will be opened by HR(probably everyday at 9pm)..
  - Those member who fill out the form will have record on Attendance table with status True.
  - Those members who are on leave should ask HR for leave. Only HR will have permission to mark members on leave with additional Remarks(Reason for leave).
  - List of members whose record isnot obtained on **Attendence** table for specific date(status neither attended(True) nor on leave(False)) will be provided to HR on need after 10pm of that day.
  - HR will have permission to add member as leave or to send the absentee member link to ask for reason.
  - Information About absentee member will be stored in **Absentee** Table.
  - HR can view remarks from **Absentee** Table 
 
### 
