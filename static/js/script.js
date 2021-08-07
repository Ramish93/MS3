$(document).ready(function () {
    $(".sidenav").sidenav();
    $('input#input_text, textarea#textarea2').characterCounter();
    $('.datepicker').datepicker({
        format: 'dd mm, yyyy',
        yearRange: 45,
        autoClose: true,
        showClearBtn: true,
        i18n: {
            done: 'Select'
        }
    });
});