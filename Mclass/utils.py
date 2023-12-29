from PIL import Image


# checking if image url is valid
def image_is_valid(image_file):
    try:
        img = Image.open(image_file)
    except:
        return False
    return True


def get_options():
    return [
        "Chemistry",
        "Biology",
        "Physics",
        "Computer Science",
        "Art",
        "History",
        "Literature",
        "Languages",
        "Music",
        "Geography",
        "Other",
    ]
