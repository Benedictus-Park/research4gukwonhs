const btnLogin = document.getElementById("btnlogin");

function performLogin(){
    var email = String(document.getElementById("login_email").value);
    var password = String(document.getElementById("login_pwd").value);
    var loginJSO = {
        "id":email,
        "pwd":password
    };
    var rsp;

    if(email.indexOf('@') == -1 || email.indexOf('.') == -1 || email.length < 3){
        alert("이메일 형식이 잘못되었습니다.");
        return;
    }
    else if(password.length < 8){
        alert("로그인 정보가 틀립니다.");
        return;
    }

    rsp = fetch("localhost:4444/login", {
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
            alert(rawrsp.statusText);
            return null;
        }
    });

    if(rsp != null){
        sessionStorage.setItem("UserName", rsp["uname"]);
        sessionStorage.setItem("Access-Token", rsp["token"]);
        location.href = "localhost/main.html";
    }
}

btnLogin.addEventListener("click", performLogin);