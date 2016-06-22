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

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if( request.message === "clicked_browser_action" ) {
      // var firstHref = $("a[href^='http']").eq(0).attr("href");
      var count = getselection().split(' ').length;

      var username = 'Homer'; // hard coding this for now
      var url = 'https://obscure-cliffs-10478.herokuapp.com/' + username + '/add/';

      word_count = { 'count': count }  // this gets build from user highlight/button click

      var posting = $.post( url, word_count );

      posting.done(function( html ) {
        alert(html);
      });


    }
  }
);
