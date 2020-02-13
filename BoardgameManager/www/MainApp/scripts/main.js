$(function() {
    function getRight() {
        if (!$('[data-toggle="popover"]').length) return 0
        return ($(window).width() - ($('[data-toggle="popover"]').offset().left + $('[data-toggle="popover"]').outerWidth()))
    }

    // $(window).on('resize', function() {
    //     var instance = $('[data-toggle="popover"]').data('bs.popover')
    //     if (instance) {
    //         instance.config.viewport.padding = getRight()
    //     }
    // })

    $('[data-toggle="popover"]').popover({
        template: '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-body popover-content px-0"></div></div>',
        title: '',
        html: true,
        trigger: 'manual',
        placement: 'bottom',
        viewport: {
            selector: 'body',
            padding: getRight()
        },
        content: function() {
            var $nav = $('#js-popoverContent').clone()
            return '<ul class="nav nav-pills nav-stacked flex-column" style="width: 120px">' + $nav.html() + '</ul>'
        }
    })

    $('[data-toggle="popover"]').on('click', function(e) {
        e.stopPropagation()
        if ($($('[data-toggle="popover"]').data('bs.popover').getTipElement()).hasClass('in')) {
            $('[data-toggle="popover"]').popover('hide')
            $(document).off('click.app.popover')

        } else {
            $('[data-toggle="popover"]').popover('show')

            setTimeout(function() {
                $(document).one('click.app.popover', function() {
                    $('[data-toggle="popover"]').popover('hide')
                })
            }, 1)
        }
    })

    // Set body padding to height of navbar
    $("body").css("padding-top", $("#app-navbar").height() + "px");

    var filterShowing = false;
    var FILTER_SHOW_TIME = 0.5;
    var computedHeight = 0;
    $("#filter-toggle-btn").click(function() {
        if (window.metadataLoaded) {
            if (!filterShowing) {
                $("#filter-panel-div").css("display", "block");

                // Hack to get the computed height of the element so we know what to tween to
                $("#filter-panel-div").css("max-height", "100%");
                computedHeight = $("#filter-panel-div").height();
                $("#filter-panel-div").css("max-height", "0px");

                TweenLite.to("#filter-panel-div", FILTER_SHOW_TIME, {
                    "max-height": computedHeight+"px",
                    onComplete:function() {
                        $(this.target).css("max-height", "max-content");
                        filterShowing = true;
                        $(this.target).css("overflow", "visible");
                    },
                });
            }
            else {
                $("#filter-panel-div").css("max-height", computedHeight+"px");
                $("#filter-panel-div").css("overflow", "hidden");
                TweenLite.to("#filter-panel-div", FILTER_SHOW_TIME, {"max-height":"0px", onComplete:function() {
                    filterShowing = false;
                    // console.log(this.target);
                    $(this.target).css("display", "none");
                }});
            }
        }
    })
})

Vue.directive('tooltip', function(el, binding){
    $(el).popover({
        html: true,
        // title: binding.value,
        title: "Information",
        placement: binding.arg,
        trigger: 'hover',
        content: function() {
            var bgg_id = $(this).attr("bgg_id");
            return $('#' + bgg_id + "_popover").html();
        },
    });
})

// Must remember to hide the original divs for the pop ups after initializing them
$(".bg-popover").css("display", "none");

var collectionArea = new Vue({
    delimiters: ['[[', ']]'],
    el: '#main',
    data() {
        return {
            collection: null,
            metadata: {
                mechanics: null,
            },
            filter: {
                showExpansions: false,
                mechanics: [],
                numPlayers: null,
                searchText: "",
                sortBy: "BGG Rating",
                sortByOrder: "Desc",
            },
            gamePicker: {
                numPlayers: 0,
                coop: "both",
                weights: ["light", "medium", "heavy"],
            },
        }
    },
    // Filter params
    // min/max players
    // duration
    // mechanics
    computed: {
        filteredAndSortedCollection: function() {
            window.filter = this.filter;
            var self = this;
            if (this.collection) {
                var filtered = this.collection.boardgames;
                if (this.filter.searchText) {
                    filtered = filtered.filter(bg_item => {
                        return bg_item.boardgame.name.toLowerCase().includes(this.filter.searchText.toLowerCase())
                    });
                }
                if (!this.filter.showExpansions) {
                    filtered = filtered.filter(bg_item => !bg_item.boardgame.is_expansion);
                }
                if (this.filter.mechanics.length > 0) {
                    filtered = filtered.filter(function(bg_item) {
                        // OR
                        // Return true if an item in the boardgames list of mechanics is also in the filter list
                        // return bg_item.boardgame.mechanics.some(m => self.filter.mechanics.indexOf(m) >= 0);

                        // AND
                        found = _.map(self.filter.mechanics, (m => bg_item.boardgame.mechanics.indexOf(m) >= 0));
                        // found = _.map(bg_item.boardgame.mechanics, (m => self.filter.mechanics.indexOf(m.name) >= 0));
                        allFound = found.indexOf(false) < 0;
                        return allFound;
                    })
                }
                if (this.filter.numPlayers) {
                    filtered = filtered.filter(function(bg_item) {
                        return this.filter.numPlayers >= bg_item.boardgame.min_players &&
                               this.filter.numPlayers <= bg_item.boardgame.max_players;
                    })
                }

                var sorted = filtered;
                if (this.filter.sortBy) {
                    if (this.filter.sortBy === "Alphabetical") {
                        sorted = sorted.sort((a, b) => a.boardgame.name.localeCompare(b.boardgame.name));
                    }
                    else if (this.filter.sortBy === "BGG Rating") {
                        sorted = sorted.sort((a, b) => a.boardgame.statistics.bayesian_avg_rating - b.boardgame.statistics.bayesian_avg_rating);
                    }
                    else if (this.filter.sortBy === "User Rating") {
                        sorted = sorted.sort((a, b) => a.rating - b.rating);
                    }
                    else if (this.filter.sortBy === "Num Plays") {
                        sorted = sorted.sort((a, b) => a.num_plays - b.num_plays);
                    }
                    else if (this.filter.sortBy === "Min Players") {
                        sorted = sorted.sort((a, b) => a.boardgame.min_players - b.boardgame.min_players);
                    }
                    else if (this.filter.sortBy === "Max Players") {
                        sorted = sorted.sort((a, b) => a.boardgame.max_players - b.boardgame.max_players);
                    }
                    else if (this.filter.sortBy === "Complexity") {
                        sorted = sorted.sort((a, b) => a.boardgame.statistics.avg_weight - b.boardgame.statistics.avg_weight);
                    }
                }
                if (this.filter.sortByOrder === "Desc") {
                    sorted.reverse();
                }

                return sorted;
            }
            else {
                return null;
            }
        },
        curatedCollection: function() {
            window.gamePicker = this.gamePicker;
            var self = this;
            if (this.collection) {
                var filtered = this.collection.boardgames;
                filtered = filtered.filter(bg_item => !bg_item.boardgame.is_expansion);

                var MIN_CURATED_RATING = 6.75;
                // Filter out games with BGG rating less than 6.75
                filtered = filtered.filter(function(bg_item) {
                    return bg_item.boardgame.statistics.bayesian_avg_rating >= MIN_CURATED_RATING;
                })

                if (this.gamePicker.numPlayers > 0) {
                    filtered = filtered.filter(function(bg_item) {
                        var recommended = bg_item.boardgame.player_suggestions.recommended;
                        return recommended.indexOf(this.gamePicker.numPlayers) != -1;
                    })
                }

                if (this.gamePicker.coop != "both") {
                    if (this.gamePicker.coop == "vs") {
                        filtered = filtered.filter(function(bg_item) {
                            return bg_item.boardgame.mechanics.indexOf("Cooperative Play") == -1;
                        })
                    }
                    else {
                        filtered = filtered.filter(function(bg_item) {
                            return bg_item.boardgame.mechanics.indexOf("Cooperative Play") != -1;
                        })
                    }
                }

                var includeLight = this.gamePicker.weights.indexOf("light") != -1;
                var includeMedium = this.gamePicker.weights.indexOf("medium") != -1;
                var includeHeavy = this.gamePicker.weights.indexOf("heavy") != -1;

                if (!includeLight) {
                    filtered = filtered.filter(function(bg_item) {
                        var weight = bg_item.boardgame.statistics.avg_weight;
                        return weight >= 2.0;
                    })
                }
                if (!includeMedium) {
                    filtered = filtered.filter(function(bg_item) {
                        var weight = bg_item.boardgame.statistics.avg_weight;
                        return weight < 2.0 || weight >= 3.0;
                    })
                }
                if (!includeHeavy) {
                    filtered = filtered.filter(function(bg_item) {
                        var weight = bg_item.boardgame.statistics.avg_weight;
                        return weight < 3.0;
                    })
                }

                var sorted = filtered;
                sorted = sorted.sort((a, b) => a.boardgame.statistics.bayesian_avg_rating - b.boardgame.statistics.bayesian_avg_rating);
                sorted.reverse();

                        // sorted = sorted.sort((a, b) => a.boardgame.statistics.avg_weight - b.boardgame.statistics.avg_weight);

                return sorted;
            }
            else {
                return null;
            }
        },
    },
    mounted() {
        var self = this;

        var username = window.username;
        axios
            .get('/user_collection/' + username)
            .then(response => {
                self.collection = response.data;
                window.collection = self.collection
                self.collection.boardgames.sort((a, b) => a.boardgame.name.localeCompare(b.boardgame.name));

                for (var i = 0; i < self.collection.boardgames.length; i++) {
                    var bg = self.collection.boardgames[i].boardgame
                    // Flatten list of mechanic objects into mechanics
                    bg.mechanics = _.map(bg.mechanics, (m => m.name));
                    // Set avg_rating/avg_weight display as avg_rating to two decimal places
                    bg.statistics.avg_rating_2dp = bg.statistics.avg_rating.toFixed(2);
                    bg.statistics.bayesian_avg_rating_2dp = bg.statistics.bayesian_avg_rating.toFixed(2);
                    bg.statistics.avg_weight_2dp = bg.statistics.avg_weight.toFixed(2);
                }
                // self.collection.boardgames = _.invoke(self.collection.boardgames, (bg =>
                //     bg.boardgame.mechanics = _.map(bg.boardgame.mechanics, (m => m.name)))
                // );

                // function flattenMechanics (bg) {
                //     console.log(bg);
                //     bg.boardgame.mechanics = _.map(bg.boardgame.mechanics, (m => m.name));
                // }
                // var testest = _.invoke(self.collection.boardgames, 'flattenMechanics');
            });

        axios
            .get('/boardgame_metadata')
            // .then(response => (this.metadata = response.data));
            .then(function(response) {
                self.metadata.mechanics = response.data.mechanics.map(mechanic => mechanic.name);
                self.metadata.mechanics.sort((a, b) => a.localeCompare(b));
                self.$nextTick(() => {
                    window.metadataLoaded = true;
                    $('#filter-mechanics').selectpicker({
                        liveSearch: true,
                        selectedTextFormat: 'static',
                        noneSelectedText: '',
                    });
                });
            });
    },
    methods: {
        removeMechanicFilter: function (event) {
            var mechanicStr = $(event.target).parent().attr("mechanic_id");
            // console.log("Removing " + mechanicStr);
            this.filter.mechanics.splice(this.filter.mechanics.indexOf(mechanicStr), 1);
        },
        filterPickedGames: function (event) {
            $('#game-picker-modal').modal('hide');
            $('#curated-collection-modal').modal('show');

            this.showCuratedGames = true;
        },
        isMobile() {
            if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                return true;
            } else {
                return false;
            }
        }
    }
})

// $(document).on('click', '.js-gotoMsgs', function() {
//     $input.remove()
//     $('.js-conversation').addClass('d-none')
//     $('.js-msgGroup, .js-newMsg').removeClass('d-none')
//     $('.modal-title').html('Messages')
// })

// $(document).on('click', '[data-action=growl]', function(e) {
//     e.preventDefault()

//     $('#app-growl').append(
//         '<div class="alert alert-dark alert-dismissible fade show" role="alert">' +
//         '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
//         '<span aria-hidden="true">×</span>' +
//         '</button>' +
//         'Click the x on the upper right to dismiss this little thing. Or click growl again to show more growls' +
//         '</div>'
//     )
// })

// $(document).on('focus', '[data-action="grow"]', function() {
//     if ($(window).width() > 1000) {
//         $(this).animate({
//             width: 300
//         })
//     }
// })

// $(document).on('blur', '[data-action="grow"]', function() {
//     if ($(window).width() > 1000) {
//         var $this = $(this).animate({
//             width: 180
//         })
//     }
// })

// // back to top button - docs
// $(function() {
//     if ($('.docs-top').length) {
//         _backToTopButton()
//         $(window).on('scroll', _backToTopButton)

//         function _backToTopButton() {
//             if ($(window).scrollTop() > $(window).height()) {
//                 $('.docs-top').fadeIn()
//             } else {
//                 $('.docs-top').fadeOut()
//             }
//         }
//     }
// })

// $(function() {
//     // doc nav js
//     var $toc = $('#markdown-toc')
//     $('#markdown-toc li').addClass('nav-item')
//     $('#markdown-toc li > a').addClass('nav-link')
//     $('#markdown-toc li > ul').addClass('nav')
//     var $window = $(window)

//     if ($toc[0]) {

//         maybeActivateDocNavigation()
//         $window.on('resize', maybeActivateDocNavigation)

//         function maybeActivateDocNavigation() {
//             if ($window.width() > 768) {
//                 activateDocNavigation()
//             } else {
//                 deactivateDocNavigation()
//             }
//         }

//         function deactivateDocNavigation() {
//             $window.off('resize.theme.nav')
//             $window.off('scroll.theme.nav')
//             $toc.css({
//                 position: '',
//                 left: '',
//                 top: ''
//             })
//         }

//         function activateDocNavigation() {

//             var cache = {}

//             function updateCache() {
//                 cache.containerTop = $('.docs-content').offset().top - 40
//                 cache.containerRight = $('.docs-content').offset().left + $('.docs-content').width() + 45
//                 measure()
//             }

//             function measure() {
//                 var scrollTop = $window.scrollTop()
//                 var distance = Math.max(scrollTop - cache.containerTop, 0)

//                 if (!distance) {
//                     $($toc.find('li a')[1]).addClass('active')
//                     return $toc.css({
//                         position: '',
//                         left: '',
//                         top: ''
//                     })
//                 }

//                 $toc.css({
//                     position: 'fixed',
//                     left: cache.containerRight,
//                     top: 40
//                 })
//             }

//             updateCache()

//             $(window)
//                 .on('resize.theme.nav', updateCache)
//                 .on('scroll.theme.nav', measure)

//             $('body').scrollspy({
//                 target: '#markdown-toc'
//             })

//             setTimeout(function() {
//                 $('body').scrollspy('refresh')
//             }, 1000)
//         }
//     }
// })
