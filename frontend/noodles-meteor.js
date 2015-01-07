Documents = new Mongo.Collection("documents");
  /*, {
  transform: function (doc) {
    if (doc.entities && doc.entities.length !=0) {
      doc.entities_text = doc.entities.map(function(ent) {
        return ent.display_name;
      }).join();
      //console.log(doc.entities_text)
    }
    doc.source_slug = doc.source_label.replace(/ /g,"_").toLowerCase()
    return doc;
  }
});*/

Companies = new Mongo.Collection("companies");
Sources = new Mongo.Collection("sources");

/*Documents.attachSchema(new SimpleSchema({
}));*/

Companies.attachSchema(new SimpleSchema({
  name: { 
    type: String,
    index: true,
    autoform: {
      type: "select2",
      options: function () {
        return Companies.find({}, {sort: {name: 1}, reactive:true}).map(function(itm) {return {label: itm.name, value: itm.slug};});
      },
      afFieldInput: {
        multiple: true
      }
    }
  },
  slug: {
    type: String,
    index: true,
    unique: true
  }
}));

Sources.attachSchema(new SimpleSchema({
  name: { 
    type: String,
    index: true
  },
  slug: {
    type: String,
    index: true,
    unique: true
  }
}));

Schema = {};

Schema.formSchema = new SimpleSchema({
  name: { 
    type: [String],
    index: true,
    unique: true,
    optional: true,
    autoform: {
      type: "select2",
      options: function () {
        return Companies.find({}, {sort: {name: 1}, reactive:true}).map(function(itm) {return {label: itm.name, value: itm.slug};});
      },
      afFieldInput: {
        multiple: true
      }
    }
  },
  source: {
    type: [String],
    index: true,
    unique: true,
    optional: true,
    autoform: {
      noselect: true,
      options: function () {
        var ret = {}
        Sources.find({}, {sort: {name: 1}, reactive:true}).forEach(function(itm) {
          ret[itm.slug] = itm.name
        });
        console.log(ret)
        return ret
      },
      afFieldInput: {
        multiple: true
      }
    } 
  }  
})

SimpleSchema.messages({
  notUnique: '[label] must be unique.',
});
/*
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
      //console.log(this.props.filteredSources)
      query.source_label = { $in : this.props.filteredSources };
    }

    if (this.props.filteredCountries.length > 0) {
      query.url = { $in : this.props.filteredCountries };
    }

    return query;
  }
});*/

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
//    {data: "entities_text", title: "entities_text", visible: true},
    {data: "source_label", title: "Source"},
//    {data: "source_slug", title: "source_slug"},
    {data: "url", title: "Document URL"},
    {
      tmpl: Meteor.isClient && Template.documentOpenCell
    }
  ]
});

if (Meteor.isClient) {
  // counter starts at 0
  Session.setDefault("name", []);
  Session.setDefault("source", []);
  
  Meteor.startup(function() {

    Documents.initEasySearch('title');

  })


  AutoForm.hooks({
    formSelect: {
      onSubmit: function (insertDoc, updateDoc, currentDoc) {
        if (insertDoc.name) {
          console.log(insertDoc)
          Session.set("name", insertDoc.name.map(function(val) {
            return val
          }))
        }
        if (insertDoc.source) {
          Session.set("source", insertDoc.source.map(function(val) {
            return val
          }))
        }
        this.done();
        return false;
      }
    }
  });

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

  Template.formSelectTemplate.helpers({
    facetedFormSchema: function() {
      return Schema.formSchema;
    }
  });

  Template.body.helpers({
    selector: function () {
      sel = {}
      if (Session.get("source").length != 0) {
        sel.source_slug = Session.get("source")[0]
      } 
/*      if (Session.get("name").length != 0) {
        var queryText = Session.get("name")[0]
        sel = {entities_text: { $regexp: queryText }}
      }*/
      console.log(sel)
      return sel;
//      return {title: "ANADARKO PETROLEUM CORP (0000773910) (Filer)"};
//      return {source_label: "SEC EDGAR"};
//      return {url: "http://www.sec.gov/Archives/edgar/data/773910/000119312507151814/d8k.htm"};
//      return {title: "ANADARKO PETROLEUM CORP (0000773910) (Filer)", source_label: "SEC EDGAR"}
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

    Companies.remove({});
    Sources.remove({});

    var sortedDocs = Documents.find({});
    sortedDocs.forEach(function (doc) {
      if (doc.entities) {
        doc.entities.forEach(function(entity) {
          try {
            Companies.insert({name: entity.display_name, mentions: entity.mentions, slug: entity.slug, doc_id: entity.id})
            //console.log({name: entity.display_name, mentions: entity.mentions, slug: entity.slug, doc_id: entity.id})
          } catch( e ) {
            console.log( "errorMessage", e.message );
          }
        })
      }
      if (doc.source_label) {
        try {
          console.log(doc.source_label.replace(/ /g,"_").toLowerCase())
          slug_txt = doc.source_label.replace(/ /g,"_").toLowerCase();
          if (slug_txt) {
            Sources.insert({name: doc.source_label, slug: slug_txt})
          }
        } catch( e ) {
          console.log( "errorMessage", e.message );
        }        
      }
    });
  });

  Meteor.publish("companies", function() {
    return Companies.find({}, {sort: {name: 1}}).map(function(comp) {console.log({name: comp.name});return {name: comp.name};});
  })

  Meteor.publish("sources", function() {
    return Sources.find({}, {sort: {name: 1}}).map(function(comp) {console.log({name: comp.name});return {name: comp.name};});
  })

}
