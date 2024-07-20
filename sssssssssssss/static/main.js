document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('inputForm');
    const stackContainer = document.getElementById('stackContainer');

    function updateStack() {
        fetch('/stack')
            .then(response => response.json())
            .then(stack => {
                stackContainer.innerHTML = ''; // 이전 내용 지우기

                // 최대 5개의 박스를 생성
                for (let i = 0; i < 5; i++) {
                    const box = document.createElement('div');
                    box.className = i < stack.length ? 'box' : 'empty-box'; // 스택 원소가 있는지 여부에 따라 클래스 설정

                    if (i < stack.length) {
                        box.textContent = stack[i]; // 원소가 있는 경우 내용 추가
                    }

                    stackContainer.appendChild(box);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const inputBox = document.getElementById('inputBox');
        const input_value = inputBox.value;

        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ inputBox: input_value }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateStack(); // 스택 업데이트
                inputBox.value = '';
                inputBox.focus();
            } else {
                console.error('Error:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // 페이지 로드 시 초기 스택 업데이트
    updateStack();
});
