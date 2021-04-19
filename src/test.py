import urllib.request
import sys
from PIL import Image

URL = "https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg" 

urllib.request.urlretrieve(URL, f"src/profile_imgs/default_profile.jpg")
