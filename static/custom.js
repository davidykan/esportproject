$(document).ready(function() {
    $('.container.streams .thumbnail img').css("height",.5625*$('.thumbnail img').width());
    $('.container.games .thumbnail img').css("height",1.397*$('.thumbnail img').width());
    $(window).resize(function(){
        $('.container.streams .thumbnail img').css("height",.5625*$('.thumbnail img').width());
        $('.container.games .thumbnail img').css("height",1.397*$('.thumbnail img').width());
    });


});