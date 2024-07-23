document.addEventListener('DOMContentLoaded', function() {
    const stackContainer = document.getElementById('stackContainer');
    const displayArea = document.getElementById('displayArea');

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

    function handleSubmit(event) {
        event.preventDefault();
        const inputBox = document.getElementById('userInput');
        const input_value = inputBox.value.trim();

        if (input_value) {
            fetch('/api/su', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ inputBox: input_value }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 성공 시 글자를 1초 동안 보여준 후 스택에 업데이트
                    const resultElement = document.createElement('div');
                    resultElement.textContent = input_value;
                    resultElement.className = 'success';
                    displayArea.appendChild(resultElement);

                    setTimeout(() => {
                        displayArea.removeChild(resultElement);
                        // 스택 업데이트 요청
                        fetch('/submit', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ inputBox: input_value }),
                        })
                        .then(response => response.json())
                        .then(submitData => {
                            if (submitData.success) {
                                updateStack(); // 스택 업데이트
                            } else {
                                console.error('Error:', submitData.error);
                            }
                        })
                        .catch(error => console.error('Error:', error));
                    }, 1000);
                } else {
                    // 실패 시 글자에 취소선 추가 후 1초 동안 보여줌
                    const resultElement = document.createElement('div');
                    resultElement.textContent = input_value;
                    resultElement.className = 'failure';
                    resultElement.style.textDecoration = 'line-through';
                    displayArea.appendChild(resultElement);

                    setTimeout(() => {
                        displayArea.removeChild(resultElement);
                        inputBox.value = ''; // 입력값 지우기
                    }, 1000);
                }

                // 입력 필드 지우기
                inputBox.value = '';
                inputBox.focus();
            })
            .catch(error => console.error('Error:', error));
        }
    }

    // Add event listener for the submit button
    document.getElementById("submitButton").addEventListener("click", handleSubmit);

    // Add event listener for the input field to detect "Enter" key press
    document.getElementById("userInput").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();  // Prevent form submission if the input is inside a form
            handleSubmit(event);
        }
    });

    // 페이지 로드 시 초기 스택 업데이트
    updateStack();
});
