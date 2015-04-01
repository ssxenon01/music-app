/* Modernizr 2.6.2 (Custom Build) | MIT & BSD
 * Build: http://modernizr.com/download/#-touch-cssclasses-teststyles-prefixes
 */
;
window.Modernizr = function (a, b, c) {
    function w(a) {
        j.cssText = a
    }

    function x(a, b) {
        return w(m.join(a + ";") + (b || ""))
    }

    function y(a, b) {
        return typeof a === b
    }

    function z(a, b) {
        return !!~("" + a).indexOf(b)
    }

    function A(a, b, d) {
        for (var e in a) {
            var f = b[a[e]];
            if (f !== c)return d === !1 ? a[e] : y(f, "function") ? f.bind(d || b) : f
        }
        return !1
    }

    var d = "2.6.2", e = {}, f = !0, g = b.documentElement, h = "modernizr", i = b.createElement(h), j = i.style, k, l = {}.toString, m = " -webkit- -moz- -o- -ms- ".split(" "), n = {}, o = {}, p = {}, q = [], r = q.slice, s, t = function (a, c, d, e) {
        var f, i, j, k, l = b.createElement("div"), m = b.body, n = m || b.createElement("body");
        if (parseInt(d, 10))while (d--)j = b.createElement("div"), j.id = e ? e[d] : h + (d + 1), l.appendChild(j);
        return f = ["&#173;", '<style id="s', h, '">', a, "</style>"].join(""), l.id = h, (m ? l : n).innerHTML += f, n.appendChild(l), m || (n.style.background = "", n.style.overflow = "hidden", k = g.style.overflow, g.style.overflow = "hidden", g.appendChild(n)), i = c(l, a), m ? l.parentNode.removeChild(l) : (n.parentNode.removeChild(n), g.style.overflow = k), !!i
    }, u = {}.hasOwnProperty, v;
    !y(u, "undefined") && !y(u.call, "undefined") ? v = function (a, b) {
        return u.call(a, b)
    } : v = function (a, b) {
        return b in a && y(a.constructor.prototype[b], "undefined")
    }, Function.prototype.bind || (Function.prototype.bind = function (b) {
        var c = this;
        if (typeof c != "function")throw new TypeError;
        var d = r.call(arguments, 1), e = function () {
            if (this instanceof e) {
                var a = function () {
                };
                a.prototype = c.prototype;
                var f = new a, g = c.apply(f, d.concat(r.call(arguments)));
                return Object(g) === g ? g : f
            }
            return c.apply(b, d.concat(r.call(arguments)))
        };
        return e
    }), n.touch = function () {
        var c;
        return "ontouchstart"in a || a.DocumentTouch && b instanceof DocumentTouch ? c = !0 : t(["@media (", m.join("touch-enabled),("), h, ")", "{#modernizr{top:9px;position:absolute}}"].join(""), function (a) {
            c = a.offsetTop === 9
        }), c
    };
    for (var B in n)v(n, B) && (s = B.toLowerCase(), e[s] = n[B](), q.push((e[s] ? "" : "no-") + s));
    return e.addTest = function (a, b) {
        if (typeof a == "object")for (var d in a)v(a, d) && e.addTest(d, a[d]); else {
            a = a.toLowerCase();
            if (e[a] !== c)return e;
            b = typeof b == "function" ? b() : b, typeof f != "undefined" && f && (g.className += " " + (b ? "" : "no-") + a), e[a] = b
        }
        return e
    }, w(""), i = k = null, e._version = d, e._prefixes = m, e.testStyles = t, g.className = g.className.replace(/(^|\s)no-js(\s|$)/, "$1$2") + (f ? " js " + q.join(" ") : ""), e
}(this, this.document);
Modernizr.addTest('android', function () {
    return !!navigator.userAgent.match(/Android/i)
});
Modernizr.addTest('chrome', function () {
    return !!navigator.userAgent.match(/Chrome/i)
});
Modernizr.addTest('firefox', function () {
    return !!navigator.userAgent.match(/Firefox/i)
});
Modernizr.addTest('iemobile', function () {
    return !!navigator.userAgent.match(/IEMobile/i)
});
Modernizr.addTest('ie', function () {
    return !!navigator.userAgent.match(/MSIE/i)
});
Modernizr.addTest('ie8', function () {
    return !!navigator.userAgent.match(/MSIE 8/i)
});
Modernizr.addTest('ie10', function () {
    return !!navigator.userAgent.match(/MSIE 10/i)
});
Modernizr.addTest('ie11', function () {
    return !!navigator.userAgent.match(/Trident.*rv:11\./)
});
Modernizr.addTest('ios', function () {
    return !!navigator.userAgent.match(/iPhone|iPad|iPod/i)
});
Modernizr.addTest('ios7 ipad', function () {
    return !!navigator.userAgent.match(/iPad;.*CPU.*OS 7_\d/i)
});


var initTile = function(){

    var TILE_IDS = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
        15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29
    ];
    var rows_lg = [
        " A A B . . . ",
        " A A B . . C ",
        " . . . . D C ",
        " E E F F D . ",
        " . . F F . . ",
        " . G G . . . "
    ];
    var rows_sm = [
        " A A B . . ",
        " A A B . . ",
        " . C . . . ",
        " . C D E E ",
        " F F D . . ",
        " F F . . . ",
        " . G G . . ",
        " . . . . . "
    ];
    var rows_xs = [
        " A A B ",
        " A A B ",
        " . . . ",
        " . . C ",
        " . . C ",
        " . . D ",
        " E E D ",
        " F F . ",
        " F F . ",
        " . . . ",
        " . G G ",
        " . . . "
    ];

    var el = $('#masonry'),
        grid = new Tiles.Grid(el);
    grid.cellPadding = 0;
    grid.animationDuration = 0;

    grid.resizeColumns = function () {
        return this.template.numCols;
    };
    grid.numCols = function () {
        return this.template.numRows;
    };

    grid.createTile = function (tileId) {
        var tile = new Tiles.Tile(tileId);
        tile.$el.attr('tile-id', tileId).addClass('pos-abt').append($(" > .item:first", el));
        return tile;
    };

    // get the rows json for different screen
    var $window = $(window);
    var getRows = function () {
        var $rows;
        $window.width() < 768 && ($rows = rows_xs);
        $window.width() >= 768 && ($rows = rows_sm);
        $window.width() >= 992 && ($rows = rows_lg);
        return $rows;
    };

    grid.template = Tiles.Template.fromJSON(getRows());
    grid.isDirty = true;
    grid.resize();

    var ids = TILE_IDS.slice(0, grid.template.rects.length);
    grid.updateTiles(ids);
    grid.redraw(true);

    // set height on mobile
    var setHeight = function () {
        el.height('auto');
        $window.width() < 768 && el.height(grid.cellSize * grid.template.numRows);
    };
    setHeight();

    // resize the window
    var $resize, $width = $window.width();
    $window.resize(function () {
        if ($width !== $window.width()) {
            clearTimeout($resize);
            $resize = setTimeout(function () {
                grid.template = Tiles.Template.fromJSON(getRows());
                grid.resize();
                grid.redraw(true);
                setHeight();
                $width = $window.width();
            }, 200);
        }
    });
};

// data-shift api 
+function ($) {
    "use strict";

    /* SHIFT CLASS DEFINITION
     * ====================== */
    var Shift = function (element) {
        this.$element = $(element);
        this.$prev = this.$element.prev();
        !this.$prev.length && (this.$parent = this.$element.parent())
    };

    Shift.prototype = {
        constructor: Shift

        , init: function () {
            var $el = this.$element
                , method = $el.data()['toggle'].split(':')[1]
                , $target = $el.data('target');
            $el.hasClass('in') || $el[method]($target).addClass('in')
        }
        , reset: function () {
            this.$parent && this.$parent['prepend'](this.$element);
            !this.$parent && this.$element['insertAfter'](this.$prev);
            this.$element.removeClass('in')
        }
    };

    /* SHIFT PLUGIN DEFINITION
     * ======================= */

    $.fn.shift = function (option) {
        return this.each(function () {
            var $this = $(this)
                , data = $this.data('shift');
            if (!data) $this.data('shift', (data = new Shift(this)));
            if (typeof option == 'string') data[option]()
        });
    };

    $.fn.shift.Constructor = Shift
}(jQuery);


// data-bjax api 
+function ($) {
    "use strict";
    initTile();
    var Bjax = function (element, options) {
        this.options = options;
        this.$element = $(this.options.target || 'html');
        this.start()
    };

    Bjax.DEFAULTS = {
        backdrop: true
        , url: ''
    };

    Bjax.prototype.start = function (popstate) {
        var that = this;
        this.backdrop();
        $.ajax(this.options.url).done(function (r) {
            that.$content = r;
            that.complete(popstate);
        });
    };

    Bjax.prototype.complete = function (popstate) {
        if(!popstate)
            if (this.$element.is('html') || (this.options.replace)) {
                try {
                    window.history.pushState({}, '', this.options.url);
                } catch (e) {
                    window.location.replace(this.options.url)
                }
            }

        this.updateBar(100);
    };

    Bjax.prototype.backdrop = function () {
        this.$element.css('position', 'relative');
        this.$backdrop = $('<div class="backdrop fade bg-white"></div>')
            .appendTo(this.$element);
        if (!this.options.backdrop) this.$backdrop.css('height', '2');
        //this.$backdrop[0].offsetWidth; // force reflow
        this.$backdrop.addClass('in');

        this.$bar = $('<div class="bar b-t b-2x b-info"></div>')
            .width(0)
            .appendTo(this.$backdrop);
    };

    Bjax.prototype.update = function () {
        this.$element.css('position', '');
        if (!this.$element.is('html')) {
            //if (this.options.el) {
            //    this.$content = $(this.$content).find(this.options.el);
            //}
            this.$element.html(this.$content);
            if(this.options.url == '/moods'){
                initTile();
            }
        }
        if (this.$element.is('html')) {
            if ($('.ie').length) {
                location.reload();
                return;
            }
            document.open();
            document.write(this.$content);
            document.close();
        }
    };

    Bjax.prototype.updateBar = function (per) {
        var that = this;
        this.$bar.stop().animate({
            width: per + '%'
        }, 500, 'linear', function () {
            if (per == 100) that.update();
        });
    };

    Bjax.prototype.enable = function (e) {
        var link = e.currentTarget;
        if (location.protocol !== link.protocol || location.hostname !== link.hostname)
            return false;
        if (link.hash && link.href.replace(link.hash, '') ===
            location.href.replace(location.hash, ''))
            return false;
        if (link.href === location.href + '#' || link.href === location.href)
            return false;
        return link.protocol.indexOf('http') != -1;

    };
    var datas = {};
    var current;
    $.fn.bjax = function (option) {
        return this.each(function () {
            var $this = $(this);
            var data = datas[option.url];
            var options = $.extend({}, Bjax.DEFAULTS, $this.data(), typeof option == 'object' && option);
            if (!data)
                datas[option.url] = data = new Bjax(this, options);
            else
                data['start']();
            if (typeof option == 'string') data[option]()
        })
    };

    $.fn.bjax.Constructor = Bjax;

    $(window).on("popstate", function (e) {
        var fn = datas[document.location.pathname];
        if(fn){
            current = document.location.pathname;
            fn['start'](true);
        }
        e.preventDefault();
    });

    $(document).on('click.app.bjax.data-api', '[data-bjax], .nav-primary a, a.db', function (e) {
        if (!Bjax.prototype.enable(e)) return false;
        var navUrl = $(this).attr('href') || $(this).attr('data-url');
        if(current == navUrl) return false;
        current = navUrl;
        $(this).bjax({replace:true,el:'#content-area',target:'#content-area',url: navUrl});
        return false;
    });
}(jQuery);

Date.now = Date.now || function () {
    return +new Date;
};

+function ($) {

    $(function () {

        // toogle fullscreen
        $(document).on('click', "[data-toggle=fullscreen]", function (e) {
            e.preventDefault();
            if (screenfull.enabled) {
                screenfull.request();
            }
        });

        // placeholder
        $('input[placeholder], textarea[placeholder]').placeholder();

        // popover
        $("[data-toggle=popover]").popover();
        $(document).on('click', '.popover-title .close', function (e) {
            var $target = $(e.target), $popover = $target.closest('.popover').prev();
            $popover && $popover.popover('hide');
        });

        // ajax modal
        $(document).on('click', '[data-toggle="ajaxModal"]',
            function (e) {
                $('#ajaxModal').remove();
                e.preventDefault();
                var $this = $(this)
                    , $remote = $this.data('remote') || $this.attr('href')
                    , $modal = $('<div class="modal fade" id="ajaxModal"><div class="modal-body"></div></div>');
                $('body').append($modal);
                $modal.modal();
                $modal.load($remote);
            }
        );

        // dropdown menu
        $.fn.dropdown.Constructor.prototype.change = function (e) {
            e.preventDefault();
            var $item = $(e.target), $select, $checked = false, $menu, $label;
            !$item.is('a') && ($item = $item.closest('a'));
            $menu = $item.closest('.dropdown-menu');
            $label = $menu.parent().find('.dropdown-label');
            var $labelHolder = $label.text();
            $select = $item.parent().find('input');
            $checked = $select.is(':checked');
            if ($select.is(':disabled')) return;
            if ($select.attr('type') == 'radio' && $checked) return;
            if ($select.attr('type') == 'radio') $menu.find('li').removeClass('active');
            $item.parent().removeClass('active');
            !$checked && $item.parent().addClass('active');
            $select.prop("checked", !$select.prop("checked"));

            var $items = $menu.find('li > input:checked');
            var $text;
            if ($items.length) {
                $text = [];
                $items.each(function () {
                    var $str = $(this).parent().text();
                    $str && $text.push($.trim($str));
                });

                $text = $text.length < 4 ? $text.join(', ') : $text.length + ' selected';
                $label.html($text);
            } else {
                $label.html($label.data('placeholder'));
            }
        };
        $(document).on('click.dropdown-menu', '.dropdown-select > li > a', $.fn.dropdown.Constructor.prototype.change);

        // tooltip
        $("[data-toggle=tooltip]").tooltip();

        // class
        $(document).on('click', '[data-toggle^="class"]', function (e) {
            e && e.preventDefault();
            var $this = $(e.target), $class, $target, $tmp, $classes, $targets;
            !$this.data('toggle') && ($this = $this.closest('[data-toggle^="class"]'));
            $class = $this.data()['toggle'];
            $target = $this.data('target') || $this.attr('href');
            $class && ($tmp = $class.split(':')[1]) && ($classes = $tmp.split(','));
            $target && ($targets = $target.split(','));
            $classes && $classes.length && $.each($targets, function (index, value) {
                if ($classes[index].indexOf('*') !== -1) {
                    var patt = new RegExp('\\s' +
                    $classes[index].
                        replace(/\*/g, '[A-Za-z0-9-_]+').
                        split(' ').
                        join('\\s|\\s') +
                    '\\s', 'g');
                    $($this).each(function (i, it) {
                        var cn = ' ' + it.className + ' ';
                        while (patt.test(cn)) {
                            cn = cn.replace(patt, ' ');
                        }
                        it.className = $.trim(cn);
                    });
                }
                ($targets[index] != '#') && $($targets[index]).toggleClass($classes[index]) || $this.toggleClass($classes[index]);
            });
            $this.toggleClass('active');
        });

        // panel toggle
        $(document).on('click', '.panel-toggle', function (e) {
            e && e.preventDefault();
            var $this = $(e.target), $class = 'collapse', $target;
            if (!$this.is('a')) $this = $this.closest('a');
            $target = $this.closest('.panel');
            $target.find('.panel-body').toggleClass($class);
            $this.toggleClass('active');
        });

        // carousel
        $('.carousel.auto').carousel();

        // button loading
        $(document).on('click.button.data-api', '[data-loading-text]', function (e) {
            var $this = $(e.target);
            $this.is('i') && ($this = $this.parent());
            $this.button('loading');
        });

        var $window = $(window);
        // mobile
        var mobile = function (option) {
            var shift = $('[data-toggle^="shift"]');
            if (option == 'reset') {
                shift.shift('reset');
                return true;
            }
            shift.shift('init');
            return true;
        };
        // unmobile
        $window.width() < 768 && mobile();
        // resize
        var $resize, $width = $window.width();
        $window.resize(function () {
            if ($width !== $window.width()) {
                clearTimeout($resize);
                $resize = setTimeout(function () {
                    setHeight();
                    $window.width() < 768 && mobile();
                    $window.width() >= 768 && mobile('reset') && fixVbox();
                    $width = $window.width();
                }, 500);
            }
        });

        // fluid layout
        var setHeight = function () {
            $('.app-fluid #nav > *').css('min-height', $(window).height() - 60);
            return true;
        };
        setHeight();


        // fix vbox
        var fixVbox = function () {
            $('.ie11 .vbox').each(function () {
                $(this).height($(this).parent().height());
            });
            return true;
        };
        fixVbox();

        // collapse nav
        $(document).on('click', '[data-ride="collapse"] a', function (e) {
            var $this = $(e.target), $active;
            $this.is('a') || ($this = $this.closest('a'));

            $active = $this.parent().siblings(".active");
            $active && $active.toggleClass('active').find('> ul:visible').slideUp(200);

            ($this.parent().hasClass('active') && $this.next().slideUp(200)) || $this.next().slideDown(200);
            $this.parent().toggleClass('active');

            $this.next().is('ul') && e.preventDefault();

            setTimeout(function () {
                $(document).trigger('updateNav');
            }, 300);
        });

        // dropdown still
        $(document).on('click.bs.dropdown.data-api', '.dropdown .on, .dropup .on, .open .on', function (e) {
            e.stopPropagation()
        });

    });

}(jQuery);