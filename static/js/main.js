$(document).ready(function(){

    $(document).on('click', '.drop-panel__button, .drop-arrow', function(){
        $(this).parents('.drop-panel').find('.drop-panel__panel').show();
    });

    $('html').click(function(){
        $('.drop-panel__panel').hide();
    });

    $(document).on('click touchstart', '.select-list li', function(){
        var value = $(this)[0].innerHTML;
        $(this).parents('.drop-panel').find('.select').val(value);
        $('.drop-panel__panel').hide();
    });

    $(document).on("click touchstart", ".header-menu__link", function(){
        var $cont = $( "#" + $(this).attr('contId') );
        $.scrollTo( $($cont).offset().top, 800);
    });

    $(document).on("click touchstart", ".user-actions__tab-title", function(){
        $('.user-actions__tab-title').removeClass('user-actions__tab-title--current');
        $(this).addClass('user-actions__tab-title--current');
        var $tab = $( "#" + $(this).attr('tab-button'));
        $('.user-actions__content').hide();
        $tab.show();
        if($('.user-actions__tab-title--current').attr('tab-button') == 'tab2'){
            $('.user-actions').addClass('user-actions--small-border');
        } else {
            $('.user-actions').removeClass('user-actions--small-border');
        };

        $('#auth-form').attr('action', $(this).attr('data-url'));
    });

    $(document).on("click touchstart", ".authorization-button", function(){
        $.scrollTo( $('#authorization').offset().top, 800);
    });

    $(document).on('click', '.read-more-rules-button', function(){
        var width = $('.rules-popup').width();
        var pos = ($(document).width() - width) / 2;
        $('.rules-popup').css('margin-left', pos + 'px').show();
        $('.popup-wrapper').show();
        $(window).scrollTop(0);
        $(".custom-scroll").mCustomScrollbar({});
    });

    $(document).on('click touchstart', '.close-button, .popup-wrapper', function(){
        $('.popup-wrapper, .rules-popup').hide();
        $(".custom-scroll").mCustomScrollbar("disable",true);
    });

    $(document).on('click touchstart', '.photo-list__item', function(){
        var width = $('.img-popup').width();
        var pos = ($(document).width() - width) / 2;
        $('.img-popup').css('margin-left', pos + 'px').show();
        $('.popup-wrapper, .img-popup').show();
        $(window).scrollTop(0);
    });

    $(document).on('click touchstart', '.popup-wrapper', function(){
        $('.popup-wrapper, .img-popup').hide();
    });

    $(document).on('click touchstart', '.drop-panel__panel, .drop-panel__button, .img-popup, .rules-popup', function(){
        event.stopPropagation();
    });

   $( '.parallax-layer' ).parallax();

});


