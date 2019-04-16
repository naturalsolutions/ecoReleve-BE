define([
    'underscore',
    'backbone'
], function(
    _, Backbone
) {
    'use strict';

    return Backbone.Model.extend({
        defaults: {
            displayMap: true,

            label: 'arbres',
            single: 'arbre',
            type: 'stations',

            uiGridConfs: [{
                    name: 'details',
                    label: 'détails'
                },
                {
                    name: 'protocols',
                    label: 'Interventions'
                },
            ],

            uiTabs: [{
                    name: 'all',
                    label: 'All',
                },
                {
                    name: 'lastImported',
                    label: 'Last imported',
                }
            ],

            formConfig: {
                name: 'StaForm',
                modelurl: 'stations',
                displayMode: 'display',
                objectType: 1,
                reloadAfterSave: true,
            }
        }
    });
});