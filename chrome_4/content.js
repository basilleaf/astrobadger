// content.js

function getselection() {
    var text = "";

    if (window.getSelection) {
        text = window.getSelection().toString();
    } else if (document.selection && document.selection.type != "Control") {
        text = document.selection.createRange().text;
    }
    return text;
}


// Move that bubble to the appropriate location.
// thanks http://stackoverflow.com/questions/4409378/text-selection-and-bubble-overlay-as-chrome-extension
function renderBubble(html) {
    // Add bubble to the top of the page.
    var bubbleDOM = document.createElement('div');
    bubbleDOM.setAttribute('class', 'selection_bubble');
    document.body.appendChild(bubbleDOM);

    // Close the bubble when we click on the screen.
    // todo: replace this so it doesn't keep adding same even listener
    document.addEventListener('mousedown', function (e) {
      bubbleDOM.style.visibility = 'hidden';
    }, false);

    bubbleDOM.innerHTML = html;

    bubbleDOM.style.visibility = 'visible';

}

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if( request.message === "clicked_browser_action" ) {
      // var firstHref = $("a[href^='http']").eq(0).attr("href");
      var count = getselection().split(' ').length;

      var username = 'Matt'; // hard coding this for now
      var url = 'https://obscure-cliffs-10478.herokuapp.com/';
      // var url = 'http://127.0.0.1:5000/';  // dev

      word_count = { 'count': count }  // this gets build from user highlight/button click

      var posting = $.post( url + username + '/add/', word_count );

      posting.done(function( html ) {

        renderBubble(html);


      });


    }
  }
);
