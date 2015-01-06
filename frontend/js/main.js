jQuery(document).ready(function() {

  var client = new $.es.Client({
    host: 'https://elastic.iilab.org',
    sniffOnStart: true,
    sniffInterval: 60000,
  });

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

$("#lady").select2({
    ajax: {
      url: "https://elastic.iilab.org/repositories",
      dataType: 'json',
      delay: 250,
      data: function (params) {
        return {
          q: params.term, // search term
          page: params.page
        };
      },
      processResults: function (data, params) {
        // parse the results into the format expected by Select2
        // since we are using custom formatting functions we do not need to
        // alter the remote JSON data, except to indicate that infinite
        // scrolling can be used
        params.page = params.page || 1;

        return {
          results: data.items,
          pagination: {
            more: (params.page * 30) < data.total_count
          }
        };
      },
      cache: true
    },
    minimumInputLength: 1,
    templateResult: function (repo) {
      if (repo.loading) return repo.text;

      var markup = '<div class="clearfix">' +
        '<div class="col-sm-1">' +
          '<img src="' + repo.owner.avatar_url + '" style="max-width: 100%" />' +
        '</div>' +
        '<div clas="col-sm-10">' +
          '<div class="clearfix">' +
            '<div class="col-sm-6">' + repo.full_name + '</div>' +
            '<div class="col-sm-3"><i class="fa fa-code-fork"></i> ' + repo.forks_count + '</div>' +
            '<div class="col-sm-2"><i class="fa fa-star"></i> ' + repo.stargazers_count + '</div>' +
          '</div>';

      if (repo.description) {
         markup += '<div>' + repo.description + '</div>';
      }

      markup += '</div></div>';

      return markup;
    },
    templateSelection: function (repo) {
      return repo.full_name || repo.text;
    }
});

$("#tramp").select2({
    ajax: {
      url: "https://api.github.com/search/repositories",
      dataType: 'json',
      delay: 250,
      data: function (params) {
        return {
          q: params.term, // search term
          page: params.page
        };
      },
      processResults: function (data, params) {
        // parse the results into the format expected by Select2
        // since we are using custom formatting functions we do not need to
        // alter the remote JSON data, except to indicate that infinite
        // scrolling can be used
        params.page = params.page || 1;

        return {
          results: data.items,
          pagination: {
            more: (params.page * 30) < data.total_count
          }
        };
      },
      cache: true
    },
    minimumInputLength: 1,
    templateResult: function (repo) {
      if (repo.loading) return repo.text;

      var markup = '<div class="clearfix">' +
        '<div class="col-sm-1">' +
          '<img src="' + repo.owner.avatar_url + '" style="max-width: 100%" />' +
        '</div>' +
        '<div clas="col-sm-10">' +
          '<div class="clearfix">' +
            '<div class="col-sm-6">' + repo.full_name + '</div>' +
            '<div class="col-sm-3"><i class="fa fa-code-fork"></i> ' + repo.forks_count + '</div>' +
            '<div class="col-sm-2"><i class="fa fa-star"></i> ' + repo.stargazers_count + '</div>' +
          '</div>';

      if (repo.description) {
         markup += '<div>' + repo.description + '</div>';
      }

      markup += '</div></div>';

      return markup;
    },
    templateSelection: function (repo) {
      return repo.full_name || repo.text;
    }
});

});
