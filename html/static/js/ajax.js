
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


function showNotifications(){
    $.ajax({
        url: '/ajax/shownotifications',
        success: function(data){
            
        }
    })
}

function addfriend(user_id) {
    if(user_id>0) {
        $.ajax({
            url: '/ajax/addfriend/' + user_id + '/',
            success: function (data) {
                if(data.OK === 1) {
                    $('#friend_button').fadeOut('slow', function(){});
                }
            }
        });
    }else{
        alert('error')
    }
}


function checkNotifications(){
    $.ajax({
        url: '/ajax/checknotifications',
        success: function (data) {
            if(data.count > 0){
                $('#notifcount').text(data.count).toggleClass('bg-secondary bg-success');
            }
        }
    })
}