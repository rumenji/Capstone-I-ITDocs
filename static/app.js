
// qJuery used for changing the active status on the top and sidebar navigation

$(document).ready(function () {
    let url = window.location;

    $('ul#navigation a[href="' + url + '"]').parent().addClass('active');
    $('ul#navigation a').filter(function () {
        return this.href == url;
    }).parent().addClass('active');

    $('ul#side-navigation a[href="' + url + '"]').parent().addClass('active-side');
    $('ul#side-navigation a').filter(function () {
        return this.href == url;
    }).parent().addClass('active-side');

    
    $('#back').on('click', function(){
        history_back()
    })
});
function history_back(){
    history.back()
}