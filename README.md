# Ecstatic Paradox Website

This document is created for the aid of any developer who may join during the development and also for our own future references to API and other stuffs.
<br> **Created with :sparkling_heart:**

**IMPORTANT: Keep the commit messages short and informative.Proper Commit Convention may be updated in future. Read this [Article at freeCodeCamp](https://www.freecodecamp.org/news/writing-good-commit-messages-a-practical-guide/) and also try to follow this [Emoji Convention](https://gist.github.com/parmentf/035de27d6ed1dce0b36a)**

## Setup Process

**Requirements**
  - Docker
  - docker-compose
  
**Commands**
`docker-compose up`

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
  - djangorestframework-simplejwt
  - wagtail cms

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
  + **`Absentee` **
    Stores the reasons for being absent of absentee member.
    - Date `Date the person was absent`
    - Member
    - Remarks
  + **`Notice` **
   - Date
   - Issuer `Foreign Key with` **`django.contrib.auth.models.User`**
   - Description
   - Attachment
   - Is Pinned
   - Expiry DateTime
   - Is expired `Boolean`
  + **`Project` **
  Only Certain Group will have authorization to add Project
    - Title
    - Overview `Short Paragraph info about Project`
    - Start Date
    - End Date
    - Thumbnail `Image Field`
    - Description `Complete Detail About Project`
    - Is Highlighted
    - Is Completed
  + **`Meeting` **
    - Date
    - Title
    - Duration
    - Overview
    - Minute
    
### Authentication System
+ Authentication System is handled with JWT Tokens.  
**Model:** `django.contrib.auth.models.User`
+ Regiatration of users will be manually done by administration.
+ Refresh Token (15 days Valid) as HttpOnly Cookie and Access Token as Json will be provided on authentication.  
+ Authorizations will be given by dividing the users into specific permission groups.
  - Superuser
  - General member
  - HR .. etc [needs discussion]() 


### Attendence System
  - Only HR will have permission to mark members on leave.
  - List of members whose record isnot obtained for specific day(neither attended nor on leave) will be provided to HR on need. 
 
