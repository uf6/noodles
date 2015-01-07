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
    type: String,
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
        return ret
      },
      afFieldInput: {
//        multiple: true
      }
    } 
  }  
})

SimpleSchema.messages({
  notUnique: '[label] must be unique.',
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
//    {data: "entities_text", title: "entities_text", visible: true},
    {data: "source_label", title: "Source"},
//    {data: "source_slug", title: "source_slug"},
    {data: "url", title: "Document URL"},
    {
      tmpl: Meteor.isClient && Template.documentOpenCell
    }
  ],
  bFilter: false,

});

if (Meteor.isClient) {
  // counter starts at 0
  Session.setDefault("name", []);
  Session.setDefault("source", "");
  
  Meteor.startup(function() {

    Documents.initEasySearch('title');

  })

/*
/ Submission hooks and events for the autoform 
/**/

  AutoForm.hooks({
    formSelect: {
      onSubmit: function (insertDoc, updateDoc, currentDoc) {
        if (insertDoc.name) {
          entities_array = []
          entities_array = Session.get("name")
          console.log('docname')
          console.log(insertDoc.name)
          insertDoc.name.forEach(function(val) {
            entities_array.push({entities_text: { '$regex' : val }})            
          })
          console.log('started@!')
          console.log(entities_array)
          Session.set("name", entities_array)
          console.log(entities_array)
          console.log('went through!')
        }
        if (insertDoc.source) {
          Session.set("source", insertDoc.source)
        }
        this.done();
        return false;
      }
    }
  });

  Template.formSelectTemplate.events({  
      'click button.reset': function () {
        this.name = []
        this.source = "";
        Session.set("name", []); 
        Session.set("source", "");
        return false;
      }
  });

  Template.body.created = function () {
    //
  };

  Template.formSelectTemplate.helpers({
    facetedFormSchema: function() {
      return Schema.formSchema;
    },
    currentCompanyValue: function() {
      console.log(Session.get("name"))
      return Session.get("name")
    },
    currentSourceValue: function() {
      return Session.get("source")
    }
  });

  Template.body.helpers({
    selector: function () {
      sel = {}
      if (Session.get("source")) {
        sel.source_slug = Session.get("source")
      } 
//      if (Session.get("coutry").length != 0) {
//        sel.$and = Session.get("country")
//      } 
      if (Session.get("name").length != 0) {
        sel.$and = Session.get("name")
      }
//      sel = {title: "ANADARKO PETROLEUM CORP (0000773910) (Filer)"};
//      sel = {entities_text: "ANADARKO PETROLEUM CORP"}
//      sel = {source_label: "SEC EDGAR"};
//      sel = {url: "http://www.sec.gov/Archives/edgar/data/773910/000119312507151814/d8k.htm"};

      console.log(sel)
      return sel;
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
