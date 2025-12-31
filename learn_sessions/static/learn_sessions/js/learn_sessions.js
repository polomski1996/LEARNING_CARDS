export class LearnSession {
    constructor() {
        this.cards = document.querySelectorAll('.card');
    }

    init() {
        this.cards.forEach(card => {
            this.bindCardFlip(card);
            this.bindRating(card);
            this.bindFinishSession();
        });
    }

    refresh_rating(card_id) {
        this.cards.forEach(card => {
            const level = 
            document.querySelector('.mastered_lvl').innerHTML = '<p><h2>' + level + '</h2></p>';
        })
    }

    bindCardFlip(card) {
        const inner = card.querySelector('.card-inner');

        inner.addEventListener('click', (e) => {
            // nie obracaj jeśli kliknięto przycisk
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

    async sendMasteredLevel(cardId, level) {
        try {
            const response = await fetch('/learning/api/rate-card/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    card_id: cardId,
                    mastered_level: level
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
            console.log('Updated card', cardId, 'to level', level);
        } else {
            console.error('Card element not found for ID:', cardId);
        }
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

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}
