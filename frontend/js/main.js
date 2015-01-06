jQuery(document).ready(function() {

  $('.facet-view-simple').facetview({
    search_url: 'https://elastic.iilab.org/noodles/document/_search?',
    search_index: 'noodles',
    datatype: 'json',
    facets: [
        {'field': 'source.source_label', 'size': 100, 'order':'term', 'display': 'publisher'},
    ],
    paging: {
      size: 10
    }
  });

});
