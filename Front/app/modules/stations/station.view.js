define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'sweetAlert',

    'ns_modules/ns_com',
    'ns_form/NsFormsModuleGit',
    'ns_navbar/navbar.view',
    './protocols/protocols.view',

    'modules/objects/detail.view',
    './station.model',

    'ns_map/ns_map',
], function(
    $, _, Backbone, Marionette, Swal,
    Com, NsForm, NavbarView, LytProtocols,
    DetailView, StationModel, NsMap
) {

    'use strict';

    return DetailView.extend({
        template: 'app/modules/stations/station.tpl.html',
        className: 'full-height white station',

        ModelPrototype: StationModel,

        events: {
            'click .tab-link': 'displayTab',
            'change input[name="LAT"], input[name="LON"]': 'getLatLng',
        },

        ui: {
            formStation: '.js-from-station',
            formStationBtns: '.js-from-btns',
            'map': '.js-map',
        },

        regions: {
            'rgStation': '.js-rg-station',
            'rgProtocols': '.js-rg-protocols',
            'rgProtocol': '.js-rg-protocol',
            'rgNavbar': '.js-navbar'
        },

        initialize: function(options) {
            this.model = new this.ModelPrototype();
            this.com = new Com();
            this.model.set('id', options.id);
            this.map = null;

            this.model.set('stationId', options.id);

            this.model.set('urlParams', {
                proto: options.proto,
                obs: options.obs
            });
        },

        reload: function(options) {
            var _this = this;
            if (options.id == this.model.get('id')) {
                this.LytProtocols.protocolsItems.getViewFromUrlParams(options);
            } else {
                this.model.set('id', options.id);
                this.model.set('stationId', options.id);
                this.model.set('urlParams', {
                    proto: options.proto,
                    obs: options.obs
                });
                this.displayStation();
            }
            if (this.map) {
                $.when(this.nsForm.jqxhr).then(function() {
                    _this.initMarker();
                });
            }
        },

        displayProtos: function() {
            this.rgProtocols.show(this.LytProtocols = new LytProtocols({
                model: this.model,
                parent: this,
            }));
        },

        displayMap: function() {
            var self = this;
            this.map = new NsMap({
                zoom: 3,
                popup: true,
                drawable: true,
                drawOptions: {
                    circle: false,
                    rectangle: false,
                    polyline: false,
                    polygon: false,
                    circlemarker: false
                }
            });
            $.when(this.nsForm.jqxhr && this.map.deffered).then(function() {
                self.initMarker();
            });

            this.map.map.on('draw:created', function(e) {
                var type = e.layerType;
                self.currentLayer = e.layer;
                self.map.drawnItems.addLayer(self.currentLayer);
                var latlon = self.currentLayer.getLatLng();
                self.setLatLonForm(latlon.lat, latlon.lng);
                self.map.toggleDrawing();
            });

            this.map.map.on('draw:edited', function (e) {
                var latlon = self.currentLayer.getLatLng();
                self.setLatLonForm(latlon.lat, latlon.lng);
              });
              
              this.map.map.on('draw:deleted', function () {
                self.removeLatLngMakrer(true);
              });

                //this.rgProtocol.currentView.rgObservation.currentView
            if (this.rgProtocol) {
                if(this.rgProtocol.currentView) {
                    if(this.rgProtocol.currentView.rgObservation) {
                        if(this.rgProtocol.currentView.rgObservation.currentView) {
                            var newItem = this.rgProtocol.currentView.rgObservation.currentView.model;
                            var geom = newItem.get('geom')
                            if (geom) {
                                this.map.addGeometry(geom, true);
                                this.map.disableDrawingControl();
                            }
                        }
                    }
                }
            }
        },

        initMarker: function(){
            var lat = this.nsForm.model.get('LAT');
            var lon = this.nsForm.model.get('LON');
            if(this.map && this.map.drawnItems && this.map.drawnItems.getLayers().length){
                this.map.drawnItems.clearLayers();
            }
            if(lat && lon){
                // this.map.toggleDrawing();
                this.currentLayer = this.map.addMarker(null,
                    this.nsForm.model.get('LAT'),
                    this.nsForm.model.get('LON'),
                    false,
                    false,
                    this.map.drawnItems);
            }
        },

        removeLatLngMakrer: function(reInitLatLng){
            if(this.currentLayer){
            this.map.drawnItems.removeLayer(this.currentLayer);
            this.currentLayer = null;
            }
            if(reInitLatLng){
            this.$el.find('input[name="LAT"]').val('');
            this.$el.find('input[name="LON"]').val('');
            }
            this.map.toggleDrawing();
        },
    
        setLatLonForm: function(lat, lon){
            var lat = this.$el.find('input[name="LAT"]').val(parseFloat(lat.toFixed(5)));
            var lon = this.$el.find('input[name="LON"]').val(parseFloat(lon.toFixed(5)));
        },
    
        getLatLng: function() {
            var lat = this.$el.find('input[name="LAT"]').val();
            var lon = this.$el.find('input[name="LON"]').val();
            this.updateMarkerPos(lat, lon);
        },

        updateMarkerPos: function(lat, lon) {
            if (lat && lon) {
            // this.map.toggleDrawing(true);
            if(this.currentLayer){
                this.currentLayer.setLatLng(new L.LatLng(lat, lon));
            } else {
                this.currentLayer = new L.marker(new L.LatLng(lat, lon));
                this.map.drawnItems.addLayer(this.currentLayer)
            }
    
            var center = this.currentLayer.getLatLng();
            this.map.map.panTo(center, {animate: false});
            } else {
            this.removeLatLngMakrer();
            }
        },

        displayTab: function(e) {
            e.preventDefault();
            this.$el.find('.nav-tabs>li').each(function() {
                $(this).removeClass('active in');
            });
            $(e.currentTarget).parent().addClass('active in');

            this.$el.find('.tab-content>.tab-pane').each(function() {
                $(this).removeClass('active in');
            });
            var id = $(e.currentTarget).attr('href');
            this.$el.find('.tab-content>.tab-pane' + id).addClass('active in');

            if (id === '#mapTab' && !this.map) {
                this.displayMap();
                if(this.nsForm.displayMode=='edit'){
                    this.map.enableDrawingControl();
                } else {
                    this.map.disableDrawingControl();
                }
            }
        },

        onShow: function() {
            this.displayStation();
            this.displayNavbar();
        },

        displayNavbar: function() {
            this.rgNavbar.show(this.navbarView = new NavbarView({
                parent: this
            }));
        },

        displayStation: function() {
            this.total = 0;
            var _this = this;
            var detailsFormRegion = this.$el.find('.js-rg-details');
            var formConfig = this.model.get('formConfig');

            formConfig.id = this.model.get('id');
            formConfig.formRegion = detailsFormRegion;
            formConfig.buttonRegion = [this.ui.formStationBtns];
            formConfig.afterDelete = function(response, model) {
                Backbone.history.navigate('#' + _this.model.get('type'), { trigger: true });
            };

            this.nsForm = new NsForm(formConfig);
            this.nsForm.BeforeShow = function() {
            };

            this.nsForm.afterShow = function() {
                var globalEl = $(this.BBForm.el).find('fieldset').first().detach();
                _this.ui.formStation.html(globalEl);

                if (this.displayMode.toLowerCase() == 'edit') {
                    this.bindChanges(_this.ui.formStation);
                    $(".datetime").attr('placeholder', 'DD/MM/YYYY');
                    $("#dateTimePicker").on("dp.change", function(e) {
                        $('#dateTimePicker').data("DateTimePicker").format('DD/MM/YYYY').maxDate(new Date());
                    });
                }
            };

            this.nsForm.afterSaveSuccess = function() {
                // if (_this.map) {
                //     _this.currentLayer = _this.map.addMarker(null, this.model.get('LAT'), this.model.get('LON'), _this.map.drawnItems);
                // }
                if (this.model.get('fieldActivityId') != _this.fieldActivityId) {
                    _this.displayProtos();
                    _this.fieldActivityId = _this.model.get('fieldActivityId');
                }
                _this.initMarker();
            };

            $.when(this.nsForm.jqxhr).then(function() {
                _this.fieldActivityId = this.model.get('fieldActivityId');
                _this.displayProtos();
            });

            this.nsForm.on('form_edit', function(){
                if(_this.map){
                    _this.map.enableDrawingControl();
                }
            });

            this.nsForm.on('form_display', function(){
                if(_this.map){
                    _this.map.disableDrawingControl();
                }
            });

        },

    });
});