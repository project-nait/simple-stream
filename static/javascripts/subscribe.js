(function() {
  let imageEl = document.getElementById('stream-content')

  let eventSrc = new EventSource('/subscribe')

  eventSrc.onmessage = function(e) {
    console.log(e.data)
  }
})()
