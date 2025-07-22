# Employee Verification Portal

A comprehensive web application for managing employee verification, certificates, and administrative tasks. Built with Django and deployed on Render.

## Features

- **Admin Portal**
  - Secure admin authentication
  - Employee management
  - Certificate verification
  - Task management
  - Department management
  - User group management
  - Competency tracking

- **Employee Portal**
  - Employee login with ID
  - Certificate upload and tracking
  - Task viewing
  - Profile management

## Tech Stack

- Python 3.9
- Django 5.0
- PostgreSQL
- Bootstrap
- Whitenoise for static files

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/gangeshwar01/Python-Developer-Employee-Verification-Portal.git
cd Python-Developer-Employee-Verification-Portal
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Deployment

The application is configured for deployment on Render. The `render.yaml` file contains the necessary configuration for:
- Web service
- PostgreSQL database
- Environment variables
- Build and start commands

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Database Schema

### employees
- emp_id (Primary Key)
- name
- designation
- join_date
- profile_image

### tasks
- task_id (Primary Key)
- emp_id (Foreign Key)
- task_title
- task_detail
- task_date

### certificates
- cert_id (Primary Key)
- emp_id (Foreign Key)
- cert_title
- cert_file
- cert_status
- upload_date 