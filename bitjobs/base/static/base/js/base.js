$(document).ready(function() {

    function search(commission_id) {
      // here we have id of model and we need an url
      window.location.href = 'TODO url';
    }

    $(function() {
      $("#bitjobs-search-input").autocomplete({
          source: "{% url 'TODO' %}",
          minLength: 2,
          select: function(event, ui) {
              search(ui.item.id);
          }
      });
    });


    $( '#menu-btn' ).click(function(){
        $('.mobile-menu').toggleClass('expand')
    })
});
