$(document).ready(function(){
    
    $('#kv_main-slider-space').css("height","525px");
    
    var slides = $('.main-slides');
    console.log(slides);
    var i = 1;
       
    $("input[type='radio']").click(function(){
        console.log('clicked');
        var delay = 500;

        setTimeout(function() {
            i = ++i % slides.length;
            console.log(i);
            //i = ++i;
           // var k=i+1;
            var k = i;
            var stp='#step'+k;
            console.log(stp);
            var height=$(stp).height();
            console.log(height);
            $('#kv_main-slider-space').css("height",+height);
            
            // scroll to that index
            $('.kv_slider-wrapper').animate(
                {'left' : -(slides.eq(i).position().left)},
            525
            );
            
        }, delay);
      
    });
});