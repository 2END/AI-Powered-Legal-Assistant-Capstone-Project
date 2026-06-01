function showLoader(){
    document.getElementById("loader").classList.remove("hidden");
}
function hideLoader(){
    document.getElementById("loader").classList.add("hidden");
}

async function summarize(){
    const text = document.getElementById("text").value;
    showLoader();

    const response = await fetch("/summarize",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({text:text})
    });

    const data = await response.json();
    document.getElementById("result").innerText = data.result;
    hideLoader();
}

async function simplify(){
    const text = document.getElementById("text").value;
    showLoader();

    const response = await fetch("/simplify",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({text:text})
    });

    const data = await response.json();
    document.getElementById("result").innerText = data.result;
    hideLoader();
}

async function uploadPDF(){
    const fileInput = document.getElementById("pdfFile");
    const file = fileInput.files[0];

    if(!file){
        alert("Pilih file PDF dulu");
        return;
    }

    showLoader();

    const formData = new FormData();
    formData.append("pdf", file);

    const response = await fetch("/upload_pdf",{
        method:"POST",
        body:formData
    });

    const data = await response.json();
    document.getElementById("result").innerText = data.result;
    hideLoader();
}

async function askQuestion(){
    const question = document.getElementById("question").value;

    if(!question){
        alert("Tulis pertanyaan dulu");
        return;
    }

    showLoader();

    const response = await fetch("/ask",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({question:question})
    });

    const data = await response.json();
    document.getElementById("result").innerText = data.result;
    hideLoader();
}