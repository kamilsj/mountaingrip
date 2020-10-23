
function addPost(profile_id=0, trip_id=0){

        $.ajax({
        type: 'POST',
        data:{'profile_id': profile_id, 'trip_id': trip_id},
        url: 'ajax/addpost/',
        sukcess: function (response){
            alert('coś tam')
        }
    });


}

function addFriend(profile_id) {

    $.ajax({
        type: 'POST',
        url: 'ajax/addfriend/'+user_id+'/',
        success: function (response) {

            alert('kamil')

        }
    });

}

function checkMessages(user_id) {

    $.ajax({
        type: 'POST',
        url: 'ajax/checkmessages/'+user_id+'/',
        sukcess: function (response){
            alert('coś tam')
        }
    });

}