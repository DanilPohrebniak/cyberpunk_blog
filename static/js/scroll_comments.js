window.onload = function() {
    if(window.location.hash === '#comments') {
      let commentLink = document.getElementById('comments');
      commentLink.scrollIntoView();
    }
    if(window.location.hash.includes('#likeComment')) {
        let commentLink = document.getElementById(window.location.hash.slice(1));
        if (commentLink) {
            commentLink.scrollIntoView();
        }
    }
}