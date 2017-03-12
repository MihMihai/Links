$(window).load(function () {
	
	$("#header").vegas({
		slides: [
			{ src: "img/slider/1.jpg" },
			{ src: "img/slider/1.jpg" },
			{ src: "img/slider/1.jpg" },
			{ src: "img/slider/1.jpg" },
			{ src: "img/slider/1.jpg" },
			{ src: "img/slider/1.jpg" },
			{ src: "img/slider/1.jpg" }
		],
        transition: 'fade',
        preloadImage: true,
        timer: true,
        shuffle: true,
        delay: 5000,
        animation: 'kenburns',
        cover: true
	});
	
	$("#video").vegas({
		slides: [
			{   src: 'videos/Productive-Morning.jpg' },
			{
			  video: {
                src: [
                    'videos/Productive-Morning.mp4',
                    'videos/Productive-Morning.webm',
                    'videos/Productive-Morning.ogv'
                ],
                loop: true,
                mute: true
               },
        delay: 16000,
		 }
		],
        cover: true
	});	
	
});

$(document).ready(function() {
						 
	// navigation click actions	
	// jQuery for page scrolling feature - requires jQuery Easing plugin

    $('.scroll-link').bind('click', function(event) {
        var $anchor = $(this);
	    var offSet = 85;
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top - offSet
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
	
						   
	if ($(window).scrollTop()===0){
		$('.navbar').removeClass('scrolled');
	}
	else{
		$('.navbar').addClass('scrolled');    
	}

	$(window).scroll(function(){
		if ($(window).scrollTop()===0){
			$('.navbar').removeClass('scrolled');
		}
		else{
			$('.navbar').addClass('scrolled');    
		}
	});
	
	$(window).scroll(function(){
		if ($(this).scrollTop() > 250) {
			$('#scrollup').fadeIn(300);
		} else {
			$('#scrollup').fadeOut(300);
		}
	});

	$('#scrollup').click(function(){
		$("html, body").animate({ scrollTop: 0 }, 1000);
		return false;
	});
	
	$('.animations').waypoint(function(){
		$(this).addClass('in');
	},{offset:function(){
			var h = $(window).height();
			var elemh = $(this).outerHeight();
			if ( elemh > h*0.3){
				return h*0.7;
			}else{
				return h - elemh;
			}
		}
	});



});

