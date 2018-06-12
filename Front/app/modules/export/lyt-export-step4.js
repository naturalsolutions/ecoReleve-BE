define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'sweetAlert',
    'moment',
    'config',
    'i18n'
], function($, _, Backbone, Marionette, Swal, Moment, Config) {
    'use strict';
    return Marionette.LayoutView.extend({
        className: 'full-height export-layout',
        template: 'app/modules/export/templates/tpl-export-step4.html',


        name: '<span class="export-step4"></span>',

        ui: {
            'pdfTile': '#pdfTile',
            'csvTile': '#csvTile',
            'gpxTile': '#gpxTile',
            'excelTile': '#excelTile',
        },

        events: {
            'change input.exportValue': 'changeValue',
            'change #sinpref ': 'activateNext'
        },

        initialize: function(options) {
            var _this = this;
            this.model = options.model;
            this.parent = options.parent;

            this.options.parent.finished = function() {
                _this.getFile();
            };
        },

        onShow: function() {
            this.$el.find('.tile-inside:first input').prop('checked', true).change();
            this.$el.find('.tile-inside:first').addClass('active');
            this.$el.i18n();
            var stepName = i18n.translate('export.step4-label');
            $('.export-step4').html(stepName);
        },

        changeValue: function(e) {
            var exportType = $(e.target).val();
            this.$el.find('label.tile-inside').each(function() {
                $(this).removeClass('active');
            });

            $(e.target).parent().addClass('active');
            this.model.set('fileType', exportType);

            if (exportType === 'sinp') {
                $('.sinpMetadata').removeClass('hidden');
                //$('#btnNext').attr('disabled', 'disabled');
            } else {
                $('.sinpMetadata').addClass('hidden');
                //$('#btnNext').removeAttr('disabled');
                $('#sinpref').val('');
            }


        },
        activateNext: function(e) {
            var ref = $('#sinpref').val();
            if (ref) {
                $('#btnNext').removeAttr('disabled');
            }

        },
        validate: function() {
            return this.model;
        },

        check: function() {
            return true;
        },

        swal: function(opts) {
            Swal({
                    title: opts.title || opts.responseText || 'error',
                    text: opts.text || '',
                    type: opts.type,
                    showCancelButton: opts.showCancelButton,
                    confirmButtonColor: opts.confirmButtonColor,
                    confirmButtonText: opts.confirmButtonText,
                    closeOnConfirm: opts.closeOnConfirm || true,
                },
                function(isConfirm) {
                    //could be better
                    if (opts.callback) {
                        opts.callback(isConfirm);
                    }
                });
        },

        getFile: function() {
            var _this = this;
            this.datas = {
                // fileType: this.model.get('fileType'),
                // viewId: this.model.get('protocolType_id'),
                filters: this.model.get('filters'),
                columns: this.model.get('columns'),
            };

            if (this.model.get('fileType') == 'excel') {
                var url = Config.coreUrl + 'export/projects/' + this.model.get('project_id') +
                    '/observations/getFile?protocolType=' + this.model.get('protocolType_id') +
                    '&fileType=' + this.model.get('fileType') +
                    '&criteria=' + JSON.stringify(this.model.get('filters')) +
                    '&columns=' + JSON.stringify(this.model.get('columns'));
                var link = document.createElement('a');
                link.classList.add('DowloadLinka');

                //link.download = url;
                link.href = url;
                link.onclick = function() {
                    //this.parentElement.removeChild(this);
                    var href = $(link).attr('href');
                    window.location.href = link;
                    document.body.removeChild(link);
                    var opts = {
                        title: i18n.t('export.msgExportOkTitle'),
                        text: i18n.t('export.msgExportOkText'),
                        type: 'success',
                        confirmButtonText: 'Ok',
                        cancelButtonText: i18n.t('export.msgGoBackHome'),
                        showCancelButton: true,
                        callback: function(isConfirm) {
                            if (!isConfirm) {
                                Backbone.history.navigate('home', { trigger: true });
                            }
                            //_this.parent.displayStep(0);
                        }
                    };

                    _this.swal(opts);
                };
                /*his.$el.append(link);*/
                document.body.appendChild(link);
                link.click();
            } else {

                var route = 'export/projects/' + this.model.get('project_id') + '/observations/getFile?protocolType=' + this.model.get('protocolType_id') + '&fileType=' + this.model.get('fileType');
                $.ajax({
                    url: route,
                    data: { criteria: JSON.stringify(this.datas.filters), columns: JSON.stringify(this.datas.columns) },
                    contentType: 'application/json',
                    type: 'GET',
                    context: this,
                }).done(function(data) {
                    var url = URL.createObjectURL(new Blob([data], { 'type': 'application/' + this.model.get('fileType') }));
                    var link = document.createElement('a');
                    link.href = url;
                    var fileType = this.model.get('fileType') == 'sinp' ? 'csv' : this.model.get('fileType');

                    link.download = this.model.get('project_name') + '_' + this.model.get('protocolType_name') + '_' + new Moment().format('DD-MM-YY') + '.' + fileType;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    var _this = this;
                    var opts = {
                        title: i18n.t('export.msgExportOkTitle'),
                        text: i18n.t('export.msgExportOkText'),
                        type: 'success',
                        confirmButtonText: 'Ok',
                        cancelButtonText: i18n.t('export.msgGoBackHome'),
                        showCancelButton: true,
                        callback: function(isConfirm) {
                            if (!isConfirm) {
                                Backbone.history.navigate('home', { trigger: true });
                            }
                            //_this.parent.displayStep(0);
                        }
                    };

                    this.swal(opts);
                }).fail(function(msg) {

                });
            }

        },

    });
});