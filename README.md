﻿# Project Name: Dish

Dynamic modular corkboard with the ability to add, update, delete widgets. Uses: django, htmx, gridstack.js and some more.

## Features

- User authentication and registration
- Create, edit, and delete boards
- Add and manage elements on boards
- Responsive design
- Image upload and scaling

## Project Structure

```
/home/wojtek/dish/
├── Dockerfile
├── README.md
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── boardish/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── boards/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   └── migrations/
│       ├── 0001_initial.py
│       ├── 0002_board_element_userboard_board_user_boardelement.py
│       ├── 0003_element_board_element_order_delete_boardelement.py
│       ├── 0004_alter_board_title.py
│       ├── 0005_alter_element_type.py
│       └── __init__.py
├── static/
│   ├── bready.css
│   ├── demo.css
│   ├── events.js
│   ├── gridstack-all.js
│   ├── gridstack.scss
│   ├── navbar.css
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── image.js
├── templates/
│   ├── base.html
│   ├── board.html
│   ├── boards.html
│   ├── index.html
│   └── partials/
│       ├── board-detail.html
│       ├── board-list-elements.html
│       ├── board-list.html
│       ├── navbar.html
│       ├── search-results.html
│       ├── search.html
│       └── registration/
│           ├── login.html
│           └── register.html
```

## Docker Setup

To run the project using Docker:

**Run the Docker container using Docker Compose:**

   ```sh
   docker-compose up
   ```

   This will start the application and its dependencies.

**Access the application:**

   Open your web browser and go to `http://localhost:7500` to access the application.

## Requirements

- Docker
- Docker Compose

## Local installation (for editing)

1. Clone the repository:

   ```sh
   git clone https://github.com/wojtaeek/dish.git
   cd dish
   ```

2. Install the required dependencies:

   ```sh
   pip install -r requirements.txt (possibly you will need to install psycopg2 separately with another tool (pacman, apt, winget etc.))
   ```

3. Set up the database:

   Create the database (assuming you have postgres) with the credentials available in the /boardish/settings.py. (Alternatively switch to sqlite db, although that may cause issues with the existing migrations as it does not support JSON data format) 

4. Apply the migrations:

   ```sh
   python manage.py migrate
   ```

5. Run the development server:

   ```sh
   python manage.py runserver
   ```

