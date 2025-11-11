

async function callEcho() {
    const raw = document.getElementById("payload").value;
    let json;
    try { json = JSON.parse(raw); } catch (e) { alert("Invalid JSON"); return; }
    const res = await fetch("/api/echo", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(json)
    });
    document.getElementById("result").textContent = await res.text();
}

async function upload() {
    const f = document.getElementById("fileInput").files[0];
    if (!f) {
        alert("pick a file"); 
        return; 
    }

    const fd = new FormData();
    fd.append("file", f);
    const r = await fetch("/upload", { method: "POST", body: fd });
    document.getElementById("uploadResult").textContent = await r.text();
}