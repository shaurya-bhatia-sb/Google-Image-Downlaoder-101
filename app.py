from flask import Flask, request, redirect, url_for, render_template, flash
from google_images_search import GoogleImagesSearch
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import zipfile

app = Flask(__name__)
app.secret_key = 'App secret key'  # Replace with a secure key for Flask sessions

# Google Images Search configuration
API_KEY = 'Google API key'  # Replace with your Google API key
CX_ID = 'Custom Search Engine ID'  # Replace with your Custom Search Engine ID
gis = GoogleImagesSearch(API_KEY, CX_ID)

# Paths
download_path = "./images"
zip_path = "./images.zip"


def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'sender email'  # Replace with your email
    msg['To'] = to_email
    msg.attach(MIMEText(body, 'plain'))

    # Attach the ZIP file
    with open(zip_path, 'rb') as zip_file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(zip_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= images.zip')
        msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login('sender email', 'app password')  # Replace with your app password
            server.sendmail('sender email', to_email, msg.as_string())
            print("Email with ZIP file sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def download_images(query, num_images):
    search_params = {
        "q": query,
        "num": min(num_images, 1000),  # Limit to 1000 images
        "fileType": "jpg",
        "imgType": "photo",
    }

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Clear the download directory to remove previous images
    for file in os.listdir(download_path):
        os.remove(os.path.join(download_path, file))

    gis.search(search_params=search_params)
    for image in gis.results():
        image.download(download_path)
        print(f"Downloaded: {image.url} to {download_path}")

    # Create a ZIP file
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(download_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zipf.write(file_path, os.path.relpath(file_path, download_path))
    
    # Clean up individual images
    for file in os.listdir(download_path):
        os.remove(os.path.join(download_path, file))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        num_images = int(request.form['num_images'])
        user_email = request.form['email']

        try:
            # Download images based on the search query and number of images
            download_images(query, num_images)

            # Send an email notification with the ZIP file as an attachment
            send_email(
                subject='Images Downloaded',
                body=f'Successfully downloaded {num_images} images for query: {query}',
                to_email=user_email
            )

            flash('Images downloaded and email with ZIP file sent!', 'success')
            return redirect(url_for('success'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    return render_template('index.html')


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
