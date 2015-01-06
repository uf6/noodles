jQuery(document).ready(function() {

  $('.facet-view-simple').facetview({
    search_url: 'https://elastic.iilab.org/noodles/document/_search?',
    search_index: 'noodles',
    datatype: 'json',
    facets: [
        {'field': 'source_label', 'display': 'source_label'},
    ],
    paging: {
      size: 10
    }
  });

});
