define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'ns_map/ns_map',
    'modules/objects/object.new.view',
    './project.model',
], function(
    $, _, Backbone, Marionette, NsMap,
    NewView, ProjectModel
) {

    'use strict';
    return NewView.extend({

        ModelPrototype: ProjectModel,
        template: 'app/modules/projects/project.new.tpl.html',
        className: 'full-height white',

        onShow: function() {
            this.displayForm();
            this.displayMap();
            var _this = this;
            this.$el.i18n();
        },

        displayMap: function(geoJson) {
            var self = this;
            this.map = new NsMap({
                //url: 'projects/' + this.model.get('id')  + '/stations?geo=true', ////only this one
                zoom: 4,
                element: 'map',
                popup: true,
                // cluster: true,
                disableCentering: true,
                drawable: true,
            });

            //center map on France
            this.map.map.fitBounds([
                [41.959891, -4.077587],
                [51.276321, 8.698981]
            ])

            this.map.map.on('draw:created', function(e) {
                var type = e.layerType;
                self.currentLayer = e.layer;
                // var latlon = self.currentLayer.getLatLng();

                self.map.drawnItems.addLayer(self.currentLayer);
                if (self.map.getGeometry().features.length > 0) {
                    var geom = self.map.getGeometry().features[0];
                } else {
                    var geom = null;
                }
                self.nsForm.model.set('geom', geom);
                // self.$el.find('input[name="LAT"]').val(latlon.lat);
                // self.$el.find('input[name="LON"]').val(latlon.lng);
                self.map.toggleDrawing();
            });


            // this.map.map.on('draw:edited', function (e) {
            //   // var latlon = self.currentLayer.getLatLng();
            //   // self.$el.find('input[name="LAT"]').val(latlon.lat);
            //   // self.$el.find('input[name="LON"]').val(latlon.lng);
            // });

            this.map.map.on('draw:deleted', function() {
                self.map.toggleDrawing();
            });

        },

        afterShow: function() {
            var _this = this;
            $.when(this.nsForm.jqxhr).done(function(data) {
                var geom = data.data.geom;
                if (_this.map.drawnItems) {
                    _this.map.drawnItems.clearLayers();
                }
                if (geom) {
                    _this.map.addGeometry(geom, true);
                }
            });


            this.nsForm.butClickSave = function(e) {
                var geom;
                if (_this.map.getGeometry().features.length > 0) {
                    geom = _this.map.getGeometry().features[0];
                } else {
                    geom = null;
                }
                _this.nsForm.model.set('geom', geom);
                NsForm.prototype.butClickSave.call(this, e);
            }
        },
    });
});