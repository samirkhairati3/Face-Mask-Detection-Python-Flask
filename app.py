import os
from flask import Flask, render_template, request, redirect, flash, url_for
import shutil 

UPLOAD_FOLDER = './inputData'

cmd1= 'java -jar ReadWebCam.jar'
cmd2= 'python detect_mask_image.py --image inputData/Capture.png'
cmd3= 'java -jar FindMatchingProbability.jar'

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] =0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def predict():
    os.system(cmd2)
    os.system(cmd3)
    shutil.move('IntermediateResult.txt', 'static/IntermediateResult.txt')
    shutil.move('FinalResult.txt', 'static/FinalResult.txt')
    shutil.copy('inputData/output.jpg', 'static/output.jpg')

@app.route('/', methods=['GET'])
def upload_file():

    if request.method=='GET':
        return render_template('index.html')
    
@app.route('/result', methods=['POST'])
def infer():
    if request.method == 'POST':
        print(request.files)
        if 'image' not in request.files:
            print('there is no image_file in form!')
            return redirect(request.url)

        image_file = request.files['image']
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'capture.png')
        image_file.save(path)
    # return path
        predict()
   
    return render_template('result.html')

@app.route('/webcam', methods=['POST'])
def webcam():
    os.system(cmd1)
    predict()
    return render_template('result.html')

@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug= True) 
