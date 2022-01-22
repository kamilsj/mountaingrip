function update(user_id){
    checkNotifications();
}

(function () {
    var form = document.getElementsByTagName('form')[0]
    var progressBar = document.getElementsByClassName('progress-bar')[0]

    form.addEventListener('progress', function (event) {
        // event.detail.progress is a value between 0 and 1
        var percent = Math.round(event.detail.progress * 100)

        progressBar.setAttribute('style', 'width:' + percent + '%')
        progressBar.setAttribute('aria-valuenow', percent)
        progressBar.innerText = percent + '%'
    })
})()