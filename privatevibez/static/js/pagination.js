	$(document).ready(function() {

var show_per_page = 20;
var number_of_items = $('#section-FEATURED').children('ul').length;
var number_of_pages = Math.ceil(number_of_items / show_per_page);


$('#main').append('<div class=controls></div><input id=current_page type=hidden><input id=show_per_page type=hidden>');
$('#current_page').val(0);
$('#show_per_page').val(show_per_page);

var navigation_html = '<a class="prev" onclick="previous()"><</a>';
var current_link = 0;
while (number_of_pages > current_link) {
	navigation_html += '<a class="page" onclick="go_to_page(' + current_link + ')" longdesc="' + current_link + '">' + (current_link + 1) + '</a>';
	current_link++;
}
navigation_html += '<a class="next" onclick="next()">></a>';

$('.controls').html(navigation_html);
$('.controls .page:first').addClass('active');

$('#section-FEATURED').children().css('display', 'none');
$('#section-FEATURED').children().slice(0, show_per_page).css('display', 'flex');

});



function go_to_page(page_num) {
var show_per_page = parseInt($('#show_per_page').val(), 0);

start_from = page_num * show_per_page;

end_on = start_from + show_per_page;

$('#section-FEATURED').children().css('display', 'none').slice(start_from, end_on).css('display', 'flex');

$('.page[longdesc=' + page_num + ']').addClass('active').siblings('.active').removeClass('active');

$('#current_page').val(page_num);
}



function previous() {

new_page = parseInt($('#current_page').val(), 0) - 1;
//if there is an item before the current active link run the function
if ($('.active').prev('.page').length == true) {
	go_to_page(new_page);
}

}

function next() {
new_page = parseInt($('#current_page').val(), 0) + 1;
//if there is an item after the current active link run the function
if ($('.active').next('.page').length == true) {
	go_to_page(new_page);
}

}