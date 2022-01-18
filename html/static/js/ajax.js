
function jointrip(id = 0){
    if(id>0) {
        $.ajax({
            url: '/ajax/jointrip/'+id+'/',
            success: function (data) {
                if(data.OK === 1){
                    $('#join_trip_button').fadeOut('slow', function(){});
                }
            }
        });
    }else{
        alert('error')
    }
}

function followgroup(id = 0){
    if(id > 0){
        $.ajax({
            url: '/ajax/followgroup/'+id+'/',
            success: function(data){
                if(data.OK === 1){
                    $('#follow_group').fadeOut('slow', function(){});
                }
            }
        })
    }
}

function followthread(id = 0){
    if(id > 0){
        $.ajax({
            url: '/ajax/followthread/'+id+'/',
            success: function(data){
                if(data.OK === 1){
                    $('#follow_thread').fadeOut('slow', function(){});
                }
            }
        })
    }
}

function showNotifications(){
    $.ajax({
        url: '/ajax/shownotifications',
        success: function(data){
            $('#notification_content').html(data);           
        }
    })
    
}

function addfriend(user_id) {
    if(user_id>0) {
        $.ajax({
            url: '/ajax/addfriend/' + user_id + '/',
            success: function (data) {
                if(data.OK === 1) {
                    $('#join_trip_button').fadeOut('slow', function(){});
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

function showSuggestions(){
    $.ajax({
        url: '/api/suggestions',
        success: function(data){
            $('#suggestion_content').html(data);           
        }
    })
    
}