
$(document).ready(function () {
    let url = window.location;
    console.log(url)
    $('ul#navigation a[href="' + url + '"]').parent().addClass('active');
    $('ul#navigation a').filter(function() {
        return this.href == url;
    }).parent().addClass('active');

    $('ul#side-navigation a[href="' + url + '"]').parent().addClass('active-side');
    $('ul#side-navigation a').filter(function() {
        return this.href == url;
    }).parent().addClass('active-side');
});