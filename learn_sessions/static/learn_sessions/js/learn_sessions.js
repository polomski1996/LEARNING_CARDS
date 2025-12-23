export class LearnSession {
    constructor() {
        this.cards = document.querySelectorAll('.card');
    }

    init() {
        this.cards.forEach(card => {
            this.bindCardFlip(card);
            this.bindRating(card);
        });
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
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}
