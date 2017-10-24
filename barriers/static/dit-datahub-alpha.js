/**
 * Data Hub / Trade Barriers JavaScript
 *
 *
 */

var bt = document.getElementById('id_barrier_type');

if(bt){

  var btOptions = bt.querySelectorAll('option');

  // Hide grand kids to make the dropdown smaller
  btOptions.forEach(function(el){
    if(el.innerHTML.indexOf('------') == 0){
      el.style.display = 'none';
    }
  });

}

/**
 * btUpdate
 * Send an AJAX call to our API with the selected id and populate a secondary
 * <select> with the JSON that comes back
 * @param {object} event
 *
 * @return {void}
 */
function btUpdate(event){

    var HTML = '';
    var DONE = 4; // readyState 4 means the request is done.
    var OK = 200; // status 200 is a successful return.
    var xhr = new XMLHttpRequest();
    var endpoint = '/api/barriersubtypes?barrier_type=';
    var ajaxSuccess = false;
    var JSONx = null;
    var sub = document.getElementById('field-sub-barrier-type');
    var subParent = document.getElementById('group-field-sub-barrier-type');

    if(!sub || !subParent){
      return;
    }

    xhr.open('GET', endpoint + bt.value);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X_REQUESTED_WITH', 'XMLHttpRequest');
    xhr.setRequestHeader('X-Requested-By', 'XMLHttpRequest');
    xhr.send();

    xhr.onreadystatechange = function () {

      if (xhr.readyState === DONE) {
        if (xhr.status === OK) {

          var JSONx = JSON.parse(xhr.responseText);

          if(JSONx.children){
            HTML = HTML + '<option value="">' + subParent.querySelector('label').innerHTML + '</option>';
            JSONx.children.forEach(function(el){
              HTML = HTML + '<option value="' + el.id + '">' + el.name + '</option>';

              if(el.children){
                el.children.forEach(function(el){
                  HTML = HTML + '<option value="' + el.id + '">--- ' + el.name + '</option>';
                });
              }

            });
            subParent.setAttribute('aria-hidden', 'false');
            subParent.classList.remove('u-hidden');
            sub.innerHTML = HTML;
            sub.setAttribute('required', true);
          } else{
            subParent.setAttribute('aria-hidden', 'true');
            subParent.classList.add('u-hidden');
            sub.innerHTML = '';
            sub.removeAttribute('required');
          }
        }
      }
    };

    // XHR error = send user to linked URL
    if(!xhr) {
      alert('Something went wrong when selecting a HMG barrier type');
    }

  }

if(bt){
  // update the dropdown with AJAX after every change
  bt.addEventListener('change', function(event){
    btUpdate(event);
  });

  // update the dropdown with AJAX on page load
  document.addEventListener('DOMContentLoaded', function(event) {
    btUpdate(event);
  });
}
