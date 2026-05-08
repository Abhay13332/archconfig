
      try {
        (function h({contextBridge:d,ipcRenderer:l}){if(!l)return;l.on("__ELECTRON_LOG_IPC__",(a,e)=>{window.postMessage({cmd:"message",...e})}),l.invoke("__ELECTRON_LOG__",{cmd:"getOptions"}).catch(a=>console.error(new Error(`electron-log isn't initialized in the main process. Please call log.initialize() before. ${a.message}`)));const o={sendToMain(a){try{l.send("__ELECTRON_LOG__",a)}catch(e){console.error("electronLog.sendToMain ",e,"data:",a),l.send("__ELECTRON_LOG__",{cmd:"errorHandler",error:{message:e?.message,stack:e?.stack},errorName:"sendToMain"})}},log(...a){o.sendToMain({data:a,level:"info"})}};for(const a of["error","warn","info","verbose","debug","silly"])o[a]=(...e)=>o.sendToMain({data:e,level:a});if(d&&process.contextIsolated)try{d.exposeInMainWorld("__electronLog",o)}catch{}typeof window=="object"?window.__electronLog=o:__electronLog=o})(require('electron'));
      } catch(e) {
        console.error(e);
      }
    