var ClientListItem = Backbone.View.extend({

    tagName: 'li',
    className: 'list-group-item',

    initialize: function(model, options) {
        this.options = options
    },

    events: {},

    template: _.template('<%- name %>'),

    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }
});

EXAMPLE.VIEWS.ClientListView = Backbone.View.extend({

    el: '#my-model-list',

    initialize: function(options){
        this.listenTo(ClientCollection, 'reset', this.addAll, this);
    },

    addOne: function(model){
        var view = new ClientListItem({model:model});
        console.log(view.render().el);
        this.$el.append(view.render().el)
    },

    addAll: function(){
        var that = this;
        ClientCollection.each(function(model){
            that.addOne(model);
        })
    },

    render: function (){
        this.$el.html(this.template());
        return this;
    }
});