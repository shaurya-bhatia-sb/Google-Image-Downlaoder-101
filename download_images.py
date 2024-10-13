from google_images_search import GoogleImagesSearch
import os

# Your API key and CX (custom search engine ID)
gis = GoogleImagesSearch(" Your API key", "your custom search engine ID")

# Define the download path at the beginning
download_path = "./images"


def download_images(query, num_images):
    # Define search parameters
    search_params = {
        "q": query,  # Query (the search term)
        "num": num_images,  # Number of images to download
        "fileType": "jpg",  # Specify file type (jpg in this case)
        "imgType": "photo",  # Specify type (photo images only)
    }

    # Ensure the download directory exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Perform the search
    gis.search(search_params=search_params)

    # Loop over the results and download each image
    for image in gis.results():
        image.download(download_path)  # Download the image to the specified directory
        print(
            f"Downloaded: {image.url} to {download_path}"
        )  # Print the URL and download path


if __name__ == "__main__":
    query = input("Enter image search tag: ")
    num_images = int(input("Enter the number of images to download: "))
    download_images(query, num_images)
