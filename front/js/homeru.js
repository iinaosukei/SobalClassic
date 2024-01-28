let postCount = 0;
let maxCount = 5;
async function showApiResult() {
    // ラジオボタンの要素を取得
    const radioButtons = document.getElementsByName('options');

    // 選択されているラジオボタンの値を見つける
    let selectedValue;
    radioButtons.forEach(radioButton => {
        if (radioButton.checked) {
            selectedValue = radioButton.value;
        }
    });

    const url = '/get_chatgpt_response/' + selectedValue
    await postData(url);
}
function showResult() {
    window.location.href = '/result';
}

function redirectUrl(url) {
    window.location.href = url;
}

// 送信するJSONデータ
// POSTリクエストを送信する関数
function postData(url) {
    var data = {
        question: document.getElementById('inputText').value
    };

    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            postCount++;
            json_data = JSON.parse(data);
            document.getElementById('pointResult').innerText = `点数: ${json_data.point}`;
            document.getElementById('textResult').innerText = `評価: ${json_data.detailed_evaluation_criteria}`;
            document.getElementById('totalPoints').innerText = `合計得点: ${json_data.total_points}`;
            document.getElementById('count').innerText = `残り回数: ${maxCount - postCount}`;
            if (maxCount - postCount <= 0) {
                sessionStorage.setItem('result', json_data.total_points);
                let button = document.createElement("button");
                button.setAttribute("type", "button");
                button.setAttribute("onclick", "showResult()");
                button.innerText = "結果を表示"
                document.getElementById('resultButton').append(button);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
