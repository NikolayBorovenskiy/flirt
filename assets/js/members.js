'use strict';

var Members = (function(Filter, Search) {
    var CREATE_THREAD_URL = '/messages/thread/',
        MEMBERS_URL = '/members',
        _params = [],
        _search = '';

    function Members($members) {
        if (!(this instanceof Members)) {
            return new Members($members);
        }

        this.$root = $members;
        this.$list = this.$root.find('.j-members_list');
        this.$view = this.$root.find('.j-members_view');
        this.init();
    }

    Members.prototype = {
        constructor: Members,
        view: 'grid',
        init: function() {
            this.data = this.$root.data();
            if (this.data.filtered) {
                this.subscribe();
            }
            this.bindEvents();
        },

        subscribe: function() {
            var self = this;

            Filter.subscribe(function(params) {
                _params = params;
                self.filterData();
            });

            Search.subscribe(function(search) {
                console.log(search, 'wq');
                _search = search;
                self.filterData();
            });
        },

        bindEvents: function() {
            var self = this;
            self.$root.on('click', '.j-members_bookmark', function() {
                var $el = $(this);
                self.createBookmark($el);
                return false;
            });
            self.$root.on('click', '.j-members_message', function() {
                var $el = $(this);
                self.createThread($el.closest('[data-email]').data().email);
                return false;
            });
        },

        filterData: function() {
            var filterParams = this.buildFilterQueryObject(),
                searchParams = this.buildSearchQueryObject(),
                self = this;
            $.get(MEMBERS_URL, _.extend(searchParams, filterParams), function(html) {
                self.clear().render(html);
            });
        },

        createBookmark: function($el) {
            var button = $el,
                url,
                email = $el.closest('[data-email]').data().email;
            url = '/bookmarks/add/' + email + '/';
            $.post(url, {},
                function(data) {
                    var message = "Вы добавили " + data['user']['first_name'] + " " + data['user']['last_name'] + " в закладки";
                    $("#messages").append("<div class='alert alert-dismissible alert-success'><button type='button' class='close' data-dismiss='alert'>×</button><p>" + message + "</p></div>");
                    button.hide();
                });
        },
        createThread: function(email) {
            $.post(CREATE_THREAD_URL, {email: email}, function(data) {
                window.location.href = '/messages/'
            });
        },

        buildFilterQueryObject: function() {
            var groupParams = {};
            _params.forEach(function(param) {
                if (groupParams[param.by]) {
                    groupParams[param.by].push(param);
                } else {
                    groupParams[param.by] = [param];
                }
            });
            for (var paramKey in groupParams) {
                var groupValue, min, max;
                groupValue = groupParams[paramKey]
                    .map(function(param) {
                        return param.value;
                    });
                groupValue = Array.prototype.concat.apply([], groupValue);
                if (groupValue.length > 2) {
                    min = Math.min.apply(Math, groupValue);
                    max = Math.max.apply(Math, groupValue);
                    groupValue = [min, max];
                }
                groupParams[paramKey] = groupValue;
            }

            return groupParams;
        },

        buildSearchQueryObject: function() {
            var obj = {};
            _search && (obj = {search: _search});
            return obj;
        },

        render: function(html) {
            this.$list.append(html);
        },

        clear: function() {
            this.$list.html('');
            return this;
        }
    };

    return Members;

}(window.Filter, window.Search));


$(function() {
    var $members = $('.j-members');
    if (!$members.length) return;

    $members.each(function() {
        new Members($(this));
    });
});