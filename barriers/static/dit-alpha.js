var ukti = window.ukti || {};

ukti.SearchFilters = (function() {
  'use strict';

	var _parentEl;
	var _openClass = 'filters-open';
	var _hiddenClass = 'hidden';
  var _togglerParentSelector = '.filters__item__last';
  var _toggleGroup;
  var _toggleGroupSelector = '.filters__groupB';
  var _filterOpenField;
  var _filterOpenFieldSelector = 'input[name$="filterOpen"]';

  var hideFilters = function () {
  	_parentEl.classList.remove(_openClass);
  	_toggleGroup.classList.add(_hiddenClass);
  	_toggleGroup.setAttribute('aria-hidden', 'true');
    setFilterOpenField (false);
  };

  var showFilters = function () {
		_parentEl.classList.add(_openClass);
		_toggleGroup.classList.remove(_hiddenClass);
    setFilterOpenField(true);
  };

  var returnToggler = function() {
		var toggler = document.createElement('a');
		toggler.classList.add('js-toggler');
		toggler.setAttribute('href', '#');
		toggler.setAttribute('aria-label', 'Filters');
		toggler.setAttribute('aria-controls', 'js-toggler');
		toggler.innerHTML = '<span class="close">Fewer filters</span><span class="open">More filters</span>';
		return toggler;
  };

  var addToggler = function() {
  	var toggler = returnToggler();
  	var togglerParent = _parentEl.querySelector(_togglerParentSelector);
  	toggler.addEventListener('click', function (event) {
  		event.preventDefault();
			toggleFilters();
  	}, false);
  	togglerParent.insertBefore(toggler, togglerParent.firstChild);
  };

  var toggleFilters = function (event) {
		if (_parentEl.classList.contains(_openClass)) {
			hideFilters();
		} else {
			showFilters();
		}
  };

  var setFilterOpenField = function (value) {
    _filterOpenField.value = value;
  };

  var returnFilterOpenFieldValue = function () {
    return _filterOpenField.value;
  };

  var checkHiddenFormField = function () {
    if (returnFilterOpenFieldValue() == 'false' || returnFilterOpenFieldValue() === '') {
      hideFilters();
    }
  };

  var initToggleFilters = function (el) {
    _parentEl = el;
    _toggleGroup = _parentEl.querySelector(_toggleGroupSelector);
    _filterOpenField = _parentEl.querySelector(_filterOpenFieldSelector);
    addToggler();
    checkHiddenFormField();
  };

  var init = function (el) {
		initToggleFilters(el);
  };

  return {
    init: init
  };

})();

var ukti = window.ukti || {};

ukti.ResultsOrder = (function() {
  'use strict';

	var changeHandler = function(event) {
		event.currentTarget.form.submit();
	};

	var attachBehaviour = function (el) {
		var radios = el.querySelectorAll('input[name="sort_column_name"]');
		for ( var i = 0; i < radios.length; i++ ) {
			radios[i].addEventListener('change', changeHandler);
		}
	};

  var init = function (el) {
		attachBehaviour(el);
  };

  return {
    init: init
  };

})();
var ukti = window.ukti || {};

ukti.ScrollTo = (function($) {
  'use strict';

  var initScrollIntoView = function (selector) {
    var el = document.querySelector(selector);
    if (el) {
      document.querySelector(selector).scrollIntoView({
        behavior: 'smooth'
      });
    }
  };

  var init = function (selector) {
		initScrollIntoView(selector);
  };

  return {
    init: init
  };

})();

// Custom checkboxes
var selectCustom = $('.select-custom');
if (selectCustom.length) {

  selectCustom.addClass('select2-hidden-accessible');
  selectCustom.attr('aria-hidden', 'true');

	selectCustom.select2({
		theme: 'flat',
		escapeMarkup: function(markup) {
		  return markup;
		},
		templateResult: function(result) {
			return '<svg class="icon icon-check"><use xlink:href="#icon-ditcheckmark" /></svg>' + result.text;
    	}
	});

	/* prevent dropdown from opening when deselecting tag */
	/* and clear label when deselecting - particularly with backspace */
	selectCustom.on('select2:unselect', function() {
		$el = $(this);
		$el.data('unselecting', true);
		setTimeout(function() {
			$el.parent().find('.select2-search__field').val('');
		}, 0);
	});

	selectCustom.on('select2:opening', function(e) {
		$el = $(this);
		if ( $el.data('unselecting') ) {
        	$el.removeData('unselecting');
        	e.preventDefault();
		}
	});
}


// Quick and simple function to stop Firefox from remembering checkbox/radio buttons after a refresh
// because for alpha we do not need that
$(document).ready(function(){
  $(':radio:checked').prop('checked', false);
  $(':checkbox:checked').prop('checked', false);
});

// Quick and simple toggle to show/hide the advanced filters
$(document).ready(function(){

  var $button = $('.js-dit-toggle-filters');
  var $filters = $('.dit-input-field--advanced');

  $button.on('click', function(){
    if($button.attr('aria-pressed') == 'false'){
      $('.dit-input-field--advanced[aria-hidden="true"]').attr('aria-hidden', 'false');
      $button.attr('aria-pressed', 'true');
      $button.find('.open').attr('aria-hidden', 'true');
      $button.find('.close').attr('aria-hidden', 'false');
    } else {
      $('.dit-input-field--advanced[aria-hidden="false"]').attr('aria-hidden', 'true');
      $button.attr('aria-pressed', 'false');
      $button.find('.open').attr('aria-hidden', 'false');
      $button.find('.close').attr('aria-hidden', 'true');
    }
  });

});

// Quick and simple toggle to show/hide the companies house list
$(document).ready(function(){
  var $button = $('.js-companies-house');
  var buttonCopy = $button.html();
  var $input = $('.js-companies-house-input');
  var $list = $('.js-companies-house-list');
  var $callback = $('.js-companies-house-callback');
  var $templateError = $('.js-companies-house-template-error');
  var $templateFail = $('.js-companies-house-template-fail');
  var $countFeedback = $('.js-companies-count-feedback');
  var $templateCountFeedback = $('.js-companies-house-template-count-feedback');
  var resultsHTML = '';
  var countFeedbackHTML = '';
  var AJAX_URL = '/api/companieshouse?company=';
  var perPage = 20;
  var activeCompanies = [];

  $button.on('click', function(){

    if($input.val().length === 0){
      // User has clicked the button but not entered any search keywords so display the error
      $button.closest('.form-group').addClass('form-group-error');
      $button.closest('.form-group').find('.error-message').removeClass('hidden').attr('aria-hidden', 'false');

      // Unpress the button for ARIA... Question: should we do this?
      $button.attr('aria-expanded', 'false');

      // Hide the old list of results (if visible)
      $list.attr('aria-hidden', 'true');
      $list.addClass('hidden');

      // The radio buttons in the list of companies are no longer `required`
      // if there is no company name (othewrwise users will get confused to see an error referencing seemingly invisible fields)
      $list.find('input').removeAttr('required');
    } else if($input.val().length > 0){
      $button.html($button.data('copy-loading'));
      // Remove any errors from the field and hide any existing results
      $button.closest('.form-group').removeClass('form-group-error');
      $button.closest('.form-group').find('.error-message').addClass('hidden').attr('aria-hidden', 'true');

      // Tell ARIA that the results container is now open
      $button.attr('aria-expanded', 'true');

      // Show a loading indicator
      $callback.html('Contacting Companies House. Please wait...');

      // Show the results
      $list.attr('aria-hidden', 'false');
      $list.removeClass('hidden');
      $list.find('input').attr('required', 'required');

      // Hide the count feedback e.g. `Showing x results of Y`
      $countFeedback.attr('aria-hidden', 'true');
      $countFeedback.addClass('hidden');

      console.log($input.val());

      // Fetch JSON results from API/this app
      $.ajax({
        url: AJAX_URL + $input.val(),
        context: document.body,
        data: {}
      }).fail(function(jqXHR) {
        // If we fail feedback to the user what they can do
        // As this is only an alpha this is not so important but really we need
        // a fallback in case the API fails for whatever reason
        $callback.html($templateFail.html());
      })
      .always(function() {
        $button.html(buttonCopy);
      })
      .done(function(json) {

        // Build up the HTML
        resultsHTML = '';
        activeCompanies = [];

        // strip out non-active companies
        if(json && json.total_results > 0){
          json.items.forEach(function(company) {
            if(company.company_status == 'active'){
              activeCompanies.push(company);
            }
          });
        }

        if(activeCompanies.length > 0){
          activeCompanies.forEach(function(company) {
            resultsHTML = resultsHTML + convertJSONToHTML(company);
          });
        } else {
          resultsHTML = $templateError.html();
        }

        // Populate results either with a list of companies OR an error message
        // Temporarily delay the response until we have AJAX in place i.e. FAKE IT for user testing
        $callback.html(resultsHTML);

        $list.find('input:first').focus();

        // Display our count feedback e.g. `Showing x results of y`
        if(activeCompanies.length > 0){
          $countFeedback.attr('aria-hidden', 'false');
          $countFeedback.removeClass('hidden');
          $countFeedback.html($templateCountFeedback.html().replace('{COUNT}', numberWithCommas(json.total_results)));
        }

      });

    }
  });

  /**
   * convertJSONToHTML
   * Take an on-page HTML template and convert our JSON to it
   * @param {string} JSON - our JSON object (just one object in the array of items)
   *
   * @return {string}
   */
  function convertJSONToHTML(json){

    /**
     * @param {object}
     */
    var $template = $('.js-companies-house-template');

    /**
     * @param {string}
     */
    var x = $template.html();

    x = x.replace(/\{NAME\}/g, json.title);
    x = x.replace(/\{NUMBER\}/g, json.company_number);
    x = x.replace(/\{ADDRESS\}/g, json.address_snippet);
    x = x.replace(/\{DESCRIPTION\}/g, json.description);

    return x;
  }

  /**
   * numberWithCommas
   * Take a number like 1000000 and return 1,000,000
   * @seee https://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
   * @param {int} x - the number
   *
   * @return {string}
   */
  function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }
});


// Quick and simple toggle to show/hide the companies house list
$(document).ready(function(){

  // Loop through all checkboxes and assign click events to them and their
  // related other checkboxes/radios
  function init(){
    $('.js-dit-toggle-field').each(function(){
      var $checkbox = $(this);
      var $checkboxes = $('[name="' + $checkbox.attr('name') + '"]');

      // Set event listener
      $checkboxes.on('change', function(){
        toggle($checkbox);
      });

    });
  }

  // If active then show related field and make it required (or vice versa)
  function toggle($checkbox){

    var $field = $('#' + $checkbox.attr('aria-controls'));

    if($checkbox.is(':checked')){
      $field.attr('aria-hidden', 'false');
      $field.attr('aria-expanded', 'true');
      $field.removeClass('hidden');
      $field.find('input, select, textarea').attr('required', 'required');
    } else{
      $field.attr('aria-hidden', 'true');
      $field.attr('aria-expanded', 'false');
      $field.addClass('hidden');
      $field.find('input, select, textarea').removeAttr('required');
    }

  }

  init();

});


// Quick and simple toggle to show/hide the header's drop down menu
$(document).ready(function(){

  /**
   * @param {object}
   */
  var $buttons = $('.js-dit-toggle-nav');

  /**
   * @param {object}
   */
  var $navs = $('.js-dit-nav');

  /**
   * @param {object}
   */
  var $body = $('body');

  /**
   * closeAllNavs
   *
   * @return {void}
   */
  function closeAllNavs(){
    $buttons.attr('aria-expanded', 'false');
    $navs.attr('aria-hidden', 'true');
  }

  // Set some event listeners

  // Show/Hide navs on click of button
  // Note: we don't show on hover as it is too fiddly for many users.
  $buttons.on('click', function(){
    var $currentButton = $(this);
    var $currentNav = $('#' + $currentButton.attr('aria-controls'));

    if($currentButton.attr('aria-expanded') === 'false'){
      closeAllNavs();
      $currentButton.attr('aria-expanded', 'true');
      $currentNav.attr('aria-hidden', 'false');
      $currentNav.find('a:first').focus();
    } else {
      closeAllNavs();
    }
  });

  // Close when click outside (Note: this is good for a11y)
  $body.on('click', function(e){
    var $currentNav = $navs.filter('[aria-hidden="false"]');

    if($currentNav.length > 0 && $(e.target).hasClass('js-dit-toggle-nav') !== true && $(e.target).hasClass('js-dit-nav') !== true){
      closeAllNavs();
    }
  });

  // Close when click Esc (Note: this is good for a11y)
  $body.on('keydown', function(e){
    var $currentNav = $navs.filter('[aria-hidden="false"]');

    if ($currentNav.length > 0 && e.keyCode == 27) {
      closeAllNavs();
    }
  });

  // Close when tab outside the open menu (Note: this is good for a11y)
  $body.on('keydown', function(e){
    var $currentNav = $navs.filter('[aria-hidden="false"]');
    var $lastItem = {};
    var $firstItem = {};

    if($currentNav.length === 0){
      return;
    }

    $firstItem = $currentNav.find('a').eq(0);
    $lastItem = $currentNav.find('a:last');

    if (e.keyCode === 9 && $(e.target).is($lastItem)) {
      closeAllNavs();
    } else if (e.shiftKey && e.keyCode === 9 && $(e.target).is($firstItem)) {
      closeAllNavs();
    }
  });

});


// Quick and dirty local storage on save/submit form fields
$(document).ready(function(){

  /**
   * @param {object}
   */
  var $saveButton = $('.js-save-button');

  /**
   * @param {object}
   */
  var $closeButton = $('.js-close-saved-success');

  /**
   * @param {object}
   */
  var $form = $('.dit-form');

  init();

  /**
   * init
   * Run on load
   *
   * @return {void}
   */
  function init(){
    $saveButton.click(function(e){
      saveFunctions(e);
    });

    $closeButton.click(function(e){
      closeFunctions(e);
    });
  }

  /**
   * saveFunctions
   * Show a hidden success message and focus the user there
   * In the future we will send an AJAX call to the back-end to save our data
   *
   * @param {object} e - click event
   *
   * @return {void}
   */
  function saveFunctions(e){
    e.preventDefault();
    $('.js-saved-success').show().attr('aria-hidden', 'false').focus();
    $form.find('.form-group, .dit-summary-sections, .dit-buttons').hide().attr('aria-hidden', 'true');
  }

  /**
   * closeFunctions
   * Hide the active success message
   *
   * @param {object} e - click event
   *
   * @return {void}
   */
  function closeFunctions(e){
    e.preventDefault();
    $('.js-saved-success').hide().attr('aria-hidden', 'true');
    $form.find('.form-group, .dit-summary-sections, .dit-buttons').css('display', '').attr('aria-hidden', 'false');
    $form.find('.form-control').eq(0).focus();
  }

});

// Create a global object we can reference
window.DITAlpha = window.DITAlpha || {};

(function ($) {

	"use strict";

	window.DITAlpha.FormValidation = {

    /**
     * @param {object}
     */
  	$form: $('.dit-form'),

    /**
     * init
     *
     * @return {void}
     */
  	init: function(){
    	var self = this;

    	self.$form.attr('novalidate', 'true');

      self.$form.submit(function(e){
        self.checkForErrors(e);
      });

      self.$form.find('.required-checkboxes').find('[type="checkbox"]').on('change', function(){
        self.swapAroundCheckboxProps($(this));
      });

    },

    /**
     * On submit we want to check to see if our form is
     * valid. `Valid` means, does it pass basic HTML5 rules
     * like `required` fields not being NULL or number fields
     * not exceeding their `max` value.
     *
     * If the form is not valid we don't submit it. Instead
     * we loop through the separate form fields showing/unshowing
     * the relevant inline error message.
     *
     * We also show a global error message which could sit at the top of the form or above the submit button
     *
     * @param {object} e - click event
     *
     * @return {void}
     */
    checkForErrors: function(e){
      var self = this,
          $field = {},
          $globalError = self.$form.find('.error-summary'),
          errors = [],
          errorsHTML = [];

      // Assume we're valid and hide all errors
      self.$form.find('.error-message').addClass('hidden').attr('aria-hidden', 'true');
      $globalError.addClass('hidden').attr('aria-hidden', 'true');
      self.$form.find('.form-group-error').removeClass('form-group-error');
      self.$form.find('.form-control-error').removeClass('form-control-error');
      $globalError.find('ul').html('');

      // Now check the form and if it isn't valid then show them
      if(self.$form[0].checkValidity() !== true){

        // Stop form from submitting
        e.preventDefault();

        // Unhide the main error message
        $globalError.removeClass('hidden').attr('aria-hidden', 'false');

        // Unhide inline error message for individual fields
        // Maybe this needs more thought for #a11y requirements
        self.$form.find('input, select, textarea').each(function() {

          var newError;

          $field = $(this);

          newError = $field.closest('.form-group').find('.error-message').text();

          if($field[0].checkValidity() !== true){
            $field.addClass('form-control-error');
            $field.closest('.form-group').addClass('form-group-error')
              .find('.error-message')
              .removeClass('hidden').attr('aria-hidden', 'false');

            if(errors.indexOf(newError) === -1){
              errors.push(newError);
              errorsHTML.push('<li><a href="#' + $field.attr('id') + '">' + newError + '</a></li>');
            }
          }
        });

        // Send focus to the error summary so users know an error has occurred
        $globalError.focus();
        $globalError.find('ul').html(errorsHTML);


        //
        self.clickToFocusOnError();

      }

    },

    /**
     * clickToFocusOnError
     *
     * @return {void}
     */
    clickToFocusOnError: function(){
      var self = this;

      self.$form.find('.error-summary-list').find('a').on('click', function(e){
        e.preventDefault();

        $($(this).attr('href')).focus();
      });
    },

    /**
     * Swap around the required attribute of the checkbox
     * to the active checkbox with the same name attribute value
     * This will trick our HTML5 validation sufficiently.
     *
     * This would work for a group of any inputs with a little
     * work.
     *
     * @param {object} $checkbox
     */
    swapAroundCheckboxProps: function($checkbox){

      var currentName = $checkbox.attr('name');
      var $group = $('[name="' + currentName + '"]');

      // Set/unset the required attribute accordingly
      $group.prop('required', true);
      if($group.is(":checked")){
        $group.prop('required', false);
      }
    }

	};

	window.DITAlpha.FormValidation.init();

}(jQuery));

// Accordion

(function ($) {

	"use strict";

	window.DITAlpha.Accordion = {

		/**
		 * @param {object}
		 */
		container: document.querySelector('[data-module="Accordion"]'),

		/**
		 * @param {object}
		 * The tab DOM elements in this self.container.
		 */
		tabs: null,

		/**
		 * @param {boolean}
		 * The tab content e.g. the content that is toggled by the tabs above.
		 */
		tabPanels: null,

		/**
		 * @param {boolean}
		 * Attribute set via HTML. if true then only one tab is allowed to be open at once
		 */
		closeOthers: null,

		/**
		 * @param {object}
		 * The active tab DOM element
		 */
		openedItem: null,

		/**
		 * @param {string}
		 * A list of elements that can receive focus
		 */
		focusString: 'a, area, object, input, select, textarea, button, iframe, [tabindex]',

		/**
		 * setElements
		 *
		 *
		 * @return {void}
		 */
		setElements: function() {
			var self = this;

			if(self.container) {
				self.tabs = self.container.querySelectorAll('[role="tab"]');
				self.tabPanels = self.container.querySelectorAll('[role="tabpanel"]');
				self.closeOthers =  (self.container.getAttribute('data-accordion-close-others') === 'true');
			}
		},

		/*
		 * _getContent(id)
		 *
		 * Returns the associated tabpanel content Node.
		 *
		 * @param (tab Node) The header Node that contains `aria-controls`
		 *
		 * @return Node
		 *
		*/
		getContent: function(tab) {
			var self = this;
			if (!tab.content) {
				tab.content = self.container.querySelector('#'+tab.getAttribute('aria-controls'));
			}
			return tab.content;
		},

		/*
		 * _isOpen(tab)
		 *
		 * @param (tab Node) Node you want to check if it is open.
		 *
		 * @return Boolean
		 *
		*/
		isOpen: function (tab) {
			return tab.getAttribute('aria-selected') === 'true';
		},

		/*
		 * _close(item)
		 *
		 * Hides the content of a given tab.
		 *
		 * @param (tab Node) The tab that should have it’s content hidden.
		 *
		 * @return N/A
		 *
		*/
		close: function (tab) {
			var self = this;
			var content = self.getContent(tab);

			tab.setAttribute('aria-selected', false);
			tab.setAttribute('aria-expanded', false);
			content.setAttribute('aria-hidden', true);

			self.openedItem = null;
		},

		/*
		 * _open(item)
		 *
		 * Displays the content of a given tab.
		 *
		 * @param (tab Node) The tab that should have it's content displayed.
		 *
		 * @return N/A
		 *
		*/
		open: function (tab) {
			var self = this;
			var content = self.getContent(tab);

			if (self.closeOthers && self.openedItem) {
				self.close(self.openedItem);
			}

			var tabsLength = self.tabPanels.length;
			for (var i = 0; i < tabsLength; i++) {
				self.tabs[i].getAttribute('tabindex', -1);
			}

			tab.setAttribute('aria-selected', true);
			tab.setAttribute('aria-expanded', true);
			tab.setAttribute('tabindex', 0);
			content.setAttribute('aria-hidden', false);

			self.openedItem = tab;
		},

		/*
		 * _changeSelection(oldTab, newTab)
		 *
		 * Function that handles the blurring and focusing of a new tab
		 *
		 * @param(oldTab Node) The soon-to-be previous tab
		 *
		 * @param(newTab Node) The new tab to be focused
		 *
		 * @return N/A
		 *
		*/
		changeSelection: function (oldTab, newTab) {
			oldTab.setAttribute('tabindex', -1);
			oldTab.blur();

			newTab.focus();
			newTab.setAttribute('tabindex', 0);
		},

		/*
		 * _selectNewTab(target, direction)
		 *
		 * Functions that handles the keyboard selection of a new tab.
		 *
		 * @param: function (target Node) Node from where the key event originated
		 *
		 * @param (direction string) Direction of the selection. Only accepts
		 * 'prev' and 'next' string lowercase values.
		 *
		 * @return N/A
		*/
		selectNewTab: function (target, direction) {
			var self = this;
			var newTab,
				curNdx;

			curNdx = $(target).index(self.tabs);

			switch(direction) {
				case 'prev':
					newTab = (curNdx === self.tabs.length-1) ? self.tabs[0] : self.tabs[curNdx+1];
					break;

				case 'next':
					newTab = (curNdx === 0) ? self.tabs[self.tabs.length-1] : self.tabs[curNdx-1];
					break;
			}

			self.changeSelection(target, newTab);
		},

		/*
		 * _handleClicks
		 *
		 * Handle clicks and trigger toggle if required.
		 *
		 * @param (e) the click event
		 *
		 * @return N/A
		 *
		*/
		handleClicks: function (e) {
			var self = this;
			if (e.target.getAttribute('aria-controls')) {
				self.toggleOpen(e.target);
			}
		},

		/*
		 * _unsetFocussability
		 *
		 * Make all inactive tabs unfocussability. This is for accessibility purposes...
		 * We don't want non-screen-reader-keybaord-using users to be tabbing to hidden tab content
		 * because it's a waste of time for the and it is confusing. Imagine a hidden tabcontent block
		 * with 50 links inside it and how annoying that would be to tab through.
		 *
		 * @return N/A
		 *
		 */
		unsetFocussability: function () {
			var self = this;
			var i = 0;
			var ii = 0;
			var elements = '';

			for(i = 0; i < self.tabPanels.length; i++) {
				elements = self.tabPanels[i].querySelectorAll(self.focusString);

				for (ii = 0; ii < elements.length; ii++) {
					elements[ii].setAttribute('tabindex', '-1');
				}
			}
		},

		/*
		 * _setFocussability
		 *
		 * Make active tabs focusable elements focusaable again and vice versa.
		 * Because we unset the ability to focus with _unsetFocussability above
		 * we now need to allow user to tab to things when a tab is active/visible.
		 *
		 * @return N/A
		 *
		 */
		setFocussability: function (tab) {

			var self = this;
			var i = 0;
			var content = self.getContent(tab);
			var elements = content.querySelectorAll(self.focusString);
			var isOpen = self.isOpen(tab);

			if (elements) {
				for (i = 0; i < elements.length; i++) {
					if (isOpen === true) {
						elements[i].removeAttribute('tabindex');
					} else {
						elements[i].setAttribute('tabindex', '-1');
					}
				}
			}

		},

		/*
		 * _toggleOpen
		 *
		 * Function that toggles a tab between opened and closed states.
		 *
		 * @param (tab Node) The tab you want to toggle.
		 *
		 * @return N/A
		 *
		*/
		toggleOpen: function (tab) {
			var self = this;
			if (self.isOpen(tab)) {
				self.close(tab);
			} else {
				self.open(tab);
			}
			self.setFocussability(tab);
		},


		/*
		 * _init()
		 *
		 * Function that kickstarts the accordion and binds the events.
		 *
		 * @return N/A
		 *
		*/
		init: function () {
			var self = this;

			if (!self.container) {
				return;
			}

			self.openedItem = self.container.querySelector('[aria-selected="true"]');

			self.setElements();
			self.unsetFocussability();
			self.container.addEventListener('click', function(e){
				self.handleClicks(e);
			}, false);
		}

	};

	window.DITAlpha.Accordion.init();

}(jQuery));
