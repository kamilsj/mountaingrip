
function jointrip(id = 0){

    if(id>0) {
        $.ajax({
            url: '/ajax/jointrip/'+id+'/',
            success: function (response) {

            }
        });
    }else{
        alert('error')
    }
}

function addpost(profile_id=0, trip_id=0){

        $.ajax({
        type: 'POST',
        data:{'profile_id': profile_id, 'trip_id': trip_id},
        url: 'ajax/addpost/',
        success: function (response){

        }
    });


}

function addfriend(profile_id) {

    $.ajax({
        type: 'POST',
        url: 'ajax/addfriend/'+user_id+'/',
        success: function (response) {



        }
    });

}

function checkMessages(user_id) {

    $.ajax({
        url: '/ajax/checkmessages/'+user_id+'/',
        success: function (response){

        }
    });

}