describe('My First Test', function() {
  // it('Consent Form No Tick', function() {
  //   cy.viewport('macbook-15') 
  // 	cy.visit('https://acclab.psy.ox.ac.uk/~saiyer/AdvisorChoice/?consent=true&PROLIFIC_PID=RAJCYPRESS')
  //   cy.contains('I am willing to participate').click()
  // })
  it('Consent Form Both Tick, Proceed', function() {

   //  Cypress.Commands.add("dragTo", { prevSubject: "element" }, (subject, targetEl) => 
   //  {
   //    cy.wrap(subject).trigger("dragstart");
   //    cy.get(targetEl).trigger("drop");
   //  });

   //  cy.on('uncaught:exception', (err, runnable) => {
   //    expect(err.message).to.include('something about the error')
   //    done()
   //    return false
   //  })

   cy.viewport('macbook-15') 
   cy.visit('https://acclab.psy.ox.ac.uk/~saiyer/AdvisorChoice/?consent=true&PROLIFIC_PID=RAJCYPRESS4')
  	// cy.get('[type="checkbox"]').check()
  	// cy.contains('I am willing to participate').click()
  	// cy.url().should('include', '?consent=true') 

  	// cy.get('[id=demoCommentAnswer0]').type('HI!')
  	// cy.contains('next').click()
  	// cy.get('[id=demoCommentAnswer0]').type('{selectall}')
  	// cy.get('[id=demoCommentAnswer0]').type('male!')
  	// cy.contains('next').click()
  	// cy.get('[id=demoCommentAnswer0]').type('{selectall}')
  	// cy.get('[id=demoCommentAnswer0]').type('m')
  	// cy.contains('next').click()

   //  cy.get('[id=demoCommentAnswer1]').type('HI!')
   //  cy.get('[id="demoCommentContainer1"]').within(() => {cy.contains('next').click()})
   //  cy.get('[id=demoCommentAnswer1]').type('{selectall}')
   //  cy.get('[id=demoCommentAnswer1]').type('14')
   //  cy.get('[id="demoCommentContainer1"]').within(() => {cy.contains('next').click()})
   //  cy.get('[id=demoCommentAnswer1]').type('{selectall}')
   //  cy.get('[id=demoCommentAnswer1]').type('5')
   //  cy.get('[id="demoCommentContainer1"]').within(() => {cy.contains('next').click()})

   //  cy.get('[id=demoCommentAnswer2]').type('HI!')
   //  cy.get('[id="demoCommentContainer2"]').within(() => {cy.contains('submit').click()})
   //  cy.get('[id=demoCommentAnswer2]').type('{selectall}')
   //  cy.get('[id=demoCommentAnswer2]').type('24')
   //  cy.get('[id="demoCommentContainer2"]').within(() => {cy.contains('submit').click()})

   cy.contains('Next').click()

    for (let c = 1; c<15; c++)
    {
      cy.contains('Next >').click()
    }

    var vals = [];
    let val; 
    var ests = [];
    let est;
    for (let n = 1; n < 991; n++)
    {
        let v = Math.round((Math.random() * 100));
        if (v == 50)
        {
          vals.push(51);
        }
        else
        {
          vals.push(v);
        }

    }
    console.log(vals);
    for (let m = 1; m < 31; m++)
    {
        let es = Math.round((Math.random() * 100));
        ests.push(es);
    }
      for (let prac = 1; prac < 3; prac ++)
      {
        for (let x = 1; x <31; x++)
        {

            cy.wait(2500);

          // React overrides the DOM node's setter, so get the original, as per the linked Stack Overflow
          const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          cy.get('[id="jspsych-canvas-sliders-response-slider0"]').then(($range) => {
            // get the DOM node
            const range = $range[0];
            // set the value manually
            nativeInputValueSetter.call(range, vals[x*prac]);
            // now dispatch the event
            range.dispatchEvent(new Event('change', { value: vals[x*prac], bubbles: true }));
          });


          cy.get('[id="jspsych-canvas-sliders-response-next"]').click();


        }
        cy.contains('Next >').click();
    }

    for (let d = 1; d<5; d++)
    {
      cy.contains('Next').click()
    }

    for (let y = 1; y <61; y++)
    {

        cy.wait(2500);

      // React overrides the DOM node's setter, so get the original, as per the linked Stack Overflow
      const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      cy.get('[id="jspsych-canvas-sliders-response-slider0"]').then(($range) => {
        // get the DOM node
        let range1 = $range[0];
        // set the value manually
        nativeInputValueSetter.call(range1, vals[y]);
        // now dispatch the event
        range1.dispatchEvent(new Event('change', { value: vals[y], bubbles: true }));
      });

      cy.get('[id="jspsych-canvas-sliders-response-next"]').click();

      cy.wait(2500);

      //let imageCount;

      //imageCount = Cypress.$(cy.get('div[id="jspsych-content"] select[id="jspsych-jas-present-advice-image0"] div')).length;

      //console.log(imageCount);

      cy.get('[id="jspsych-jas-present-advice-image0"]')
        .its('length')
        .then(lengthOfClassElements => {
          if (lengthOfClassElements > 1)
          {
            cy.get('[id="jspsych-jas-present-advice-image0"]').first().click({timeout: 500});
          }

        });

      //console.log(imageCount);

      // imageCount = cy.get('[id="jspsych-content"]').find('[id="jspsych-jas-present-advice-image0"]');
      // console.log(cy.get('[id="jspsych-content"]').find('[id="jspsych-jas-present-advice-image0"]'));

      // if (imageCount > 1)
      // {
      //   cy.get('[id="jspsych-jas-present-advice-image0"]').first().click({timeout: 500});
      // }
      
      // React overrides the DOM node's setter, so get the original, as per the linked Stack Overflow
      cy.get('[id="jspsych-canvas-sliders-response-slider0"]').then(($range) => {
        // get the DOM node
        let range2 = $range[0];
        // set the value manually
        nativeInputValueSetter.call(range2, vals[y]);
        // now dispatch the event
        range2.dispatchEvent(new Event('change', { value: vals[y], bubbles: true }));
      });


       cy.get('[id="jspsych-canvas-sliders-response-next"]').click();


    }
    cy.contains('Next >').click();


    for (let d = 1; d<4; d++)
    {
      cy.contains('Next').click()
    }

    for (let exp = 1; exp < 5; exp ++)
      {
        for (let y = 1; y <31; y++)
        {

            cy.wait(2500);

          // React overrides the DOM node's setter, so get the original, as per the linked Stack Overflow
          const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          cy.get('[id="jspsych-canvas-sliders-response-slider0"]').then(($range) => {
            // get the DOM node
            let range1 = $range[0];
            // set the value manually
            nativeInputValueSetter.call(range1, vals[y*exp+1]);
            // now dispatch the event
            range1.dispatchEvent(new Event('change', { value: vals[y*exp+1], bubbles: true }));
          });

          cy.get('[id="jspsych-canvas-sliders-response-next"]').click();

          cy.wait(2500);

          //let imageCount;

          //imageCount = Cypress.$(cy.get('div[id="jspsych-content"] select[id="jspsych-jas-present-advice-image0"] div')).length;

          //console.log(imageCount);

          cy.get('[id="jspsych-jas-present-advice-image0"]')
            .its('length')
            .then(lengthOfClassElements => {
              if (lengthOfClassElements > 1)
              {
                cy.get('[id="jspsych-jas-present-advice-image0"]').first().click({timeout: 500});
              }

            });

          //console.log(imageCount);
 
          // imageCount = cy.get('[id="jspsych-content"]').find('[id="jspsych-jas-present-advice-image0"]');
          // console.log(cy.get('[id="jspsych-content"]').find('[id="jspsych-jas-present-advice-image0"]'));

          // if (imageCount > 1)
          // {
          //   cy.get('[id="jspsych-jas-present-advice-image0"]').first().click({timeout: 500});
          // }
          
          // React overrides the DOM node's setter, so get the original, as per the linked Stack Overflow
          cy.get('[id="jspsych-canvas-sliders-response-slider0"]').then(($range) => {
            // get the DOM node
            let range2 = $range[0];
            // set the value manually
            nativeInputValueSetter.call(range2, vals[y*exp+1]);
            // now dispatch the event
            range2.dispatchEvent(new Event('change', { value: vals[y*exp+1], bubbles: true }));
          });


           cy.get('[id="jspsych-canvas-sliders-response-next"]').click();

        }
        cy.contains('Next >').click();
    }

    cy.contains('Next >').click();
    for (let d = 0; d<12; d++)
    {
       let id = '[id=questionCommentContainer' + d +  ']';
       let choice = Math.floor(Math.random() * 5) + 1;
       let value = 'input[value=' + choice +  ']';
       cy.get(id).within(() => {
        cy.get('[id="options"]').within(() => {
          cy.get(value).click()
        })
       });
       if (d==11)
       {
          cy.get(id).within(() => {
            cy.contains('submit').click();
          });
       }
       else
       {
          cy.get(id).within(() => {
            cy.contains('next').click();
          });  
       } 
    }

    cy.contains('Next >').click();

    for (let d = 1; d<8; d++)
    {
      cy.contains('Next').click();
    }


    for (let e = 0; e < 10; e++)
    {
      let id = '[id="estimateCommentAnswer1' + e +  '"]';
      cy.get(id).type(ests[e]);
      let container = '[id=estimateCommentContainer' + e +  ']';
      if (e==9)
       {
          cy.get(container).within(() => {
          cy.contains('submit').click();
          cy.contains('submit').click();
          cy.contains('submit').click();
        });
       }
       else
       {
        cy.get(container).within(() => {
          cy.contains('next').click();
          cy.contains('next').click();
          cy.contains('next').click();
        });
       } 
    }

    for (let d = 1; d<3; d++)
    {
      cy.contains('Next').click()
    }

    for (let e = 10; e < 20; e++)
    {
      let num = e-10;
      let id = '[id="estimateCommentAnswer1' + num +  '"]';
      let container = '[id=estimateCommentContainer' + num +  ']';
      cy.get(id).type(ests[e]);
      if (e==19)
       {
        cy.get(container).within(() => {
          cy.contains('submit').click();
        });
       }
       else
       {
        cy.get(container).within(() => {
          cy.contains('next').click();
        });
       } 
    }

    cy.contains('next').click();

    for (let d = 1; d<3; d++)
    {
      cy.contains('Next').click()
    }

    for (let e = 20; e < 30; e++)
    {
      let num = e-20;
      let id = '[id="estimateCommentAnswer1' + num +  '"]';
      let container = '[id=estimateCommentContainer' + num +  ']';
      cy.get(id).type(ests[e]);
      if (e==29)
       {
        cy.get(container).within(() => {
          cy.contains('submit').click();
        });
       }
       else
       {
        cy.get(container).within(() => {
          cy.contains('next').click();
        });
       } 
    }

    cy.get('[id="estimateCommentAnswerReward"]').type('5');
    cy.contains('submit').click();
    cy.get('[id="estimateCommentModelGuess"]').type('25');
    cy.contains('submit').click();
    cy.get('[id="estimateCommentOwnGuess"]').type('15');
    cy.contains('submit').click();
    cy.contains('Next >').click();
    cy.contains('next').click();

    for (let d = 0; d<2; d++)
    {
       let id = '[id=questionCommentContainer' + d +  ']';
       let choice = Math.floor(Math.random() * 5) + 2;
       let value = 'input[value=' + choice +  ']';
        cy.get(id).within(() => {
        cy.get('[id="options"]').within(() => {
          cy.get(value).click()
        })
       });
       if (d==1)
       {
          cy.get(id).within(() => {
            cy.contains('submit').click();
          });
       }
       else
       {
          cy.get(id).within(() => {
            cy.contains('next').click();
          });
       } 
    }



      cy.get('[id="dotsAnswer"]').type('HI!');
    cy.get('[id="estimateAnswer"]').type('HI!');
    cy.contains('submit').click()
  })
})