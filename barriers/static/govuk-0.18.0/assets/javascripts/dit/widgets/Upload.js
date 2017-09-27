// widget to upload a file
define(function() {
    "use strict";
	var constructor = function(el) {
		var self = this;
		this.el = el;
		el.on('change',function(evt){onChange.call(self,evt)});
		el.on('click',function(evt){trigger.call(self,evt)});
        this.container = el.closest('.form-group');
        this.container.on('click',_.bind(onClick,this));
        this.updateFileTable = _.bind(updateFileTable,this);
	}

	function trigger(evt) {
		var self = this;
		this.form = $('<form><input type="file" name="file" multiple="multiple"></form>');
		this.form.find('input').trigger('click').on('change',function(evt){onChange.call(self,evt)});
	}

    function getDetails() {
        var outerForm = $('form.dd-form');
        return {
            csrfmiddlewaretoken: outerForm.find('input[name=csrfmiddlewaretoken]').val(),
            instance: outerForm.find('input[name=instance]').val(),
            page: outerForm.find('input[name=page]').val(),
            fieldName: this.container.attr('data-fieldname')
        }
    }

    function updateFileTable(content) {
        var newEl = $(content);
        var old = this.container.find('table.file-list');
        old.after(newEl.find('table.file-list'));
        old.remove();
    }

    // Click on a delete icon
    function onClick(evt) {
        var aTag = $(evt.target).closest('a.file-delete');
        var fileId = aTag.attr('data-fileid');
        if(fileId) {
            evt.preventDefault();
            var details = getDetails.call(this);
            details.fileId = fileId;
            details.action = 'delete';
            var data = [];
            _.each(details,function(value, key) {
                data.push({name:key, value:value});
            })
            $.ajax({
                url: 'file',
                type: 'POST',
                data: data
            }).then(this.updateFileTable)
        }
    }

	function onChange(evt) {
		// var crsfToken = this.el.attr('data-csrfToken');  // for the django anti X site hoisting attack
        var self = this;
        var details = getDetails.call(this);
        _.each(details, function(value,key) {
            self.form.append($('<input type="hidden" name="'+key+'" value="'+value+'">'));
        });

		var data = new FormData(this.form[0]);

        var progress = $('<div class="progress"><div></div></div>');
        this.container.find('table.file-list').after(progress);
        $.ajax({
            url: 'file',
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,

            xhr: function() {
                var myXhr = $.ajaxSettings.xhr();
                if (myXhr.upload) {
                    // For handling the progress of the upload
                    myXhr.upload.addEventListener('progress', function(e) {
                        if (e.lengthComputable) {
                            var pc = Math.floor((e.loaded/e.total)*100);
                            progress.find('div').css({width:pc+'%'});
                        }  /*if(e.loaded >= e.total) {
                            setTimeout(function() {  // a delay after loading completed before removing the upload bar
                                progress.remove();
                            },300);
                        } */
                    } , false);
                }
                return myXhr;
            },
        }).then( function(content) {
                self.updateFileTable(content);
                progress.remove();
            }
        );
	}
	return constructor;
});
