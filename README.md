# Socio Backend

A Django-based web application for management with authentication, REST API, and modern UI built with Tailwind CSS.

## Features

- User authentication and authorization
- Employee management system
- REST API endpoints
- Google OAuth integration
- Modern responsive UI with Tailwind CSS
- Role-based access control

## Prerequisites

- Python 3.8+
- Node.js 14+ (for Tailwind CSS build)
- Mysql (optional, SQLite is used by default)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd sociobackend
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
# For development
pip install -r requirements/dev.txt

# For production
pip install -r requirements/prod.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
# Edit .env file with your configuration
```

Required environment variables:
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3


### 5. Install Node.js Dependencies

```bash
npm install
```

### 6. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Project Structure
sociobackend/
├── src/
│ ├── accounts/ # User authentication and employee management
│ ├── config/ # Django settings and configuration
│ └── web/ # Web templates and static files
├── requirements/ # Python dependencies
├── media/ # User uploaded files
└── manage.py # Django management script


## API Endpoints

- Authentication: `/api/auth/`
- Employee Management: `/api/employees/`
- Menu Management: `/api/menu/`
