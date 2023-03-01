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
Before you run serving, you need to create a <code>vue.dev.config.js</code> file which is used to set up the backend server address. For example,

```js
module.exports = {
	devServerAddress: 'http://localhost:5000',
}
```

Then you also need to run the backend server.
After that, you can run a hot-reloads server.

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