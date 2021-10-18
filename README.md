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
     User must have profile to use dashboard, so if logged in user has to profile then, they are redirected to profile create page. 
  + **`Attendance Issue`**
    To store on which days HR opened attendance.
    - Date
    - issuer `HR who opened attendance that day`
    - remarks
  + **`Attendance`**
    - issue `Foreign Key of **Attendace Issue** `
    - Member `Foreign Key of **User** model`
    - Status `Boolean either Attended(True) or On Leave(False)`
    - Remarks `Information about why the person was on leave`
  + **`Absentee`**
    Stores the reasons for being absent of absentee member.
    - issue `Date the person was absent, Foreign Key of Attendance Issue Model`
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
    - Author `Many to Many Relationship with User Model`
    - Content
    - Section
    Content streamfield should have sections, figures
+ **`Blog`**
    - Title
    - Author
    - Content
    - Feed_image
    - Section
    Content Streamfield should have heading, para, media, `Quote` 
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
+ Default Wagtail Auth System.


 
