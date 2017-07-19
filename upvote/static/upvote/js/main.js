function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function vote(slug) {
    console.log(slug);
    $.ajax({
        url: "/ajax/vote/",
        type : "POST",
        data: {
            'slug': slug,
        },
        success: function (json) {
            var sticky_alert = $('.alert-sticky');
            sticky_alert.find('#alert-message').html(json.message);
            $('.alert-sticky').addClass('show');
            if (json.success) {
                var slug = '#' + json.slug;
                var count_container = $(slug).find('#vote-count');
                var count = +count_container.html() + 1;
                count_container.html(count);
            }
            setTimeout( function() {
                $('.alert-sticky').removeClass('show');
            }, 2000);
        }
    });
}