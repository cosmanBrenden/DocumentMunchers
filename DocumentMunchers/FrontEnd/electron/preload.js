const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  send: (channel, payload) => ipcRenderer.send(channel, payload),
  receive: (channel, func) => ipcRenderer.on(channel, (event, ...args) => func(...args))
})
