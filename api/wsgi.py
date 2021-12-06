import json
import os
import re
import base64
import zipfile
from flask import Flask
from flask import Response

PAPER_PATH = os.environ.get('PAPER_PATH', '')
FOLDER_PATH = os.environ.get('FOLDER_PATH', '')
assert PAPER_PATH != ''
assert FOLDER_PATH != ''

app = Flask(__name__)
app.run()

@app.route('/downloadAll/<title_base64>')
def download_all(title_base64):
    title = base64.decodebytes(title_base64.encode()).decode()

    response = Response()
    response.status_code = 200
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] =  'attachment; filename="{}.zip";'.format(title)

    with zipfile.ZipFile('all.zip', 'w') as z:
        for file in os.listdir(os.path.join(FOLDER_PATH, title)):
            z.write(os.path.join(FOLDER_PATH, title, file), arcname=file)
    with open('all.zip', 'rb') as z:
        response.set_data(z.read())
    return response

@app.route('/download/<title_base64>')
def download_pdf(title_base64):
    title = base64.decodebytes(title_base64.encode()).decode()
    response = Response()
    response.status_code = 200
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =  'attachment; filename="{}.pdf";'.format(title)

    with open(os.path.join(FOLDER_PATH, title, 'main.pdf'), 'rb') as pdf:
        response.set_data(pdf.read())
    return response

@app.route('/view/<title_base64>')
def view_pdf(title_base64):
    title = base64.decodebytes(title_base64.encode()).decode()
    response = Response()
    response.status_code = 200
    response.headers['Content-Type'] = 'application/pdf'

    with open(os.path.join(PAPER_PATH, title + '.pdf'), 'rb') as pdf:
        response.set_data(pdf.read())
    return response

@app.route('/api/getPapers')
def get_papers():
    titles = os.listdir(FOLDER_PATH)
    papers = []

    for title in titles:
        with open(os.path.join(FOLDER_PATH, title, 'abstract.html')) as rf:
            content = rf.read()

            authors = re.findall('(?<=author" content=").*?(?=")', content)
            authors = ', '.join([' '.join(author.split(', ')[: : -1]) for author in authors])
            abstract = re.search('(?<=Abstract)[\s\S]*?(?=\<\/p\>)', content).group()
            abstract = re.sub('\<.*?\>', '', abstract).strip()
            title_base64 = base64.encodebytes(title.encode()).decode().strip()

            papers.append({'title': title, 'titleBase64': title_base64, 'authors': authors, 'abstract': abstract})

    response = Response()
    response.status_code = 200
    response.headers['content-type'] = 'application/json; charset=utf-8'
    response.set_data(json.dumps(papers))

    return response