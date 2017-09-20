define(['modules/helpers'], function(helpers) {

	var tpText = _.template('<label><%=title%></label><input type="text" name="<%=field%>" value="<%=obj[field]%>">');
	var tpArea = _.template('<label><%=title%></label><textarea name="<%=field%>"><%=obj[field]%></textarea>');
	var tpSelect = _.template('<label><%=title%></label><select name="<%=field%>" value="<%=obj[field]%>">\
		<option value="label" <% if(obj[field]=="label") { %> selected<%}%> >Label</option>\
		<option value="text" <% if(obj[field]=="text") { %> selected<%}%> >Text box</option>\
		<option value="textArea" <% if(obj[field]=="textArea") { %> selected<%}%> >Text area</option>\
		<option value="checkset" <% if(obj[field]=="checkset") { %> selected<%}%> >Checkboxes</option>\
		<option value="radioset" <% if(obj[field]=="radioset") { %> selected<%}%> >Radio buttons</option>\
		<option value="fileupload" <% if(obj[field]=="fileupload") { %> selected<%}%> >File upload(bucket)</option>\
		<option value="fileuploadtemplate" <% if(obj[field]=="fileuploadtemplate") { %> selected<%}%> >File upload(template)</option>\
		<option value="date" <% if(obj[field]=="date") { %> selected<%}%> >Date</option>\
		<option value="typeahead" <% if(obj[field]=="typeahead") { %> selected<%}%> >Type-ahead</option>\
		<option value="table" <% if(obj[field]=="table") { %> selected<%}%> >Table(template)</option>\
		<option value="blockrepeat" <% if(obj[field]=="blockrepeat") { %> selected<%}%> >Block Repeat</option>\
		</select>');

	var tpRo = _.template('<label><%=title%></label><span><%=obj[field]%></span>');

	var tp = _.template('\
		<form>\
		<div><%= tpText({title:"Order",field:"order",obj:obj}) %></div>\
		<div><%= tpText({title:"Field name",field:"fieldName",obj:obj}) %></div>\
		<div><%= tpArea({title:"Label",field:"label",obj:obj}) %></div>\
		<div><%= tpArea({title:"Hint",field:"hint",obj:obj}) %></div>\
		<div><%= tpSelect({title:"Field type",field:"fieldType",obj:obj}) %></div>\
		<div><%= tpText({title:"Option group",field:"optionGroup",obj:obj}) %></div>\
		<div><%= tpArea({title:"Options",field:"options",obj:obj}) %></div>\
		<div><button type="button" class="button dlg-close" value="cut">Cut to clipboard</button></div>\
		</form>');
		//<div><%= tpRo({title:"Section",field:"section_id",obj:obj}) %></div>');


	var pageTemplate = _.template('\
		<form>\
		<div><%= tpText({title:"Page Title",field:"title",obj:obj}) %></div>\
		</form>\
	')

	var form = $('form.dd-form');

	function createPage(page,details) {
		require(['modules/Lightbox'], function(Lightbox) {
			var lightbox = new Lightbox({title:'Create Page',message:''});
			var container = lightbox.getContainer();
			container.find('.outer .outer').html(pageTemplate({obj:page,tpRo:tpRo,tpText:tpText,tpArea:tpArea,tpSelect:tpSelect}));
			container.find('button[value=ok]').on('click', function() {
				var update = _.extend(helpers.unMap(container.find('form').serializeArray()),details);
				$.ajax({
				  method: 'post',
				  dataType: "json",
				  url:'/formbuilder/page',
				  data: helpers.map(update)
			  	})			
			});
		});
	}

	function clipboard(details, action) {
		details.action = action;
		$.ajax({
		  method: 'post',
		  url:'/formbuilder/page',
		  data: helpers.map(details)
	  	}).then(function(content) {
	  		window.location.reload()
	  	})
	}

	function editQuestionFull(question, details, questionContainer) {
		require(['modules/Lightbox'], function(Lightbox) {
			details.oldFieldName = questionContainer && questionContainer.attr('data-fieldName') || '';
			var lightbox = new Lightbox({title:'Edit Question', message:"Name : "+name});
			var container = lightbox.getContainer();
			container.find('.outer .outer').html(tp({obj:question,tpRo:tpRo,tpText:tpText,tpArea:tpArea,tpSelect:tpSelect}));
			container.find('button[value=ok]').on('click', function() {
				// save the result
				details = _.extend(details,helpers.unMap(container.find('form').serializeArray()));
				$.ajax({
				  method: 'post',
				  url:'/formbuilder/question',
				  data: helpers.map(details)
			  	}).then(function(content) {
			  		location.reload();
			  		//questionContainer.html($(content).html());
			  	})
			})
			container.find('button[value=cut]').on('click', function() {
				// move to clipboard
				details.action = 'cut';
				$.ajax({
				  method: 'post',
				  url:'/formbuilder/question',
				  data: helpers.map(details)
				}).then(function(content) {
					location.reload();
			  		//questionContainer.html($(content).html());
			  	})
			})
		})
	}

	function getDetails() {
		return {
			'csrfmiddlewaretoken': form.find('input[name=csrfmiddlewaretoken]').val(),
			'instance': form.find('input[name=instance]').val(),
			'page': form.find('input[name=page]').val()
		}
	}

	function editQuestion(container) {
		//var form = $(container).closest('form.dd-form');
		// get things from the form
		//var container = $(evt.target).closest('.form-group');  // if we are editing
		var details = getDetails();
		var fieldName = container && container.attr('data-fieldName');
		if(fieldName) {
			details.fieldName = fieldName;
			$.ajax({
			  dataType: "json",
			  url:'/formbuilder/question' ,
			  data: helpers.map(details)
			}).then(
				function(questions) {
					editQuestionFull(questions[0],details,container)
				}
			)
		} else {
			// Create a new question
			editQuestionFull({},details,container);
		}
	}
	
	// form editor
	var editEnabled = false;
	$(document.body).on('click', function(evt) {
		if(editEnabled) {
			editEnabled = false;
			var questionContainer = $(evt.target).closest('.form-group');
			if(questionContainer) {
				editQuestion(questionContainer);
			}
		}
	});

	function onClick(evt) {
		var target = $(evt.target);
		if(highlightedQuestion && target.hasClass('question-edit-block')) {
			evt.preventDefault();
			evt.stopImmediatePropagation();
			editQuestion($(highlightedQuestion));
		}
		if(target.hasClass('new-question')) {
			editQuestion();
		}
		if(target.hasClass('new-page')) {
			createPage({},getDetails());
		}
		if(target.hasClass('paste')) {
			clipboard(getDetails(),'paste');
		}
		if(target.hasClass('empty-clip')) {
			clipboard(getDetails(),'empty-clip');
		}
	}

	var highlightedQuestion;

	var editBlock = $('<img class="question-edit-block">');

	function editHover(evt) {
		var target = $(evt.target);
		var question = target.closest('.form-group');
		if(question[0] != highlightedQuestion) {
			if(highlightedQuestion) {
				$(highlightedQuestion).removeClass('highlight');
				editBlock.remove();
			}
			highlightedQuestion = question[0];
			question.addClass('highlight');
			question.append(editBlock);
		}
	};

	function navClick(evt) {
		var target = $(evt.target).closest('li');
		if(target.length) {
			evt.preventDefault();
			evt.stopPropagation();
			var data = getDetails();
			data.page = parseInt(target.attr('data-page'),10);
			$.ajax({
				method: 'get',
				dataType: "json",
				url:'/formbuilder/page',
				data: helpers.map(data)
			}).then(function(content) {

			})
		}
	}

	function initialize() {
		/* form.find('.form-group').each(function() {
			$(this).append($('<img class="form-edit icon icon-pen">'));
		});*/
		var tp = _.template('\
			<div class="config-menu">\
				<button type="button" class="new-question button">New question</button>\
				<button type="button" class="new-page button">New page</buton>\
				<button type="button" class="paste button">Paste</buton>\
				<button type="button" class="empty-clip button">Empty clipboard</buton>\
			</div>\
		');
		$('#global-header').append($(tp()));
		$('#global-header').append($('<img class="threeline-menu">'));
		$(document.body).on('click',onClick);
		$(document.body).on('mouseover', editHover);

		//$('ul.nav').on('click', navClick);
	}

	/* function keyDown(evt) {
		if(evt.which == 88 && evt.altKey) {
			initialize();
			$(document.body).off('keydown',keyDown);
		}
	}		
	$(document.body).on('keydown',keyDown ) */
	initialize();
});
