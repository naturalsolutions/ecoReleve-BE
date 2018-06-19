define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'sweetAlert',
    //'translater',
    //'ns_modules/ns_com',
    //'ns_grid/grid.view',
    //'ns_filter/filters',
    'config',
    //'tooltipster-list',
    //'i18n'

], function(
    $, _, Backbone, Marionette, Swal,
    Config
) {

    'use strict';

    return Marionette.LayoutView.extend({

        template: 'app/modules/sinp/sinp.tpl.html',
        className: 'full-height animated white rel',

        events: {
            'click .sinpValue': 'activateIframe'

        },

        initialize: function(options) {

        },
        activateIframe: function(e) {
            $('.sinpInfos').addClass('hidden');
            var elem = $(e.target);
            var id = $(elem).attr('id');
            $('.sinpValue').removeClass('sinpSelected');
            $(elem).addClass('sinpSelected');
            if (id === 'inpnLink') {
                $('#inpn').removeClass('hidden');
                $('#ginco').addClass('hidden');
            } else {
                $('#inpn').addClass('hidden');
                $('#ginco').removeClass('hidden');
            }
        },

        onShow: function() {


        },

        afterShow: function() {
            //console.warn('method not implemented');
        },

        changePageSize: function(e) {
            this.gridView.changePageSize($(e.target).val());
        },

    });
});