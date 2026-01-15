export class LearnSession {
    constructor() {
        this.cards = document.querySelectorAll('.card');
    }

    init() {
        this.cards.forEach(card => {
            this.bindCardFlip(card);
            this.bindRating(card);
            this.bindFinishSession();
            this.bindJudgeAnswer(card);
        });
        this.colourTableResultsRows();
    }

    bindCardFlip(card) {
        const inner = card.querySelector('.card-inner');
        const cardType = card.dataset.cardType;

        if (cardType !== 'open_card') return;

        inner.addEventListener('click', (e) => {
            
            if (e.target.closest('.rate-btn')) return;

            inner.classList.toggle('flipped');
        });
    }

    bindRating(card) {
        const buttons = card.querySelectorAll('.rate-btn');
        const cardId = card.dataset.cardId;

        buttons.forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.stopPropagation();

                const level = btn.dataset.level;

                await this.sendMasteredLevel(cardId, level);

                btn.classList.add('active');
            });
        });
    }

    async sendMasteredLevel(cardId, level) {
        const segments = window.location.pathname.split('/').filter(segment => segment !== '');
        const sessionId = segments[segments.length - 1];
        try {
            const response = await fetch('/learning/api/rate-card/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    card_id: cardId,
                    mastered_level: level,
                    session_id: sessionId
                })
            });

            if (!response.ok) {
                throw new Error('Failed to save rating');
            }
        } catch (err) {
            console.error(err);
        }
        
        // Update card master_lvl on front, find card by data-card-id
        const cardElement = document.querySelector(`.card[data-card-id="${cardId}"]`);
        
        if (cardElement) {
            cardElement.querySelector('.mastered_lvl').innerHTML = `<h2>${level}</h2>`;
            // console.log('Updated card', cardId, 'to level', level, 'session_ID:  ', sessionId);
        } else {
            console.error('Card element not found for ID:', cardId);
        }
    }


    async sendClosedAnswer(cardId, answer){
        const cardElement = document.querySelector(`.card[data-card-id="${cardId}"] .card-inner`);
        const segments = window.location.pathname.split('/').filter(segment => segment !== '');
        const sessionId = segments[segments.length - 1];
        try {
            const response = await fetch('/learning/api/judge-answer/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    card_id: cardId,
                    answer: answer,
                    session_id: sessionId
                })
            });

            if (!response.ok) {
                throw new Error('Failed to bring answer')
            }

            // ADD COLORS HIGHLIGHT
            const data = await response.json();
            if (data.result === "correct") {
                cardElement.classList.add('correct');
                setTimeout(() => {
                    cardElement.classList.remove('correct');
                }, 400);
            }
            else if (data.result === "incorrect") {
                cardElement.classList.add('incorrect');
                setTimeout(() => {
                    cardElement.classList.remove('incorrect');
                }, 400);
            }

        } catch (err) {
            console.error(err);
        }
    }

    bindJudgeAnswer(card) {
        const cardType = card.dataset.cardType;
        const ansBtns = card.querySelectorAll('.answer_btn');
        const cardId = card.dataset.cardId;
        
        if (cardType !== 'closed_card') return;

        ansBtns.forEach(button => {
            button.addEventListener('click', async (e) => {
                e.stopPropagation();

                const answer = button.dataset.level;
                await this.sendClosedAnswer(cardId, answer);
            })
            
        });


    }

    bindFinishSession(){
        const finish_btn = document.querySelector('#finish_session');
        const segments = window.location.pathname.split('/').filter(segment => segment !== '');
        const sessionId = segments[segments.length - 1];

        if (!finish_btn){
            console.error('Element #finish_session does not exist!');
            return;
        }

        finish_btn.addEventListener('click', (e) => {
            this.sendFinish_Sesssion(sessionId)
                .then(() => {
                    window.location.href = '/account/';
                })
                .catch(error => {
                    console.error('Error during finishing session:', error);
                    alert('We were not manage to finish the session.')
                });
        });
    }

    async sendFinish_Sesssion(id){
        try {
            const response = await fetch('/learning/api/finish_session/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    is_finished: true,
                    finished_at: new Date().toISOString(),
                    session_id: id
                })
            },);

            if (!response.ok) {
                throw new Error('Failed to save finish session');
            }
        } catch (err) {
            console.error(err);
        }
    }

    // Apply row background colors based on is_correct and is_better values
    colourTableResultsRows(){

        const tableRows = document.querySelectorAll(".log-table tbody tr");

        tableRows.forEach((row) => {
            // Get the third cell which contains Correct/Progress information
            const resultCell = row.cells[2]

            if (resultCell) {
            const resultText = resultCell.textContent.trim()

            // Check for is_correct values (True/False)
            if (resultText === "True") {
                row.classList.add("bg-correct")
            } else if (resultText === "False") {
                row.classList.add("bg-incorrect")
            }
            // Check for is_better values (BETTER/WORSE/STILL)
            else if (resultText === "BETTER") {
                row.classList.add("bg-better")
            } else if (resultText === "WORSE") {
                row.classList.add("bg-worse")
            }
            // STILL - no class added, keeps default background
            }
        })
        console.log('hej, funcja colourTableResultsRows działa')
    }



    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}
