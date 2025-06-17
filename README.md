# Boardish

Dynamic modular board with the ability to add, update, delete widgets.
Uses: django, htmx, gridstack.js and some more.

## Features

- User authentication and registration
- Create, edit, and delete boards
- Add and manage elements on boards
- Work in real time with other users

## Planned changes

- Upgraded image storing
- Break down board elements into segmental customizable pieces

## Project Structure

```.
├── boardish
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── boards
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_board_element_userboard_board_user_boardelement.py
│   │   ├── 0003_element_board_element_order_delete_boardelement.py
│   │   ├── 0004_alter_board_title.py
│   │   ├── 0005_alter_element_type.py
│   │   ├── __init__.py
│   ├── models.py
│   ├── routing.py
│   ├── signals.py
│   ├── templates
│   │   ├── base.html
│   │   ├── board.html
│   │   ├── boards.html
│   │   ├── index.html
│   │   ├── partials
│   │   │   ├── board-detail.html
│   │   │   ├── board-list-elements.html
│   │   │   ├── board-list.html
│   │   │   ├── navbar.html
│   │   │   ├── search.html
│   │   │   └── search-results.html
│   │   └── registration
│   │       ├── login.html
│   │       └── register.html
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
├── requirements2.txt
├── requirements.txt
└── static
    ├── board_images
    ├── bready.css
    ├── css
    │   └── styles.css
    ├── demo.css
    ├── events.js
    ├── gridstack-all.js
    ├── gridstack.scss
    ├── js
    │   └── image.js
    ├── khot.png
    └── navbar.css

14 directories, 72 files
```

## Docker Setup

To run the project using Docker:

**Run the Docker container using Docker Compose:**

   ```sh
   cd /path/to/repo
   docker-compose up
   ```

   This will start the application and its dependencies.

**Access the application:**

   Open your web browser and go to `http://localhost:7500` to access the application.

## Requirements

- Docker
- Docker Compose
- Database (Postgresql)

## Local installation (for editing)

1. Clone the repository:

   ```sh
   git clone https://github.com/wojtaeek/boardish.git
   cd dish
   ```

2. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up the database:

   Create the database (assuming you have postgres) with the credentials
   available in the /boardish/settings.py.
   (Alternatively switch to sqlite db, although that may cause
   issues with the existing migrations as it does not support JSON data format)

4. Run redis in docker:

   ```sh
   docker run -d redis
   ```

5. Apply the migrations:

   ```sh
   python manage.py migrate
   ```

6. Run the development server:

   ```sh
   python manage.py runserver
   ```
