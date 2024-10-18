# Logistics Platform

This is a scalable logistics platform where users can book transportation services for goods, and drivers can accept or reject bookings. It supports role-based access (admin, user, driver) and integrates Google Maps for location input.

## Features

- Role-based access control: Separate dashboards for Admin, User, and Driver.
- Google Maps API integration: Autocomplete for location input.
- Booking Management: Users can create bookings, and drivers can accept or reject them.
- Admin Control: Admins can manage users and bookings, excluding the ability to deactivate themselves.

## Tech Stack

- **Backend**: Django 5.1.2
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (default)
- **Google Maps API**: For location autocomplete in the driver dashboard

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your_username/logistics-platform.git
   cd logistics-platform
Install Dependencies

Create a virtual environment and install the dependencies listed in requirements.txt.

bash

Copy
python -m venv venv
Activate the virtual environment:

On Windows:

bash

Copy
venv\Scripts\activate
On macOS/Linux:

bash

Copy
source venv/bin/activate
Then install the dependencies:

bash

Copy
pip install -r requirements.txt
Set Up Environment Variables

To hide your Google Maps API key, create a .env file in the root directory and add the following:

makefile

Copy
GOOGLE_MAPS_API_KEY=your_api_key_here
You will also need to update your Django settings to load the API key from the .env file. Open logistics_platform/settings.py and add:

python

Copy
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
In your template or JavaScript file, use the environment variable like this:

html

Copy
<script src="https://maps.googleapis.com/maps/api/js?key={{ GOOGLE_MAPS_API_KEY }}&libraries=places"></script>
Run Migrations

Apply database migrations by running:

bash

Copy
python manage.py migrate
Create a Superuser

Create an admin user with the following command:

bash

Copy
python manage.py createsuperuser
Follow the prompts to set up your admin account.

Run the Development Server

Start the development server using:

bash

Copy
python manage.py runserver
You can now access the platform at http://127.0.0.1:8000/.

Google Maps API Setup

Visit the Google Cloud Console.

Create a project and enable the Google Maps JavaScript API.

Generate an API key and add it to your .env file as shown above.

Deployment

To deploy this project, you can use platforms like Heroku, DigitalOcean, or AWS. Make sure to:

Set up environment variables on the hosting platform.

Update the ALLOWED_HOSTS in settings.py with your domain or server IP.

Admin Dashboard Features
View, edit, and delete users (Admins cannot delete themselves).

Manage pending, active, and completed bookings.

Driver Dashboard Features
View and update your current location using Google Maps Autocomplete.

Accept or reject bookings.

Update booking status (e.g., "En Route to Pickup", "Delivered").

User Dashboard Features
Create new bookings by entering pickup and drop-off locations.

View booking status and driver information.

Contributing
Feel free to fork this repository and make pull requests. Contributions are welcome!

License
This project is licensed under the MIT License.

requirements.txt
txt

Copy
Django==5.1.2
googlemaps==4.4.5
django-dotenv==1.4.2
