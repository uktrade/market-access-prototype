// Typeahead - using the jqueryUI autocomplete widget
define(function() {
    "use strict";
	var constructor = function(el) {
		var self = this;
		this.el = el;
        if(this.settings = settings[el.attr('data-mode')]) {
            //this.url = 'https://selling-online-overseas.export.great.gov.uk/products/api/';
            require(['jqui/widgets/autocomplete'],function(autocomplete) {
                el.autocomplete({
                    source:_.bind(search,self)
                });
            });
        } else {
            console.error('Unknown typeahead settings - "'+el.attr('data-mode')+'"');
        }
	}

    var settings = {
        productCat: {
            url: 'https://selling-online-overseas.export.great.gov.uk/products/api/',
            getParameters: function(request) {
                return {q:request.term}
            },
            processResult: function(data) {
                var result = [];
                _.each(data.categories, function(sub) {
                    _.each(sub,function(cat) {
                        result.push({label:cat,value:cat});
                    });
                });
                return result;
            }
        },
        company: {
            url: 'https://find-a-buyer.export.great.gov.uk/api/internal/companies-house-search/',
            getParameters: function(request) {
                return request
            },
            processResult: function(data) {
                var result = [];
                _.each(data, function(company) {
                    result.push({label:company.title+'\n'+company.address_snippet,value:company.title});
                });
                return result;
            }
        }
    }

    function search(request, response) {
        var settings = this.settings;
        if ( this.xhr ) {
            this.xhr.abort();
        }
        this.xhr = $.ajax({
            url: settings.url,
            data: settings.getParameters(request),
            dataType: "json",
            success: function( data ) {
                response(settings.processResult(data));
            },
            error: function() {
                response( [] );
            }
        });
    }

	return constructor;
});
