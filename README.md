<div align="center">
  <h1 align="center">Task Scheduler for Matomo</h1>
</div>



<a id="readme-top"></a>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This web app designed in Flask is built to perform daily a scheduled API call from matomo analytics, the fetched data is stored it into a database and the interface serves as a management system to look aut for the API status and data statistics

The API call performed from matomo is **Live.getLastVisitsDetails** you can read the matomo API documentation [here](https://developer.matomo.org/api-reference/reporting-api)

<img width="1454" alt="Screenshot 2024-09-08 alle 20 31 55" src="https://github.com/user-attachments/assets/04fc797f-6a5b-417e-ac90-d6ab1520b8ec">

Main functionalities:
* API calls from Matomo Analytics
* CRUD Operations
* DB operations
* Scheduled jobs
* Automatic deployment
* Authentication

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
<p align="left"> 

  
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="40" height="40" />
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original.svg" width="40" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg" width="40" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/githubactions/githubactions-original.svg" width="40" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/supabase/supabase-original.svg" width="40" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vercel/vercel-original.svg" width="40" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pycharm/pycharm-original.svg" width="40" height="40" />
          
          
</p>

* The application environment is built with Flask. 
* The postgreSQL db is hosted with Supabase. 
* The app is deployed on Vercel. 
* The scheduled job is performed with Github Actions

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running be sure to have the following steps checked.

### Prerequisites

* Make sure you have pip installed 
* Create your DB instance.
* Create necessary DB tables. You can execute all the CREATE queries in [db/create_tables.sql](db%2Fcreate_tables.sql)


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ccrisc/matomo.git
   ```
2. Install necessary packages
  ```sh
  pip install -r requirements.txt
  ```
3. Create a `.env` file and define the following variables
    ```php
   ENVIRONMENT=development
   SUPABASE_HOST=localhost
   SUPABASE_PORT=5432
   SUPABASE_DB_NAME=matomo_task_scheduler
   SUPABASE_PASSWORD=xxxx
   SUPABASE_USER=xxxx
   FLASK_SECRET_KEY=xxxx
   MATOMO_API_URL=xxxx
   ```
5. Start your Flask app
   ```sh
   python app.py
   ```
6. Visit http://127.0.0.1:5000

### Set up production environment



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Login
Login with your user credentials. If you successfully set up the db you can log in with the following credentials:
username: demo
password: abcd
<img width="823" alt="Screenshot 2024-09-08 alle 20 29 07" src="https://github.com/user-attachments/assets/e1cc7870-347a-4dc7-9f8d-eb22e957eacc">
You will be automatically logged out after 30 minutes of inactivity

### Dashboard
The dashboard shows on the left the navigation sidebar. You can expand it by clicking on the burger menu.
On the top right you can perform log out and read the latest messages.

The dashboard shows the last api call status if it was successful or if it failed and datetime of when it was performed.
<img width="1454" alt="Screenshot 2024-09-08 alle 20 56 24" src="https://github.com/user-attachments/assets/575fe38d-0664-49f4-95be-6b50c2fbefd4">

### Users
Only if the current user logged has admin privilege he can access the users management section.

In the users table you have an overview of all your users that have an account. The table can be filtered by column

<img width="1386" alt="Screenshot 2024-09-08 alle 21 03 16" src="https://github.com/user-attachments/assets/cbfb39b6-a4dc-47c4-94ed-0eff997cd23a">


**CRUD Operations:** 

You can create a NEW USER by clicking the button on the top right of the table. You will be asked to specify the username, the password and if the user is an admin or not.

<img width="1386" alt="Screenshot 2024-09-08 alle 21 10 18" src="https://github.com/user-attachments/assets/5a61b324-9138-4ffd-a82d-3009e80a5855">

By clicking the EDIT button you can proceed to edit data for that specific user

By clicking the DELETE button you will remove the selected user. You will be asked for confirmation prior irreversible delete.

<img width="1374" alt="Screenshot 2024-09-08 alle 21 14 28" src="https://github.com/user-attachments/assets/a0f1c51a-a899-415f-8b3c-b3d9b8c3630b">


### Api Calls

Here you will have an overview of all the API calls performed and if they were successful or not.
In the table you see the column state that indicates if the call was successful (green) or if it failed (red).
At the same time if the call failed then it will be shown the details of the error.

<img width="1374" alt="Screenshot 2024-09-08 alle 21 17 06" src="https://github.com/user-attachments/assets/8f205556-a2b2-4f7f-904b-70faed3e05fd">

### Statistics

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you think you found a bug in this repo, you can [submit an issue](https://github.com/ccrisc/matomo-task-scheduler/issues/new/choose).

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For more details see  See `CONTRIBUTING.md`

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU GENERAL PUBLIC License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



