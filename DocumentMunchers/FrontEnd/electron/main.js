const { app, BrowserWindow } = require('electron')
const path = require('path')
const isDev = require('electron-is-dev')
const { title } = require('process')
const http = require("http")

const sendKillRequest = () => {
    const url = 'http://localhost:5000/api/kill';
    
    // Using http module (since you're using localhost:5000)
    const req = http.get(url, (res) => {
        console.log(`Kill request sent. Status Code: ${res.statusCode}`);
    });
    
    req.on('error', (err) => {
        console.error('Error sending kill request:', err.message);
    });
    
    req.on('timeout', () => {
        console.log('Kill request timed out');
        req.destroy();
    });
    
    // Set timeout (optional)
    req.setTimeout(5000); // 5 second timeout
}

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  })

  if (isDev) {
    win.loadURL('http://localhost:5173')
    win.webContents.openDevTools()
  } else {
    // Load renderer/index.html
    win.loadFile(path.join(__dirname, '..', 'dist', 'renderer', 'index.html'))
  }
}

app.whenReady().then(createWindow)

app.on('before-quit', (event) => {
    // This fires when the app is quitting (Cmd+Q, app.quit(), etc.)
    sendKillRequest(); // Uncomment if you want to send request on app quit too
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin'){
    const baseUrl = 'http://localhost:5000/api/kill';
        

    const response = fetch(baseUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify([])
    });
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})