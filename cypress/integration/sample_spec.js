describe('My First Test', function() {
  it('Consent Form No Tick', function() {
  	cy.visit('raj925.github.io/AdvisorChoice/index.html')
    cy.contains('I am willing to participate').click()
  })
  it('Consent Form Both Tick, Proceed', function() {
  	cy.visit('raj925.github.io/AdvisorChoice/index.html')
  	cy.get('[type="checkbox"]').check()
  	cy.contains('I am willing to participate').click()
  	cy.url().should('include', '?consent=true') 

  	cy.get('[id=demoCommentAnswer0]').type('HI!')
  	cy.contains('next').click()
  	cy.get('[id=demoCommentAnswer0]').type('{selectall}')
  	cy.get('[id=demoCommentAnswer0]').type('male!')
  	cy.contains('next').click()
  	cy.get('[id=demoCommentAnswer0]').type('{selectall}')
  	cy.get('[id=demoCommentAnswer0]').type('m')
  	cy.contains('next').click()

  	cy.get('[id=demoCommentAnswer1]').type('HI!')
  	cy.contains('submit').click()
  	cy.get('[id=demoCommentAnswer1]').type('{selectall}')
  	cy.get('[id=demoCommentAnswer1]').type('14')
  	cy.contains('submit').click()
  	cy.get('[id=demoCommentAnswer1]').type('{selectall}')
  	cy.get('[id=demoCommentAnswer1]').type('45')
  	cy.contains('submit').click()
  	cy.get('[id=demoCommentAnswer1]').type('{selectall}')
  	cy.get('[id=demoCommentAnswer1]').type('25')
  	cy.contains('submit').click()

  	cy.contains('Next').click()

  	cy.get('[id=jspsych-canvas-sliders-response-slider0]').click(Math.floor(Math.random() * 100),0)
  	cy.get('[id=jspsych-canvas-sliders-response-slider0]').click(Math.floor(Math.random() * 100),0)
  	cy.get('[id=jspsych-canvas-sliders-response-slider0]').click(Math.floor(Math.random() * 100),0)
  	cy.get('[id=jspsych-canvas-sliders-response-slider0]').click(Math.floor(Math.random() * 100),0)
  	cy.get('[id=jspsych-canvas-sliders-response-slider0]').click(Math.floor(Math.random() * 100),0)
  	cy.get('[id=jspsych-canvas-sliders-response-slider0]').click(Math.floor(Math.random() * 100),0)

  })
})