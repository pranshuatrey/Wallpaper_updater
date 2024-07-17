import requests
import ctypes
import os
from PIL import Image, ImageDraw, ImageFont


# Constants
SPI_SETDESKWALLPAPER = 20
UNSPLASH_ACCESS_KEY = 'sgN2SIrNRi3fRXgPAd_hVTEC2ZyPFp5ZFuDTmQbfPqA'
UNSPLASH_URL = 'https://api.unsplash.com/photos/random'
QUOTE_API_URL = 'https://zenquotes.io/api/random'

# User-Agent header for Unsplash API
headers = {
    'Accept-Version': 'v1',
    'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
}

# Function to fetch a random photo from Unsplash
def fetch_random_photo():
    response = requests.get(UNSPLASH_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data from Unsplash. Status code: {response.status_code}")
        return None

# Function to fetch a random quote from ZenQuotes
def fetch_random_quote():
    response = requests.get(QUOTE_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data from ZenQuotes. Status code: {response.status_code}")
        return None

# Function to download an image
def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as imageFile:
            imageFile.write(response.content)
        return os.path.exists(path) and os.path.getsize(path) > 0
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return False

# Function to overlay quote on image
def overlay_text_on_image(image_path, tittle):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    #print(type(image))
    
    #font_path = os.path.join(os.environ['WINDIR'], 'Fonts', 'arial.ttf')
    font_path = 'fonto/Roboto-BoldItalic.ttf'
    if not os.path.exists(font_path):
        print(f"Font path {font_path} does not exist.")
        return
    
    Image_width, Image_height = image.size
    font_size = 40
    Font = ImageFont.truetype(font_path, font_size)
    
    # Calculate width and height from bounding box
    def text_width(tittle,Font):
          # Get bounding box of the text
        bbox = draw.textbbox((0,0),tittle,font=Font)
        t_width = bbox[2] - bbox[0]
        return t_width
   
    def text_height(tittle,Font):
        bbox = draw.textbbox((0,0),tittle,font=Font)
        t_height = bbox[1] - bbox[0]
        return t_height

    while True:
        if text_width(tittle,Font) < Image_width-40:
            break
        font_size -= 1
        Font = ImageFont.truetype(font_path, font_size)

    print(tittle)
    text_y = (Image_height-text_height(tittle,Font))/2
    draw.text((25,text_y),tittle,(0, 0, 0),font=Font)

    image.save(image_path)

def get_screen_resolution():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize

def resize_image_to_screen(image_path, screen_size):
    with Image.open(image_path) as img:
        resized_image = img.resize(screen_size, Image.Resampling.LANCZOS)
        resized_image_path = os.path.join(os.path.dirname(image_path), "resized_" + os.path.basename(image_path))
        resized_image.save(resized_image_path)
        return resized_image_path

    
# Function to set the desktop wallpaper
def set_wallpaper(image_path):
    result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
    if not result:
        print("Failed to set wallpaper. Error code:", ctypes.GetLastError())
    else:
        print("Wallpaper set successfully.")

# Main function
def main():
    photo_data = fetch_random_photo()
    quote_data = fetch_random_quote()
    if photo_data and quote_data:
        image_url = photo_data['urls']['regular'] 
        quote_text = quote_data[0]['q'] + " -" + quote_data[0]['a']
        image_path = os.path.join(os.environ['USERPROFILE'], 'wallpaper.jpg')
        if download_image(image_url, image_path):
            scr_res = get_screen_resolution()
            #print(f'Screen resolution: {scr_res}')
            img_path = resize_image_to_screen(image_path, scr_res)
            overlay_text_on_image(img_path, quote_text)
            set_wallpaper(img_path)
        else:
            print("Failed to write the image file.")
    else:
        print("Failed to retrieve data from Unsplash or ZenQuotes.")

if __name__ == "__main__":
    main()






