# Logistics Platform

This scalable logistics platform allows users to book transportation services for goods, and drivers to accept or reject bookings. It features role-based access for admin, user, and driver roles and integrates Google Maps for location input.

## Features

- **Role-based access control**: Separate dashboards for Admin, User, and Driver.

- **Google Maps API integration**: Autocomplete for location input.

- **Booking Management**: Users can create bookings, and drivers can accept or reject them.

- **Admin Control**: Admins can manage users and bookings, excluding the ability to deactivate themselves.

## Tech Stack

- **Backend**: Django 5.1.2

- **Frontend**: HTML, CSS, Bootstrap

- **Database**: SQLite (default)

- **Google Maps API**: For location autocomplete in the driver dashboard

## Setup Instructions

### 1. **Clone the Repository**

      ```bash
      git clone https://github.com/your_username/logistics-platform.git
      cd logistics-platform

### 2. **Install Dependencies**

     ```bash

  python -m venv venv

  source venv/bin/activate  # For Linux/MacOS

  venv\Scripts\activate  # For Windows

  pip install -r requirements.txt

### 3. **Set Up API Keys**

Create a `cred.py` file in the root directory to store your API keys:

```python

# cred.py

SECRET_KEY = 'django-insecure-z&o5ln1pbb#+*o!+isypo6d%v@0cnk91r8...'

GOOGLE_MAPS_API_KEY = 'AIzaSyCbSg7br_mo3_MCZ...'

Update your Django settings to load these keys:

```python

# logistics_platform/settings.py

from cred import SECRET_KEY, GOOGLE_MAPS_API_KEY

```

    In your HTML templates, add the script to load the Google Maps API:

```html

<script src="https://maps.googleapis.com/maps/api/js?key={{ GOOGLE_MAPS_API_KEY }}&libraries=places"></script>

```

### 4. **Run Migrations**

```bash

python manage.py migrate

```

### 5. **Create a Superuser**

```bash

python manage.py createsuperuser

```

Follow the prompts to set up your admin account.

### 6. **Run the Development Server**

```bash

python manage.py runserver

```

You can now access the platform at http://127.0.0.1:8000/.

### 7. **Google Maps API Setup**

- Visit the Google Cloud Console.

- Create a project and enable the Google Maps JavaScript API.

- Generate an API key and add it to your `cred.py` as shown above.

### 8. **Deployment**

To deploy this project, you can use platforms like Heroku, DigitalOcean, or AWS. Make sure to:

- Set up environment variables on the hosting platform.

- Update the `ALLOWED_HOSTS` in `settings.py` with your domain or server IP.

## Admin Dashboard Features

- View, edit, and delete users (Admins cannot delete themselves).

- Manage pending, active, and completed bookings.

## Driver Dashboard Features

- View and update your current location using Google Maps Autocomplete.

- Accept or reject bookings.

- Update booking status (e.g., "En Route to Pickup", "Delivered").

## User Dashboard Features

- Create new bookings by entering pickup and drop-off locations.

- View booking status and driver information.

## License

This project is licensed under the MIT License.
