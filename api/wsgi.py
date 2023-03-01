import json
import os
import re
import base64
import zipfile
from flask import Flask
from flask import Response, request

app = Flask(__name__)
app.run()

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data')

def search_pdf(title):
    for conf in os.listdir(data_path):
        file = title + '.pdf'
        if file in os.listdir(os.path.join(data_path, conf, '_all_papers')):
            return os.path.join(data_path, conf, '_all_papers', file)

def search_all(title):
    for conf in os.listdir(data_path):
        if title in os.listdir(os.path.join(data_path, conf, 'folders')):
            return os.path.join(data_path, conf, 'folders', title)

@app.route('/api/getConfList')
def get_conf_list():
    conf_list = os.listdir(data_path)

    response = Response()
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'
    response.set_data(json.dumps(conf_list))
    return response


@app.route('/downloadAll/<title_base64>')
def download_all(title_base64):
    title = base64.decodebytes(title_base64.encode()).decode()

    response = Response()
    response.status_code = 200
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] =  'attachment; filename="{}.zip";'.format(title)

    with zipfile.ZipFile('all.zip', 'w') as z:
        path = search_all(title)
        for file in os.listdir(path):
            z.write(os.path.join(path, file), arcname=file)
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

    path = search_pdf(title)
    with open(path, 'rb') as pdf:
        response.set_data(pdf.read())
    return response

@app.route('/view/<title_base64>')
def view_pdf(title_base64):
    title = base64.decodebytes(title_base64.encode()).decode()
    response = Response()
    response.status_code = 200
    response.headers['Content-Type'] = 'application/pdf'

    path = search_pdf(title)
    with open(path, 'rb') as pdf:
        response.set_data(pdf.read())
    return response

@app.route('/api/getPapers')
def get_papers():
    papers = []

    for conf in os.listdir(data_path):
        folders_path = os.path.join(data_path, conf, 'folders')
        titles = os.listdir(folders_path)

        for title in titles:
            title_base64 = base64.encodebytes(title.encode()).decode().strip()
            paper = {'title': title, 'titleBase64': title_base64, 'authors': '', 'abstract': '', 'conf': conf}

            if os.path.exists(os.path.join(folders_path, title, 'abstract.html')):
                with open(os.path.join(folders_path, title, 'abstract.html')) as rf:
                    content = rf.read()

                    authors = re.findall('(?<=author" content=").*?(?=")', content)
                    authors = ', '.join([' '.join(author.split(', ')[: : -1]) for author in authors])
                    abstract = re.search('(?<=Abstract)[\s\S]*?(?=\<\/p\>)', content).group()
                    abstract = re.sub('\<.*?\>', '', abstract).strip()

                    paper['authors'] = authors
                    paper['abstract'] = abstract
            papers.append(paper)

    response = Response()
    response.status_code = 200
    response.headers['content-type'] = 'application/json; charset=utf-8'
    response.set_data(json.dumps(papers))

    return response