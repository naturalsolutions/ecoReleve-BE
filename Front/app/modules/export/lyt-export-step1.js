define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'i18n'
], function($, _, Backbone, Marionette) {
    'use strict';
    return Marionette.LayoutView.extend({
        className: 'full-height',
        template: 'app/modules/export/templates/tpl-export-step1.html',

        name: '<span class="export-step1"></span>',
        /*name : (function () {
            return i18n.translate('export.step1-label'); 
        })(),*/

        ui: {
            'themes': '#themes',
            'views': '#views',
            'requirement': '#requirement'
        },

        events: {
            'click #themes>li': 'getViews',
            'click #views>li': 'enableNext',
        },

        initialize: function(options) {
            this.model = new Backbone.Model();
            this.themeColl = new Backbone.Collection();
            this.themeColl.url = 'export/projects';
            this.defered = this.themeColl.fetch();

            this.model.set('protocolType_id', '');
            this.model.set('protocolType_name', '');
        },

        onShow: function() {
            var _this = this;
            $.when(this.defered).done(function() {
                _this.themeColl.each(function(model, index) {
                    var line = $('<li class="list-group-item" value="' + model.get('ID') + '">' + model.get('Name') + '</li>');
                    _this.ui.themes.append(line);
                });
            });
            this.$el.i18n();
            var stepName = i18n.translate('export.step1-label');
            $('.export-step1').html(stepName);
        },

        getViews: function(e) {
            var _this = this;

            this.ui.themes.find('.active').removeClass('active');
            $(e.target).addClass('active');
            var project_name = $(e.target).html();
            this.model.set('project_name', project_name);

            this.ui.requirement.val('').change();

            this.viewColl = new Backbone.Collection();
            this.project_id = $(e.target).val();
            this.viewColl.url = 'export/projects/' + this.project_id + '/protocols';
            var defered = this.viewColl.fetch();

            _this.ui.views.empty();
            $.when(defered).done(function() {
                _this.viewColl.each(function(model, index) {
                    var line = $('<li class="list-group-item" value="' + model.get('ID') + '">' + model.get('Name') + '</li>');
                    _this.ui.views.append(line);
                });
            });
        },

        enableNext: function(e) {
            this.ui.views.find('.active').removeClass('active');
            $(e.target).addClass('active');
            var protocolType_id = $(e.target).val();
            var protocolType_name = $(e.target).html();
            this.ui.requirement.val(protocolType_id).change();

            this.model.set('project_id', this.project_id);
            this.model.set('protocolType_id', protocolType_id);
            this.model.set('protocolType_name', protocolType_name);
        },

        validate: function() {
            return this.model;
        },

        check: function() {
            if (this.ui.requirement.val()) {
                return true;
            } else {
                return false;
            }
        },

    });
});