# Paper-Retrieval

## Project setup

Setup frontend

```
npm install
```

Setup backend

```
cd ./api
pip install -r requirements.txt
```

### Compiles and hot-reloads for development
Before you run serving, you need to create a <code>vue.dev.config.js</code> file which is used to setup backend server address. For example,

```js
module.exports = {
	devServerAddress: 'http://localhost:5000',
}
```

Then you also need to run backend server.

```bash
cd ./api
PAPER_PATH=/path/to/your_pdf_files \
FOLDER_PATH=/path/to/your_paper_folders \
flask run

# The content of the two folders should be like
# ├── FOLDER_PATH
# │   ├── A
# │   │   ├── abstract.html
# │   │   ├── main.pdf
# │   │   └── supp.zip
# │   ├── B
# │   │   ├── abstract.html
# │   │   ├── main.pdf
# │   │   └── supp.pdf
# │   └── ...
# └── PAPER_PATH
#     ├── A.pdf
#     ├── B.pdf
#     └── ...
```

After that you can run a hot-reloads server.

```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
