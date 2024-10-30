from flask import Flask, request, redirect, url_for, render_template, flash
from google_images_search import GoogleImagesSearch
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)
app.secret_key = 'Your Secret key'  # Replace with a secure key for Flask sessions

# Google Images Search Configuration
API_KEY = ' API KEY'  # Replace with your Google API key
CX_ID = 'CUSTOM SEARCH ENGINE ID'  # Replace with your Custom Search Engine ID
gis = GoogleImagesSearch(API_KEY, CX_ID)

# Path to download images
download_path = "./images"


def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'sbhatia_be22@thapar.edu'  # Replace with your email
    msg['To'] = to_email
    msg.attach(MIMEText(body, 'plain'))

    # Attach each image in the download directory
    for filename in os.listdir(download_path):
        file_path = os.path.join(download_path, filename)
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {filename}')
            msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login('sbhatia_be22@thapar.edu', 'hjwb dcux swxy bcyn')  # Replace with your app password
            server.sendmail('sbhatia_be22@thapar.edu', to_email, msg.as_string())
            print("Email with images sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")



def download_images(query, num_images):
    search_params = {
        "q": query,
        "num": num_images,
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        num_images = int(request.form['num_images'])
        user_email = request.form['email']

        try:
            # Download images based on the search query and number of images
            download_images(query, num_images)

            # Send an email notification with the images as attachments to the user's email
            send_email(
                subject='Images Downloaded',
                body=f'Successfully downloaded {num_images} images for query: {query}',
                to_email=user_email
            )

            flash('Images downloaded and email with images sent!', 'success')
            return redirect(url_for('success'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    return render_template('index1.html')


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
