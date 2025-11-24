export async function send_Data(test_verisi) {
    console.log("api.js de send data çalıştı");

    try {
        const response=await fetch("http://127.0.0.1:8000/MakeDataAnalayze",{
            method:"POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(test_verisi)
        });
        const data=await response.json();
        console.log("geri dönen data:"+data)
        return data;
    }
    catch (error) {
        console.log("veri yüklemede hata oluştu");
        console.log(error);
    }
    
}

export async function send_Photo(YandanPhoto,ArkadanPhoto) {
    console.log("api.js de send photo çalıştı");

    const formdata=new FormData();
    formdata.append("YandanPhoto",YandanPhoto);
    formdata.append("ArkadanPhoto",ArkadanPhoto);
    try {
        const response=await fetch("http://127.0.0.1:8000/MakePhotoAnalayze",{
            method:"POST",
            body:formdata,
        });
        const data=await response.json();
        return data;
    }
    catch (error) {
        console.log("veri yüklemede hata oluştu");
        console.log(error);
    }
}