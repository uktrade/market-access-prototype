define([], function() {
    return {
        urlParameters: function() {
            var sPageURL = window.location.search.substring(1),
                sURLVariables = sPageURL.split('&'),
                out = {};

            for (var i = 0; i < sURLVariables.length; i++) {
                var dec = decodeURIComponent(sURLVariables[i]);
                var split = dec.split('=');
                out[split[0]] = split[1] || '1'
            }
            return out;
        },
        hashParameters: function(vals,assign) {
            var hashParams = {};
            _.each(location.hash.replace(/^\#/,'').split('&'), function(part) {
                var pair = part.split('=');
                hashParams[pair[0]] = pair[1];
            });
            if(vals) {
                // something to update
                _.extend(hashParams, vals);
                var out = [];
                _.each(hashParams, function(value,key) {
                    if(value || value === 0) {
                        out.push(key + '=' +value);
                    }
                })
                var url = location.protocol + '//' + location.hostname + ':'+location.port+location.pathname+location.search+'#'+out.join('&');
                location[ assign ? 'assign' : 'replace'](url);
            }
            return hashParams;
        },

        unMap: function(arr) {
            // return an object from an array of name/value pairs
            var out = {};
            _.each(arr, function(obj) {
                if(_.isString(obj)) { 
                    out[obj] = true;
                } else {
                    out[obj.name] = obj.value;
                }
            })
            return out;
        },
        map: function(obj) {
            // Map an object to an array of name/value objects
            var out = [];
            _.each(obj, function(value,key) {
                out.push({name:key,value:value})
            });
            return out;
        }
    }
})