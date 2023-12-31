var timer_div = document.getElementById("timer");
var studied_secs = 0;
var studied_secs_add = 0;
var timer;

var toggle = document.getElementById("toggle");
var isTimerRunning = false;

var todo_ul = document.getElementById("todo");
var todo_end_ul = document.getElementById("todo_end");

if (sessionStorage.getItem("Access-Token") == null) {
  alert("세션이 만료되었거나 잘못된 접근입니다.");
  sessionStorage.clear();
  location.href = "index.html";
}

sync_with_svr();

toggle.addEventListener("click", () => {
  if (isTimerRunning) {
    toggle.textContent = "시작!";
    alert(
      "(???) 재수할 수 있는 방식, 총 세 가지 있어요.\n첫째, 자기가 못 한다. 힘들다, 공부가 *같다.\n그러면 재수 할 수 있습니다."
    );
    isTimerRunning = false;
    clearInterval(timer);
    sync_with_svr();
  } else {
    isTimerRunning = true;
    toggle.textContent = "종료!";
    alert(
      "(???) 둘째, 공부를 안 한다.\n하는 척 하고 공부 안 하면 대학 입학.\n불가능합니다.\n서류컷 조치 하겠습니다.\n\n세 번째. 능력 부족. 인성 문제가 있다. \n강제 재수시키겠습니다. \n아시겠습니까."
    );
    timer = setInterval(() => {
      studied_secs_add += 1;
      var tmp_secs = studied_secs + studied_secs_add;
      var hour = 0;
      var min = 0;
      var sec = 0;

      hour = Math.floor(tmp_secs / 3600);
      tmp_secs %= 3600;

      min = Math.floor(tmp_secs / 60);
      tmp_secs %= 60;

      sec = tmp_secs;

      timer_div.textContent =
        String(hour) + "시간 " + String(min) + "분 " + String(sec) + "초";
      sync_with_svr();
    }, 1000);
  }
});

document.getElementById("add_goal").addEventListener("click", () => {
  let goal = document.getElementById("goal_txt");
  let goal_str = goal.value;
  goal.value = "";

  if (goal_str == "") {
    return;
  }

  fetch("http://localhost:4444/add-goal", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      token: sessionStorage.getItem("Access-Token"),
    },
    body: JSON.stringify({
      goal: goal_str,
    }),
  });

  sync_with_svr();
});

function sync_with_svr() {
  fetch("http://localhost:4444/sync-profile", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      token: sessionStorage.getItem("Access-Token"),
    },
    body: JSON.stringify({
      secs: studied_secs_add,
    }),
  })
    .then((rawrsp) => {
      if (rawrsp.ok) {
        return rawrsp.json();
      } else {
        rawrsp.text().then((s) => alert(s));
        sessionStorage.clear();
        location.href = "index.html";
        return null;
      }
    })
    .then((rsp) => {
      if (rsp == null) {
        return;
      }

      studied_secs = Number(rsp["studied_time"]);
      studied_secs_add = 0;

      var tmp_secs = studied_secs + studied_secs_add;
      var hour = 0;
      var min = 0;
      var sec = 0;

      hour = Math.floor(tmp_secs / 3600);
      tmp_secs %= 3600;

      min = Math.floor(tmp_secs / 60);
      tmp_secs %= 60;

      sec = tmp_secs;

      timer_div.textContent =
        String(hour) + "시간 " + String(min) + "분 " + String(sec) + "초";

      var goals = rsp["goals"];
      var ended = 0;
      var not_ended = 0;

      for (let i = 0; i < goals["count"]; i++) {
        if (goals["records"][i]["completed"] == 0) {
          not_ended++;
        } else {
          ended++;
        }
      }

      if (ended) {
        todo_end_ul.innerHTML = "";
      }
      if (not_ended) {
        todo_ul.innerHTML = "";
      }

      for (let i = 0; i < goals["count"]; i++) {
        let node = document.createElement("li");
        node.appendChild(document.createTextNode(goals["records"][i]["goal"]));

        if (goals["records"][i]["completed"] == 0) {
          node.innerHTML +=
            ' <button onclick="goal_completion(' +
            String(goals["records"][i]["idx"]) +
            ');">완료!</button>';
          todo_ul.appendChild(node);
        } else {
          todo_end_ul.appendChild(node);
        }
      }
    });
}

function goal_completion(idx) {
  fetch("http://localhost:4444/goal-completion", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      token: sessionStorage.getItem("Access-Token"),
    },
    body: JSON.stringify({
      idx: String(idx),
    }),
  });

  sync_with_svr();
}
