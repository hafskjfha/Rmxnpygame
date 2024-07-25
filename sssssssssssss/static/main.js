document.addEventListener('DOMContentLoaded', function() {
    const stackContainer = document.getElementById('stackContainer');
    const displayArea = document.getElementById('displayArea');
    let lastLetter = '';  // 마지막으로 표시된 letter를 저장하는 변수

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
                    // 성공적인 요청 처리
                    displayArea.style.display = 'block'; // 글자 표시 박스를 보이도록 설정
                    displayArea.textContent = input_value;
                    displayArea.className = 'displayArea success'; // 성공 스타일 적용

                    setTimeout(() => {
                        displayArea.textContent = ''; // 글자 사라지게 설정
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
                                // 응답에서 letter를 추출하여 표시
                                lastLetter = submitData.letter; // 마지막으로 표시된 letter 저장
                                updateStack(); // 스택 업데이트

                                // displayArea에 letter 표시 (계속 유지)
                                displayArea.textContent = lastLetter;
                                displayArea.className = 'displayArea success'; // 성공 스타일 적용
                            } else {
                                console.error('Error:', submitData.error);
                            }
                        })
                        .catch(error => console.error('Error:', error));
                    }, 2000);
                } else {
                    // 실패한 요청 처리
                    displayArea.textContent = input_value;
                    displayArea.className = 'displayArea failure'; // 실패 스타일 적용

                    setTimeout(() => {
                        displayArea.textContent = ''; // 글자 사라지게 설정
                        // 실패한 경우, 마지막 letter 다시 표시
                        displayArea.textContent = lastLetter;
                        displayArea.className = 'displayArea success'; // 성공 스타일 적용
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
