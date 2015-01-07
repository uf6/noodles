Documents = new Mongo.Collection("documents");

Companies = new Mongo.Collection("companies");

Documents.attachSchema(new SimpleSchema({
}));

Companies.attachSchema(new SimpleSchema({
  name: { 
    type: String,
    index: true,
    unique: true,
    autoform: {
      type: "select2",
      options: function () {
        return Companies.find({}, {sort: {name: 1}, reactive:true}).map(function(itm) {return {label: itm.name, value: itm.slug};});
      },
      afFieldInput: {
        multiple: true
      }
    }
  }
}));

SimpleSchema.messages({
  notUnique: '[label] must be unique.',
});

EasySearch.createSearchIndex('documents', {
  'field' : ['entities'],
  'collection' : Documents.find().map(function(doc) {return doc}),
  'limit' : 20,
  'props' : {
    'filteredSources' : [],
    'filteredCountries' : [],
  },
  'query' : function (searchString) {
    // Default query that will be used for searching
    var query = EasySearch.getSearcher(this.use).defaultQuery(this, searchString);

    // filter for categories if set
    if (this.props.filteredSources.length > 0) {
      console.log(this.props.filteredSources)
      query.source_label = { $in : this.props.filteredSources };
    }

    if (this.props.filteredCountries.length > 0) {
      query.url = { $in : this.props.filteredCountries };
    }

    return query;
  }
});

TabularTables = {};

Meteor.isClient && Template.registerHelper('TabularTables', TabularTables);

TabularTables.Documents = new Tabular.Table({
  name: "DocumentList",
  collection: Documents,
  columns: [
    {data: "title", title: "Title"},
    {
      data: "entities",
      title: "Entities",
      render: function (val, type, doc) {
        return ramda.map(function(entity) {
                  return entity.display_name; 
                },val);     
      }
    },
    {data: "source_label", title: "Source"},
    {data: "url", title: "Document URL"},
    {
      tmpl: Meteor.isClient && Template.documentOpenCell
    }
  ]
});

if (Meteor.isClient) {
  // counter starts at 0
  Session.setDefault("entity_selector", []);
  
  Meteor.subscribe("parties");

  Meteor.startup(function() {

    Documents.initEasySearch('title');

  })

  AutoForm.hooks({
    formSelect: {
      after: {
        update: function(err,result,template) {
          console.log(result)
        }
      }
    }
  })

  Template.body.created = function () {
    // set up reactive computation

    this.autorun(function () {
      var instance = EasySearch.getComponentInstance(
          { index : 'documents' }
      );

      instance.on('autosuggestSelected', function (values) {
        // run every time the autosuggest selection changes
        if (values && values.length) {
          entity_selector = Session.get("entity_selector")
          Session.set("entity_selector", values.map(function(val) {
            return {title: val.value}
          }))
        }
      });
    });
  };

  Template.sources_filter.events({
    'change select' : function (e) {
      var instance = EasySearch.getComponentInstance(
        { index : 'documents' }
      );

      // Change the currently filteredCategories like this
      console.log($(e.target).val())
      EasySearch.changeProperty('documents', 'filteredSources', $(e.target).val());
      // Trigger the search again, to reload the new products
        entity_selector = Session.get("entity_selector")
        console.log({source_label: $(e.target).val()})
        source_filter_value = {source_label: $(e.target).val()}
        entity_selector.push(source_filter_value)
        console.log(entity_selector)
        Session.set("entity_selector", entity_selector)
    }
  });

  Template.countries_filter.events({
    'change select' : function (e) {
      var instance = EasySearch.getComponentInstance(
        { index : 'documents' }
      );

      // Change the currently filteredCategories like this
      EasySearch.changeProperty('documents', 'filteredCountries', $(e.target).val());
      // Trigger the search again, to reload the new products
      instance.triggerSearch();
    }
  });

  Template.body.helpers({
    selector: function () {
      if (Session.get("entity_selector").length == 0) {
        sel = {}
      } else {
        sel = {$and: Session.get("entity_selector")}
      }
      console.log(sel)
      return sel;
//      return {author: "Agatha Christie"};
    },
    documents: function () {
      return Documents.find({});
    },
    'suggestion' : function () {
     return Template.suggestionTpl;
    }
  });

  Template.documentOpenCell.events({
    'click .open': function () {
      console.log(this._id);
    }
  });

}

if (Meteor.isServer) {
  Meteor.startup(function () {
    // code to run on server at startup
    var sortedDocs = Documents.find({});
    sortedDocs.forEach(function (doc) {
      if (doc.entities) {
        doc.entities.forEach(function(entity) {
          try {
            Companies.insert({name: entity.display_name, mentions: entity.mentions, slug: entity.slug, doc_id: entity.id})
            console.log({name: entity.display_name, mentions: entity.mentions, slug: entity.slug, doc_id: entity.id})
          } catch( e ) {
            console.log( "errorMessage", e.message );
          }
        })
      }
    });
  });

  Meteor.publish("companies", function() {
    return Companies.find({}, {sort: {name: 1}}).map(function(comp) {console.log({name: comp.name});return {name: comp.name};});
  })
}
