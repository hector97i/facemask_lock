import requests

def post_image(img, base_url):
    url = 'http://' + base_url + '/predict'
    files = {'media': img}
    response = requests.post(url, files=files)


