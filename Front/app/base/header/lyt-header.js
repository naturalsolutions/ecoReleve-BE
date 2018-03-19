define([
        'jquery',
        'marionette',
        'config',
        './lyt-breadcrumb',
        'bootstrap'
    ],
    function($, Marionette, config, Breadcrumb) {
        'use strict';
        return Marionette.LayoutView.extend({
            template: 'app/base/header/tpl-header.html',
            className: 'header',
            events: {
                'click #logout': 'logout'
            },
            regions: {
                'breadcrumb': '#breadcrumb'
            },

            ui: {
                'userName': '#userName',
            },

            logout: function() {
                $.ajax({
                    context: this,
                    url: 'security/logout'
                }).done(function() {
                    document.location.href = config.portalUrl;
                });
            },

            onShow: function() {
            // activate pipefy if it is demo instance
            this.loadSelectProject();
            var _this = this;
            var isDomoInstance = config.instance ;
            if(isDomoInstance == 'demo') {
                $('.pipefy-support').removeClass('hidden');
            }
            this.$el.i18n();

            this.breadcrumb.show(new Breadcrumb());
            window.app.user = new Backbone.Model();
            window.app.user.url = 'currentUser';
            window.app.user.fetch({
                success: function(data) {
                $('body').addClass(window.app.user.get('role'));
                $.xhrPool.allowAbort = true;
                _this.ui.userName.html(window.app.user.get('fullname'));
                }
            });
            },

            loadSelectProject: function(){
            $.ajax({
                context:this,
                url: 'projects?criteria=%5B%5D&page=1&per_page=200&offset=0&order_by=%5B%5D&typeObj=1',
                success: function(data){
                console.log(data);
                var project_list = data[1];
                $('#js-select-project').append(new Option('Tous les projects',0));
        
                _.each(project_list,function(model) {
                    $('#js-select-project').append(new Option(model.Name,model.ID));
                },this);
                this.customSelect();
                }
            });
            },
            customSelect: function(){
            var _this = this;
            $('#js-select-project').each(function(){
                var $this = $(this), numberOfOptions = $(this).children('option').length;
            
                $this.addClass('select-hidden'); 
                $this.wrap('<div class="select nav"></div>');
                $this.after('<div class="select-styled"></div>');
            
                var $styledSelect = $this.next('div.select-styled');
                $styledSelect.text($this.children('option').eq(0).text());
            
                var $list = $('<ul />', {
                    'class': 'select-options'
                }).insertAfter($styledSelect);
            
                for (var i = 0; i < numberOfOptions; i++) {
                    var li = $('<li />', {
                        text: $this.children('option').eq(i).text(),
                        rel: $this.children('option').eq(i).val()
                    }).prepend('<span class="reneco reneco-folder" style="margin-right:8px;"/>');
                    li.appendTo($list);
                }
            
                var $listItems = $list.children('li');
                $styledSelect.click(function(e) {
                    e.stopPropagation();
                    $('div.select-styled.active').not(this).each(function(){
                        $(this).removeClass('active').next('ul.select-options').hide();
                    });
                    $(this).toggleClass('active').next('ul.select-options').toggle();
                });
            
                $listItems.click(function(e) {
                    e.stopPropagation();
                    $styledSelect.text($(this).text()).removeClass('active');
                    $this.val($(this).attr('rel'));
                    $list.hide();
                    _this.setContextProject($(this).attr('rel'));
                });
            
                $(document).click(function() {
                    $styledSelect.removeClass('active');
                    $list.hide();
                });
            
            });
            },

            setContextProject: function(project_id){
            if(project_id){
                window.curent_project_url = 'projects/'+project_id+'/';
            } else{
                window.curent_project_url = '';
            }
            },
        });
});
