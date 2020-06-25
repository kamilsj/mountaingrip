

function addFriend(userId) {

    $.ajax({
        type: 'POST',
        url: 'ajax/addfriend/'+userId+'/',
        success: function (response) {

            alert('kamil')

        }
    })

}