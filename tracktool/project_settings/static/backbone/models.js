var ClientModel = Backbone.Model.extend({
    initialize: function(){
    },
    urlRoot: '/api/v1/client/'
});

var Clients = Backbone.Collection.extend({
    urlRoot: '/api/v1/client/',
    model: ClientModel
});

var ClientCollection = new Clients;