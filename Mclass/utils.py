import requests

# checking if image url is valid
def image_is_valid(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    try:
        r = requests.head(image_url)
    except:
        return False
    if r.headers["content-type"] in image_formats:
        return True
    return False