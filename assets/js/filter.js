'use strict';

var Filter = (function() {
    var _params = [];


    return {
        $root: $('#j-filter'),

        init: function() {
            this.$root.find('.j-filter_clear').hide();
            this.bindEvents();
        },

        bindEvents: function() {
            var self = this;
            self.$root
                .on('click', 'a', function(e) {
                    var $el = $(this),
                        multi = e.shiftKey || e.ctrlKey;
                    if (!$el.data().by) return;
                    self.select($el, multi);
                    return false;
                })
                .on('click', '.j-filter_clear', function() {
                    self.clearFilter($(this));
                    return false;
                });
        },

        select: function($el, multi) {
            var self = this,
                data = _.extend({}, $el.data()),
                isExist;
            data.value = data.value.toString().indexOf('-') > -1 ? data.value.toString().split('-') : data.value;
            $el.closest('ul').parent().closest('ul').find('.j-filter_clear').show();

            if (!multi) {
                $el.parent().addClass('active');
                $el.parent().siblings().removeClass('active');
                isExist = false;
                for (var i = 0; i < _params.length; i++) {
                    if (_params[i].by == data.by) {
                        _params[i].value = data.value;
                        isExist = true;
                        break;
                    }
                }
                if (!isExist) _params.push(data);
            } else {
                var index = -1;
                isExist = _params.some(function(item, idx) {
                    if (item.by == data.by && _.isEqual(item.value, data.value)) {
                        index = idx;
                        return true;
                    }
                    return false;
                });
                if (isExist) {
                    $el.parent().removeClass('active');
                    _params.splice(index, 1);
                    if (!_params.some(function(item) {
                            return item.by == data.by;
                        })) {
                        $el.closest('ul').parent().closest('ul').find('.j-filter_clear').hide();
                    }
                } else {
                    $el.parent().addClass('active');
                    _params.push(data);
                }
            }

            this.published(_params);
        },

        clearFilter: function($el) {
            var by = $el.data().by,
                clearedParams = [];
            $el.hide();
            $el.closest('ul').find('.active').removeClass('active');
            for (var i = 0; i < _params.length; i++) {
                console.log(i);
                if (_params[i].by !== by) {
                    clearedParams.push(_params[i]);
                }
            }
            _params = clearedParams;
            this.published(_params);
        },

        published: function(params) {
            var self = this;
            self.subscribed.forEach(function(item) {
                item.cb.call(item.context, params);
            });
        },

        subscribed: [],

        subscribe: function(cb, context) {
            this.subscribed.push({cb: cb, context: context});
        }

    }
}());


$(function() {
    if ($('#j-filter')) {
        Filter.init();
    }
});