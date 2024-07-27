document.addEventListener('DOMContentLoaded', function() {
    const stackContainer = document.getElementById('stackContainer');
    const displayArea = document.getElementById('displayArea');
    const inputBox = document.getElementById('userInput');
    const inputForm = document.getElementById('inputForm');
    const submitButton = document.getElementById('submitButton');
    const startButton = document.getElementById('startButton');
    let lastLetter = '';  // 마지막으로 표시된 letter를 저장하는 변수
    let myTurn = true;  // 초기 상태는 true

    function updateStack() {
        fetch('/stack')
            .then(response => response.json())
            .then(stack => {
                stackContainer.innerHTML = ''; // 이전 내용 지우기

                // 최대 4개의 박스를 생성
                for (let i = 0; i < 4; i++) {
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

    function updateInputVisibility() {
        if (myTurn) {
            inputBox.disabled = false;
            submitButton.disabled = false;
            inputBox.focus();  // 인풋창에 포커스 설정
        } else {
            inputBox.disabled = true;
            submitButton.disabled = true;
        }
    }

    function handleSubmit(event) {
        event.preventDefault();
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

                    // myTurn을 false로 설정
                    myTurn = false;
                    updateInputVisibility();

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

                                // /api/com에서 단어 받아오기
                                fetch('/api/com')
                                    .then(response => response.json())
                                    .then(comData => {
                                        if (comData.word) {
                                            displayArea.textContent = comData.word; // 단어 표시
                                            setTimeout(() => {
                                                displayArea.textContent = ''; // 2초 후 단어 지우기

                                                if (comData.game === 'ing') {
                                                    // myTurn을 true로 설정
                                                    myTurn = true;
                                                    updateInputVisibility();

                                                    // 스택 업데이트 요청
                                                    fetch('/submit', {
                                                        method: 'POST',
                                                        headers: {
                                                            'Content-Type': 'application/json',
                                                        },
                                                        body: JSON.stringify({ inputBox: comData.word }),
                                                    })
                                                    .then(response => response.json())
                                                    .then(updateData => {
                                                        if (updateData.success) {
                                                            lastLetter = updateData.letter;
                                                            updateStack();
                                                            displayArea.textContent = lastLetter; // 마지막으로 표시된 letter 유지
                                                            displayArea.className = 'displayArea success';
                                                        } else {
                                                            console.error('Error:', updateData.error);
                                                        }
                                                    })
                                                    .catch(error => console.error('Error:', error));
                                                } else if (comData.game === 'comwin') {
                                                    displayArea.textContent = `컴퓨터 승리!`;
                                                    displayArea.className = 'displayArea user_lose';
                                                } else if (comData.game === 'userwin') {
                                                    displayArea.textContent = '사용자 승리!';
                                                    displayArea.className = 'displayArea user_win';
                                                }
                                            }, 2000); // 2초 후 단어 지우기
                                        } else {
                                            console.error('Error:', comData.error);
                                        }
                                    })
                                    .catch(error => console.error('Error:', error));
                            } else {
                                console.error('Error:', submitData.error);
                            }
                        })
                        .catch(error => console.error('Error:', error));
                    }, 2000);
                } else {
                    // 실패한 요청 처리
                    displayArea.textContent = `${data.reason}; ${input_value}`;
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
    submitButton.addEventListener("click", handleSubmit);

    // Add event listener for the input field to detect "Enter" key press
    inputBox.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();  // Prevent form submission if the input is inside a form
            handleSubmit(event);
        }
    });

    // Add event listener for the start button
    startButton.addEventListener("click", function() {
        fetch('/api/st')
            .then(response => response.json())
            .then(startData => {
                if (startData.letter) {
                    // 시작 글자 표시
                    displayArea.style.display = 'block';
                    displayArea.textContent = startData.letter;
                    displayArea.className = 'displayArea success';
                    lastLetter = startData.letter;

                    // myTurn을 true로 설정하고 입력창 가시성 업데이트
                    myTurn = true;
                    updateInputVisibility();

                    // 시작 버튼 비활성화
                    startButton.disabled = true;
                } else {
                    console.error('Error:', startData.error);
                }
            })
            .catch(error => console.error('Error:', error));
    });

    // 페이지 로드 시 초기 스택 업데이트
    updateStack();
});
