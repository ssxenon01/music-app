$(document).ready(function () {

    var myPlaylist = new jPlayerPlaylist({
        jPlayer: "#jplayer_N",
        cssSelectorAncestor: "#jp_container_N"
    }, [
        /*{
         title: "Love Me Like You Do",
         artist: "Ellie",
         mp3: "http://stream.sons.mn:6055/COHC/amlst:f5e8385f-5f15-4de7-ae05-596d7564728c/playlist.m3u8",
         //mp3: "https://drive.google.com/uc?&id=0B6PXUZA-KpFoY3hQMzM4eDkzZHM",
         poster: "/p/img/m0.jpg"
         }*/
    ], {
        playlistOptions: {
            autoPlay: true
        },
        swfPath: "/p/ext/jplayer/dist/jplayer/jquery.jplayer.swf",
        supplied: "webmv, ogv, m4v, oga, mp3, mpeg",
        smoothPlayBar: true,
        keyEnabled: true,
        audioFullScreen: false
    });

    $(document).on($.jPlayer.event.pause, myPlaylist.cssSelector.jPlayer, function () {
        $('.musicbar').removeClass('animate');
        var sel = $('.jp-play-me');
        sel.removeClass('active');
        sel.parent('li').removeClass('active');
    });

    $(document).on($.jPlayer.event.play, myPlaylist.cssSelector.jPlayer, function () {
        $('.musicbar').addClass('animate');
    });

    $(document).on('click', '.jp-play-me', function (e) {
        e && e.preventDefault();
        var $this = $(e.target);
        if (!$this.is('a')) $this = $this.closest('a');
        var sel = $('.jp-play-me');
        sel.not($this).removeClass('active');
        sel.parent('li').not($this.parent('li')).removeClass('active');

        $this.toggleClass('active');
        $this.parent('li').toggleClass('active');
        if (!$this.hasClass('active')) {
            myPlaylist.pause();
        } else {
            var i = Math.floor(Math.random() * (1 + 7 - 1));
            myPlaylist.play(i);
        }
    });
    var prevState;
    $(document).on('click', 'a[data-id]', function (e) {
        e.preventDefault();
        var link = $(this),
            id = link.attr('data-id'),
            title = link.attr('data-title'),
            artist = link.attr('data-artist');
        myPlaylist.setPlaylist([{
            title: title,
            artist: artist,
            mp3: 'https://drive.google.com/uc?&id=' + id
        }]);
        if (prevState)
            prevState.removeClass('active');
        prevState = link.closest('.item-overlay');
        prevState.addClass('active');
        myPlaylist.play();


    });

});
if (window.console) {
    window.console.info('Юм хайж байна уу ?');
}