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

This web app designed in Flask is built to perform daily a scheduled API call from matomo analytics, download data and store it into PostgreSQL database.

<img width="1792" alt="Screenshot 2024-07-29 alle 08 57 09" src="https://github.com/user-attachments/assets/0c71dc2f-f8ae-45ec-be30-a34dc16d4987">

Main functionalities:
* API calls from Matomo Analytics
* DB operations
* Scheduled jobs
* Automatic deployment
* Authentication

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
<p align="left"> 

  
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="40" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original.svg" width="40" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg" width="40" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/supabase/supabase-original.svg" width="40" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vercel/vercel-original.svg" width="40" height="40" />
          
          
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
To get a local copy up and running follow be ture to have the following steps checked.

### Prerequisites

* Make sure you have pip installed 
* Create a DB instance on supabase
* Create necessary DB tables. You can find all the CREATE queries in [db/create_tables.sql](db%2Fcreate_tables.sql)
* Install necessary packages
  ```sh
  pip install -r requirements.txt
  ```


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ccrisc/rent_items_management.git
   ```
2. Enter your DB credentials in `config.php`
    ```php
   define('DB_NAME', '*****');
   define('DB_USER', '*****');
   define('DB_PASSWORD', '*****');
   define('DB_HOST', '*****:3306');;
   ```
3. You can create schema and tables by executing the SQL from the `demo_dump` folder fo getting started
4. Run your local PHP server (if you are using PHPStorm you can set up your server following <a href="http://www.php.cn/faq/738624.html">these instructions</a>)
   ```sh
   python app.py
   ```
5. Visit http://127.0.0.1:5000

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

### Add new customer
You can add a new customer by clicking the orange button on the main page, the form allows to insert first name and last name
<img width="1792" alt="Screenshot 2024-07-29 alle 09 10 22" src="https://github.com/user-attachments/assets/45beedfc-7a50-4ca8-90d8-d82d5e8e8878">

### New Order
In a single order you can add multiple items and different quantities for each. At the bottom you have to specify the customer the return date and the order number.
<img width="1307" alt="Screenshot 2024-07-29 alle 09 10 47" src="https://github.com/user-attachments/assets/06ad8e26-e67d-4d70-b74b-145438a38f42">


### Orders Management
In the order management table you have an overview of all your orders. 
<img width="1269" alt="Screenshot 2024-07-29 alle 09 10 57" src="https://github.com/user-attachments/assets/fd5ec400-e58d-4363-803b-36ec39cab27c">
In the table you see the column state that indicates if the order has been closed (green) or if it still active (orange).
At the same time the column return date signal if the return date is past (red) or not yet arrived.

By clicking the DETAIL button you get the order overview. If the order is still active you can proceed to close it, if the customer return all the items or to close it partially.
<div style="display: flex; gap: 10px;">
  <img width="315" alt="Screenshot 2024-07-29 alle 09 13 28" src="https://github.com/user-attachments/assets/d1560cce-18b0-43a5-b740-03f0dc880006">
  <img width=315" alt="Screenshot 2024-07-29 alle 09 13 21" src="https://github.com/user-attachments/assets/5504b9ce-e88f-46ff-a991-2144adbb8c13">
</div>

When you proceed to close an order partially you will be asked to specify for each article the quantity that the user has returned. The difference will be calculated in the backend and added to the not returned items for that specific user.
<img width="1225" alt="Screenshot 2024-07-29 alle 09 19 45" src="https://github.com/user-attachments/assets/382164b3-f1e8-4158-aabc-5123ab4e1451">


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you think you found a bug in this repo, you can [submit an issue](https://github.com/ccrisc/rent_items_management/issues/new/choose).

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



