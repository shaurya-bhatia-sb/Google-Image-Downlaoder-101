Google-Image-Downlaoder101
This project is a Flask-based web application that lets users request specific types of images (e.g., "cat," "dog," "car") by entering keywords, the number of images to download, and an email address. It uses the Google Custom Search API to retrieve images and then sends them to the user as a compressed ZIP file via email.

Features:
Customizable Search: Users specify keywords and the number of images.
Email Delivery: Images are zipped and emailed directly to the user.
User-Friendly Interface: Accessible through a simple web form.
Prerequisites
Google Custom Search API Key and Custom Search Engine (CSE) ID
Get a Google API Key
Create a Custom Search Engine (CSE)

Python Packages:
Flask
google-api-python-client
requests
smtplib
zipfile

Email Service:
Sender email address and an app-specific password if using Gmail.
Setup
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
Install Required Packages:

bash
Copy code
pip install -r requirements.txt
Configure API Keys and Email: Open app.py and replace placeholders:

python
Copy code
API_KEY = 'YOUR_GOOGLE_API_KEY'
CSE_ID = 'YOUR_CSE_ID'
SENDER_EMAIL = 'your_email@example.com'
SENDER_PASSWORD = 'your_email_password'


Run the App:
python app.py
The app will be available at http://127.0.0.1:5000.

Usage
Open http://127.0.0.1:5000 in your browser.

Enter:
Email Address: Where images will be sent.
Image Type: (e.g., "cat," "car").
Number of Images: Specify up to n images.

Submit, and the images will be emailed to you as a ZIP file.
