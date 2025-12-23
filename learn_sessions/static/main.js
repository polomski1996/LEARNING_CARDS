import { LearnSession } from './learn_sessions/js/learn_sessions.js'

//Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new LearnSession().init();
})