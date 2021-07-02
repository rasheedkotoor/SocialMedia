
//__________________________________________ csrf token ________________________________________________//
//------------------------------------------------------------------------------------------------------//
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

//_________________________________________adding new comment_________________________________________//
//------------------------------------------Studenthome.html------------------------------------------//
$(".cmnt_button").on("click", function(){
    var button = $(this);
    var post_id = $(this).attr('data-post_id');
    var comment = $('#cmnt-'+post_id).val();

    var data = {
        'csrfmiddlewaretoken' : csrftoken,
        'postid' : post_id,
        'comment' : comment,
    }
    $('#loader3').html('Please wait...');
    $.ajax({
        url: '/add_cmnt/',
        method: 'POST',
        data: data,
        success:function(data){
            if (data=='added'){
                $(".coment-area").fadeOut(800, function(){
                   location.reload();
                });
            }
            else if(data == 'error') {
                $(".comment_err").html("enter something")
            }
        }
    });
})

//__________________________________________add Like for post _________________________________________//
//------------------------------------------Studenthome.html-------------------------------------------//
$(".like_button").on("click", function(){
    var button = $(this);
    var post_id = $(this).attr('data-post_id');
    var data = {
        'csrfmiddlewaretoken' : csrftoken,
        'postid' : post_id,
    }
    $('#loader3').html('Please wait...');
    $.ajax({
        url: '/add_like/',
        method: 'POST',
        data: data,
        success:function(data){
            $(button).fadeOut(800, function(){
                button.html(data).fadeIn().delay(2000);

            });
        }
    });
})

//__________________________________________add friend req/cancel   __________________________________________//
//------------------------------------------Studenthome.html-------------------------------------------//
$(".friend_req").on("click", function(){
    var button = $(this);
    var value = $(this).text();
    var to_id = $(this).attr('data-user_id');
    var data = {
        'csrfmiddlewaretoken' : csrftoken,
        'to_id' : to_id,
        'value' : value,
    }
    $('#loader3').html('Please wait...');
    $.ajax({
        url: '/accounts/add_friend/',
        method: 'POST',
        data: data,
        success:function(data){
            $(button).fadeOut(800, function(){
                button.html(data).fadeIn().delay(2000);

            });
        },
    });
});

//__________________________________________profile updating    __________________________________________//
//------------------------------------------student > profile.html-------------------------------------------//
$(document).ready(function(){
    $(".profile_edit_fn").on("click", function(){
        var f_name = $(this).next()
        var l_name = $(this).next().next()
        f_name.removeAttr('hidden');
        l_name.removeAttr('hidden');
        var user_id = $(this).attr('data-user_id');
        $(".prof_save_btn").on("click", function(){
            var first_name = f_name.children().val();
            var last_name = l_name.children().val();
            var data = {
                'csrfmiddlewaretoken' : csrftoken,
                'first_name' : first_name,
                'last_name' : last_name,
                'user_id' : user_id,
            }
            $.ajax({
                url: '/edit_fullname/',
                method: 'POST',
                data: data,
                success:function(data){
                    location.reload();
                },
            });
        });
    });
});

//__________________________________________profile updating    __________________________________________//
//------------------------------------------student > profile.html-------------------------------------------//
$(document).ready(function(){
    $(".profile_edit").on("click", function(){
        var input_field = $(this).next()
        var user_id = $(this).attr('data-user_id');
        var differ = $(this).attr('data-name');
        input_field.removeAttr('hidden');
        $(".prof_save_btn").on("click", function(){
            var editing_value = input_field.children().val();
            var data = {
                'csrfmiddlewaretoken' : csrftoken,
                'editing_value' : editing_value,
                'user_id' : user_id,
                'differ' : differ,
            }
            $.ajax({
                url: '/edit_profile_data/',
                method: 'POST',
                data: data,
                success:function(data){
                    location.reload();
                },
            });
        });
    });
});

//__________________________________ enter phone number for otp login    _____________________________________//
//----------------------------------------- acount > otplogin.html -------------------------------------------//
$('#loginbtn').click(function(){
    var phone_number = $('#phone_number').val();
    var data = {
        'csrfmiddlewaretoken' : csrftoken,
        'phone_number' : phone_number,
    }
    if (phone_number === "") {
        $('#errmsg2').html("Enter your Phone number")
    }
    else {
        $.ajax({
            url:'/accounts/otp_login/',
            method:'POST',
            data: data,
            dataType:'json',
            success:function(data){
                if (data=='true'){
                    window.location.replace('/accounts/enter_otp/')
                }
                else if(data == 'upw') {
                    $("#errmsg2").html("Phone number is wrong")
                }
                else if(data == 'blck') {
                    $("#errmsg2").html("Your account is blocked. Contact your Admin")
                }
                else if(data == 'nouser') {
                    $("#errmsg2").html("Mobile number does not exists")
                }
            }
        })
    }
})

//__________________________________ enter otp for  login    _____________________________________//
//_________________________________ _ accounts enterotp     _____________________________________//

$('#loginbtn2').click(function(){
        var otp = $('#otp').val();
        var data = {
        'csrfmiddlewaretoken' : csrftoken,
        'otp' : otp,
        }
    if (otp === "") {
        $('#errmsg2').html("Enter your otp")
    }
    else {
        $.ajax({
            url:'',
            method:'POST',
            data: data,
            dataType:'json',
            success:function(data){
                if (data=='true'){
                    window.location.replace('/')
                }
                else if(data == 'und') {
                    $("#errmsg2").html("otp dose not matching")
                }
            }
        })
    }
})

//__________________________________________ add page admin     __________________________________________//
//------------------------------------------ union > unoionlist.html-------------------------------------------//
$(document).ready(function(){
    $(".add_admin_btn").on("click", function(){
        var page = $(this).attr('data-union');
        var admin_select = $(this).next()
        admin_select.removeAttr('hidden');
        $(".admin_add_btn").on("click", function(){
            var admin = admin_select.children().val();
            console.log(page, admin, "========================")
            var data = {
                'csrfmiddlewaretoken' : csrftoken,
                'page' : page,
                'admin' : admin,
            }
            $.ajax({
                url: '/adminn/add_page_admin/',
                method: 'POST',
                data: data,
                success:function(data){
                    if (data == 'true') {
                        window.alert('the user is added as admin');
                        location.reload()
                    }
                    else if (data == "false") {
                        window.alert("User is not found");
                    }
                },
            });
        });
    });
});

//__________________________________________ select_my_union     __________________________________________//
//------------------------------------------ students > studenthome.html-------------------------------------------//
$(document).ready(function(){
    $(".select_my_union").on("click", function(){
        admin_select = $(this).next()
        admin_select.removeAttr('hidden');
        $("#select_union").on("click", function(){
            var union = admin_select.children().children().val();
            var data = {
                'csrfmiddlewaretoken' : csrftoken,
                'union' : union,
            }
            $.ajax({
                url: '/select_my_union/',
                method: 'POST',
                data: data,
                success:function(data){
                    if (data == "true") {
                        window.alert('do you want to send request your union');
                        location.reload()
                    }
                    else if (data == "false") {
                        window.alert('You already send request to the Union');
                        location.reload()
                    }
                },
            });
        });
    });
});

//__________________________________________add join req req/cancel   __________________________________________//
//------------------------------------------Studenthome.html-------------------------------------------//
$(".join_req").on("click", function(){
    if (confirm("Are you sure?")) {
        var button = $(this);
        var value = $(this).text();
        var union_id = $(this).attr('data-union_id');
        var user_id = $(this).attr('data-user_id');
        var data = {
            'csrfmiddlewaretoken' : csrftoken,
            'union_id' : union_id,
            'user_id' : user_id,
            'value' : value,
        }
        $.ajax({
            url: '/union/join_req/',
            method: 'POST',
            data: data,
            success:function(data){
                location.reload()
            },
        });
    }
    return false;
});

//__________________________________________  union detail update  __________________________________________//
//------------------------------------------my_union.html          -----------------------------------------//
$(document).ready(function(){
    $(".union_profile_edit").on("click", function(){
        var input_field = $(this).next()
        var union_id = $(this).attr('data-union_id');
        var differ = $(this).attr('data-name');
        input_field.removeAttr('hidden');
        $(".union_prof_save_btn").on("click", function(){
            var editing_value = input_field.children().val();
            var data = {
                'csrfmiddlewaretoken' : csrftoken,
                'editing_value' : editing_value,
                'union_id' : union_id,
                'differ' : differ,
            }
            $.ajax({
                url: '/union/edit_profile_data/',
                method: 'POST',
                data: data,
                success:function(data){
                    location.reload();
                },
            });
        });
    });
});


//__________________________________________    __________________________________________//
//------------------------------------------.demo -----------------------------------------//

//$("#remove_mem").on("click", function(){
//    var button = $(this);
//    var user_id = $(this).attr('data-user_id');
//
//    var data = {
//        'csrfmiddlewaretoken' : csrftoken,
//        'user_id' : user_id,
//    }
//    $.ajax({
//        url: '/union/remove_mem/',
//        method: 'POST',
//        data: data,
//        success:function(data){
//            location.reload()
//        },
//    })
//});