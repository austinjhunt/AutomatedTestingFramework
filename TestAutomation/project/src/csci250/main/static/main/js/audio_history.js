
var is_super_user;

$(document).ready(function()
{
        var curr_time_global = 0;

        var vid_1 = document.getElementById("audio_37");
        vid_1.ontimeupdate = function () {
            myFunction(vid_1)
        };

        var vid_2 = document.getElementById("audio_38");
        vid_2.ontimeupdate = function () {
            myFunction(vid_2)
        };

        var vid_3 = document.getElementById("audio_39");
        vid_3.ontimeupdate = function () {
            myFunction(vid_3)
        };

        function myFunction(curr_vid) {
            if (Math.round(curr_vid.currentTime) == curr_time_global)
                return;
            else
                curr_time_global = Math.round(curr_vid.currentTime);

            var d = new Date();
            var date_formatted =
                d.getFullYear() + "-" +
                ("00" + (d.getMonth() + 1)).slice(-2) + "-" +
                ("00" + d.getDate()).slice(-2) + " " +
                ("00" + d.getHours()).slice(-2) + ":" +
                ("00" + d.getMinutes()).slice(-2) + ":" +
                ("00" + d.getSeconds()).slice(-2);

            $.ajax(
                {
                    type: "POST",
                    data: {
                        btnType: 'update_audio_history',
                        audio_id: curr_vid.id,
                        action: 'currently_playing',
                        date_formatted: date_formatted,
                        time_in_seconds: Math.round(curr_vid.currentTime),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    success: function (data) {
                        // do nothing...
                    }
                });
        }
});