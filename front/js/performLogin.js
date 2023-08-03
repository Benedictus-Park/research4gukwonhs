const btnLogin = document.getElementById("btnlogin");

function performLogin(){
    var email = String(document.getElementById("login_email").value);
    var password = String(document.getElementById("login_pwd").value);
    var loginJSO = {
        "email":email,
        "pwd":password
    };

    if(email.indexOf('@') == -1 || email.indexOf('.') == -1 || email.length < 3){
        alert("이메일 형식이 잘못되었습니다.");
        return;
    }
    else if(password.length < 8){
        alert("로그인 정보가 틀립니다.");
        return;
    }

    fetch("http://localhost:4444/login", {
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify(loginJSO)
    }).then((rawrsp) => {
        if(rawrsp.ok){
            return rawrsp.json();
        }
        else{
            rawrsp.text().then((s) => alert(s));
            return null;
        }
    }).then((rsp) => {
        if(rsp == null){
            return;
        }
        
        alert("로그인 성공!");
        sessionStorage.setItem("UserName", rsp["uname"]);
        sessionStorage.setItem("Access-Token", rsp["token"]);
        location.href = "main.html";
    });
}

btnLogin.addEventListener("click", performLogin);