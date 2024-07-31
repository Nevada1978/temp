from flask import Flask, request, jsonify
import os
import subprocess
import requests
from datetime import datetime
app = Flask(__name__)
image_counter = 1

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    if 'url' not in data or 'access_token' not in data:
        return jsonify({'error': 'No URL or access_token provided'}), 400

    file_url = data['url']
    access_token = data['access_token']
    current_date = datetime.now().strftime("%m_%d")
    local_filename = f'/Users/mac/PycharmProjects/test/{current_date}_image{image_counter}.png'

    # local_filename = 'downloaded_image.png'

    # Use curl to download the image
    download_command = f'curl -o {local_filename} {file_url}'
    subprocess.run(download_command, shell=True, check=True)

    # Upload the image using curl and capture the response
    upload_url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image'
    upload_command = f'curl -F "media=@{local_filename}" "{upload_url}"'
    upload_response = subprocess.run(upload_command, shell=True, check=True, capture_output=True, text=True)

    # Parse the JSON response from the upload
    response_json = upload_response.stdout
    response_data = jsonify(response_json)

    return response_data, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123)
