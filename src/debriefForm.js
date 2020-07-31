"use strict";
/**
 * Draw the debrief form the participant will see at the end of the experiment.
 *
 * @param submitFunction {function} - function to be called when the submit button is pressed
 */
export default function drawDebriefForm() {
    let owner = this;
    // Create form
    let div = document.querySelector('.jspsych-content').appendChild(document.createElement('div'));
    div.id = 'debriefContainer';
    div.className = 'debrief';
    let header = div.appendChild(document.createElement('h1'));
    header.id = 'debriefTitle';
    div.className = 'debrief';
    header.innerText = 'finally...';
    let form = div.appendChild(document.createElement('form'));
    form.id = 'debriefForm';
    form.className = 'debrief';
    let dots = form.appendChild(document.createElement('div'));
    dots.id = 'dotsQContainer';
    dots.className = 'debrief';
    let dotsQ = dots.appendChild(document.createElement('div'));
    dotsQ.id = 'dotsQuestion';
    dotsQ.className = 'debrief';
    dotsQ.innerHTML = 'On the dots task, the advisors differed from one another in their advice-giving. ' +
        'What do you think the difference between the advisors was? <em>(optional)</em>';
    let dotsA = dots.appendChild(document.createElement('textarea'));
    dotsA.id = 'dotsAnswer';
    dotsA.className = 'debrief';
    let estimate = form.appendChild(document.createElement('div'));
    estimate.id = 'estimateQContainer';
    estimate.className = 'debrief';
    let estimateQ = estimate.appendChild(document.createElement('div'));
    estimateQ.id = 'estimateQuestion';
    estimateQ.className = 'debrief';
    estimateQ.innerHTML = 'On the estimation task, what were your thoughts and feelings on the statistical model? <em>(optional)</em>';
    let estimateA = estimate.appendChild(document.createElement('textarea'));
    estimateA.id = 'estimateAnswer';
    estimateA.className = 'debrief';
    let ok = form.appendChild(document.createElement('button'));
    ok.innerText = 'submit';
    ok.className = 'debrief jspsych-btn';
    ok.onclick = function(e){
        e.preventDefault();
        owner.debriefFormSubmit(form);
    };
}