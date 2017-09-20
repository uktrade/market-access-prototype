// attach widget

define('jquery', [], function() {
    return jQuery;
});

var widgets = [
	{
		selector: '.edit-button',
		module:'EditInPlace'
	},
	{
		selector: '.expander',
		module: 'ExpandCollapse'
	},
	{
		selector: '.typeahead',
		module: 'Typeahead'
	},
	{
		selector: '.file-upload',
		module: 'Upload'
	},
	{
		selector: '.widget-date',
		module: 'Date'
	},
	{
		selector: '[data-revealedby]',
		module: 'Reveal'
	},
	{	selector:'.type-blockrepeat',
		module: 'Repeat' 
	}
];

$(function() {
	requirejs.config({
	    baseUrl: dit.jsBase,
	    paths: {
	        widgets: 'widgets',
	        vendor: 'vendor',
	       	jqui: 'vendor/ui',
	       	modules:'modules'
	    }
	});
	_.each(widgets, function(widget) {
		$(document.body).find(widget.selector).each(function(idx) {
			var el = this;
			if(!el[widget.module]) {
				el[widget.module] = 1;
				require(['widgets/'+widget.module], function(module) {
					el[widget.module] = new module($(el)) || true;
				});
			}
		});
	});

	// Load the form builder
	require(['modules/helpers'],function(helpers) {
		if(helpers.urlParameters().config) {
			localStorage.config = helpers.urlParameters().config;
		}

		if(localStorage.config == 'on') {
			require(['modules/formBuilder'], function(formBuilder) {
			})
		}
	})
/*
	var tpText = _.template('<label><%=title%></label><input type="text" name="<%=field%>" value="<%=obj[field]%>">');
	var tpArea = _.template('<label><%=title%></label><textarea name="<%=field%>"><%=obj[field]%></textarea>');

	var tpRo = _.template('<label><%=title%></label><span><%=obj[field]%></span>');

	var tp = _.template('\
		<div><%= tpText({title:"Order",field:"order",obj:obj}) %></div>\
		<div><%= tpText({title:"Field name",field:"fieldName",obj:obj}) %></div>\
		<div><%= tpArea({title:"Label",field:"label",obj:obj}) %></div>\
		<div><%= tpArea({title:"Hint",field:"hint",obj:obj}) %></div>\
		<div><%= tpText({title:"Field type",field:"fieldType",obj:obj}) %></div>\
		<div><%= tpText({title:"Option group",field:"optionGroup",obj:obj}) %></div>\
		<div><%= tpArea({title:"Options",field:"options",obj:obj}) %></div>\
		<div><%= tpRo({title:"Section",field:"section_id",obj:obj}) %></div>');

	function editQuestion(question, details) {
		require(['modules/Lightbox'], function(Lightbox) {
			var lightbox = new Lightbox({title:'Edit Question', message:"Name : "+name});
			var container = lightbox.getContainer();
			var out = [];
			out.push(tp({obj:question,tpRo:tpRo,tpText:tpText,tpArea:tpArea}));
			container.find('.outer .outer').html('<form>'+out.join('')+'</form>');
			container.find('button[value=ok]').on('click', function() {
				// save the result
				var update = container.find('form').serializeArray();
				update.push({name:'csrfmiddlewaretoken', value:details.token});
				update.push({name:'questionnaire', value:details.questionnaireId});
				update.push({name:'page', value:details.page});
				update.push({name:'oldFieldName', value:details.fieldName || ''});
				$.ajax({
				  method: 'post',
				  dataType: "json",
				  url:'/formbuilder/question',
				  data: update
			  })
			})
		})
	}
	
	// form editor
	var editEnabled = false;
	$(document.body).on('click', function(evt) {
		if(editEnabled) {
			editEnabled = false;
			var form = $(evt.target).closest('form.dd-form');
			if(form.length) {
				// get things from the form
				var container = $(evt.target).closest('.form-group');  // if we are editing
				var details = {
					token: form.find('input[name=csrfmiddlewaretoken]').val(),
					questionnaireId: form.find('input[name=questionnaire]').val(),
					page: form.find('input[name=page]').val(),
					fieldName: container.attr('data-fieldName')
				};
				if(details.fieldName) {
					$.ajax({
					  dataType: "json",
					  url:'/formbuilder/question' ,
					  data: {
					  	questionnaire:details.questionnaireId,
					  	fieldName:details.fieldName,
					  	page:details.page
					  }
					}).then(
						function(questions) {
							editQuestion(questions[0],details)
						}
					)
				} else {
					// Create a new question
					editQuestion({},details);
				}
			}
		}
	})
	$(document.body).on('keydown',function(evt) {
		if(evt.which == 88 && evt.altKey) {
			editEnabled = true;
		}
	})
	$(document.body).on('keyup',function() {
		editEnabled = false;
	}); */
});

