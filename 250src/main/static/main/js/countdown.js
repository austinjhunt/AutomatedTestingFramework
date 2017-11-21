/*
Item Name : Circular Countdown jQuery Plugin
Item URI : http://codecanyon.net/item/circular-countdown-jquery-plugin/3761921
Author URI : http://codecanyon.net/user/Pixelworkshop/
Version : 1.21
*/


(function ($) {


    var settings = {

        strokeDaysBackgroundColor:'rgba(101,127,129,0.06)',
        strokeDaysColor:'rgba(101,127,129,0.3)',
        strokeHoursBackgroundColor:'rgba(101,127,129,0.06)',
        strokeHoursColor:'rgba(101,127,129,0.3)',
        strokeMinutesBackgroundColor:'rgba(101,127,129,0.06)',
        strokeMinutesColor:'rgba(101,127,129,0.3)',
        strokeSecondsBackgroundColor:'rgba(101,127,129,0.06)',
        strokeSecondsColor:'rgba(101,127,129,0.3)',
        // Stroke width can be set to a number equal to 10% of the total width 
        // of the countdown to get full circles instead of strokes.
        // If your countdown has a width of 800px, set the strokeWidth to 80
        // to get full circles. Use 70 if your countdown has a width of 700px, etc.
        strokeWidth:17,
        strokeBackgroundWidth:17,
        countdownEasing:'easeOutBounce',
        countdownTickSpeed:'slow',
        backgroundShadowColor: 'rgba(0,0,0,0.2)',
        backgroundShadowBlur: 0,
        strokeShadowColor: 'rgba(0,0,0,0.2)',
        strokeShadowBlur: 0

    };


    var methods = {
        
        init:function (options) {
            
            settings = $.extend(1, settings, options);

            return this.each(function () {

				countdownTimer();
	            countdownArcs();

            }); // End each

        },

        update:function (options) {
            settings = $.extend(1, settings, options);
        }
    };


    $.fn.circularCountdown = function (method) {

        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('No found method ' + method);
        }

    };


	function countdownArcs() { 

		var circularCountdown = $('#circular_countdown_days'),
			countdownElementRadius = ($('#countdown_timer li').width() - settings.strokeWidth) / 2,
			countdownElementWidth = countdownElementRadius * 2 + settings.strokeWidth,
			countdownXPosition = countdownElementWidth / 2,
			countdownYPosition = countdownElementWidth / 2;


			$("#circular_countdown_days")
				.drawArc({
					layer: true,
					name: "days_bg",
					strokeStyle: settings.strokeDaysBackgroundColor,
					strokeWidth: settings.strokeBackgroundWidth,
					radius: countdownElementRadius,
					shadowColor: settings.backgroundShadowColor,
					shadowBlur: settings.backgroundShadowBlur,
					x: countdownXPosition, 
					y: countdownYPosition
				})
				.drawArc({
					layer: true,
					name: "days",
					strokeStyle: settings.strokeDaysColor,
					strokeWidth: settings.strokeWidth,
					radius: countdownElementRadius,
					shadowColor: settings.strokeShadowColor,
					shadowBlur: settings.strokeShadowBlur,
					x: countdownXPosition, 
					y: countdownYPosition
				})
			$("#circular_countdown_hours")
				.drawArc({
					layer: true,
					name: "hours_bg",
					strokeStyle: settings.strokeHoursBackgroundColor,
					strokeWidth: settings.strokeBackgroundWidth,
					radius: countdownElementRadius,
					shadowColor: settings.backgroundShadowColor,
					shadowBlur: settings.backgroundShadowBlur,
					x: countdownXPosition, 
					y: countdownYPosition
				})
				.drawArc({
					layer: true,
					name: "hours",
					strokeStyle: settings.strokeHoursColor,
					strokeWidth: settings.strokeWidth,
					radius: countdownElementRadius,
					shadowColor: settings.strokeShadowColor,
					shadowBlur: settings.strokeShadowBlur,
					x: countdownXPosition, 
					y: countdownYPosition
				})
			$("#circular_countdown_minutes")
				.drawArc({
					layer: true,
					name: "minutes_bg",
					strokeStyle: settings.strokeMinutesBackgroundColor,
					strokeWidth: settings.strokeBackgroundWidth,
					radius: countdownElementRadius,
					shadowColor: settings.backgroundShadowColor,
					shadowBlur: settings.backgroundShadowBlur,
					x: countdownXPosition, 
					y: countdownYPosition
				})
				.drawArc({
					layer: true,
					name: "minutes",
					strokeStyle: settings.strokeMinutesColor,
					strokeWidth: settings.strokeWidth,
					radius: countdownElementRadius,
					shadowColor: settings.strokeShadowColor,
					shadowBlur: settings.strokeShadowBlur,
					x: countdownXPosition, 
					y: countdownYPosition
				})
			$("#circular_countdown_seconds")
				.drawArc({
					layer: true,
					name: "seconds_bg",
					strokeStyle: settings.strokeSecondsBackgroundColor,
					strokeWidth: settings.strokeBackgroundWidth,
					radius: countdownElementRadius,
					shadowColor: settings.backgroundShadowColor,
					shadowBlur: settings.backgroundShadowBlur,
					x: countdownXPosition, 
					y: countdownYPosition
				})
				.drawArc({
					layer: true,
					name: "seconds",
					strokeStyle: settings.strokeSecondsColor,
					strokeWidth: settings.strokeWidth,
					radius: countdownElementRadius,
					shadowColor: settings.strokeShadowColor,
					shadowBlur: settings.strokeShadowBlur,
					x: countdownXPosition, 
					y: countdownYPosition
				})

				.drawLayers()

	}


	function countdownAnimation()
	{
		$("#circular_countdown_days")
			.animateLayer("days", {
				end:$('#countdown_timer ul li.days em').text() * 90 // (90 is 360/4) 4 days
			}, settings.countdownTickSpeed, settings.countdownEasing)
		$("#circular_countdown_hours")
			.animateLayer("hours", {
				end:$('#countdown_timer ul li.hours em').text() * 15
			}, settings.countdownTickSpeed, settings.countdownEasing)
		$("#circular_countdown_minutes")
			.animateLayer("minutes", {
				end:$('#countdown_timer ul li.minutes em').text() * 6
			}, settings.countdownTickSpeed, settings.countdownEasing)
		$("#circular_countdown_seconds")
			.animateLayer("seconds", {
				end:$('#countdown_timer ul li.seconds em').text() * 6
			}, settings.countdownTickSpeed, settings.countdownEasing)
					
	}


	function countdownTimer()
	{
		console.log('de hello in countdown');


		$('#countdown_timer').countdown({

			// new Date(year, mth, day, hr, min, sec) - Date / Time to count down to 

			// How to format the date :
			// Year,
			// Month (january = 0, february = 1; etc.),
			// Day of the month (2 for the 2nd, 3 for the 3rd, etc.),
			// Hour of the day (using the 24-hour system) 
			// Optionnally you can add minutes and seconds separated by commas

			// Examples : 
			// new Date(2014, 2, 15, 18) will count until the 15th of March 2014 at 6 PM.
			// new Date(2013, 6, 3, 8) will count until the 3rd of July 2013 at 8 AM.

			//until: new Date(nextReleaseDate.getFullYear(), nextReleaseDate.getMonth(), nextReleaseDate.getDate(), nextReleaseDate.getHours(), nextReleaseDate.getMinutes()+1),
			until: new Date(2016, 7, 22, 9, 0),
			timezone: null,
			format: 'DHMS',
			layout: 
				'<div class="row"><ul>' +
				'{d<}<div class="col-lg-3 col-md-3 col-sm-6 col-xs-12"><li class="days"><em>{dn}</em> {dl}</li></div>{d>}' +
				'{h<}<div class="col-lg-3 col-md-3 col-sm-6 col-xs-12"><li class="hours"><em>{hn}</em> {hl}</li></div>{h>}' +
				'{m<}<div class="col-lg-3 col-md-3 col-sm-6 col-xs-12"><li class="minutes"><em>{mn}</em> {ml}</li></div>{m>}' +
				'{s<}<div class="col-lg-3 col-md-3 col-sm-6 col-xs-12"><li class="seconds"><em>{sn}</em> {sl}</li></div>{s>}' +
				'</ul></div>',

			onTick: function() {
				countdownAnimation();
			}

		});
					
	}


})(jQuery);