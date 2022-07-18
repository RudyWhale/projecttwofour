guest_data = {};
guest_equip = {};
guest_statuses = ['не определился', 'участвую', 'не участвую'];
guest_car_statuses = ['нет', 'да'];


function parse_current_guest_status() {
    status_val = $('#guest_status_btn').text();

    if (status_val == 'не определился'){ return 'Possible going' }
    else if (status_val == 'участвую'){ return 'Going' }
    else if (status_val == 'не участвую'){ return 'Not going' }
}


function set_current_guest_status(status_val) {
    status_btn = $('#guest_status_btn');

    if (status_val == 'Possible going'){ status_btn.text('не определился') }
    else if (status_val == 'Going'){ status_btn.text( 'участвую') }
    else if (status_val == 'Not going'){ status_btn.text('не участвую') }
    
    if (status_val == 'Not going'){ status_btn.addClass('negative'); }
    if (status_val == 'Going'){ status_btn.addClass('positive'); }    
}


function get_message_div(message_html) {
    return '<div class="message">\n' + message_html + '\n</div>';
};


function load_content(){
    $.get(urls.load_content, function(response){
        guest_data = response.guest_data;
        guest_equip = response.guest_equip;
        messages = response.messages_content;
        messages_html = '';
        messages.forEach(msg => messages_html = messages_html + get_message_div(msg.html));
        $('#guest_messages').html(messages_html);

        $('#guest_first_name').text(guest_data.first_name);
        $('#guest_last_name').text(guest_data.last_name);
        set_current_guest_status(guest_data.guest_status);

        $('#have_car_btn').text(guest_equip.has_car ? 'да' : 'нет');
        $('#mats_count').text(guest_equip.mats);
        $('#tents_count').text(guest_equip.tents);

        if (guest_equip.has_car){$('#have_car_btn').addClass('positive')}
        if (guest_equip.mats > 0){$('#mats_count_form').addClass('positive')}
        if (guest_equip.tents > 0){$('#tents_count_form').addClass('positive')}

        $('#guest_reg_form').addClass('hidden');
        $('#citation_container').addClass('collapsed');
        $('#guest_info, #guest_messages').removeClass('hidden');
    });
};


function send_guest_code_handler(e){
    e.preventDefault();
    guest_code = $('input#guest_code').val();
    // guest_email = $('input#guest_email').val();
    csrf_token = $('input[name=csrfmiddlewaretoken]').val();

    if (guest_code == ''){
        alert('Для продолжения необходимо ввести код гостя');
    }
    else {
        request_data = {
            guest_code: guest_code,
            // guest_email: guest_email,
            csrfmiddlewaretoken: csrf_token,
        }
        $.post(urls.authenticate, request_data, function(response){
            if (response.status == 'success') {
                guest_data = response.guest_data;
                load_content();
            }
            else {
                alert('Гость не найден :(');
            }
        });
    }
};


function change_user_status() {
    button = $('#guest_status_btn');
    curr_status = button.text();
    curr_status_index = guest_statuses.findIndex(el => el == curr_status);
    next_status = guest_statuses[(curr_status_index + 1) % guest_statuses.length];
    button.text(next_status);

    if (next_status == 'участвую'){
        button.removeClass('negative');
        button.addClass('positive');
    }
    else if (next_status == 'не участвую'){
        button.removeClass('positive');
        button.addClass('negative');
    }
    else {
        button.removeClass('positive');
        button.removeClass('negative');
    }
};


function change_car_status() {
    button = $('#have_car_btn');
    curr_status = button.text();
    curr_status_index = guest_car_statuses.findIndex(el => el == curr_status);
    next_status = guest_car_statuses[(curr_status_index + 1) % guest_car_statuses.length];
    button.text(next_status);

    if (next_status == 'да'){
        button.addClass('positive');
    }
    else {
        button.removeClass('positive');
    }
};


function increase_equip_count(counter, form) {
    curr_count = parseInt(counter.text());
    counter.text(curr_count + 1);
    form.addClass('positive');
};


function decrease_equip_count(counter, form) {
    curr_count = parseInt(counter.text());

    if (curr_count > 0){
        counter.text(curr_count - 1);
    }
    if (curr_count == 1){
        form.removeClass('positive');
    }
};


function show_guest_info() {
    $('div#guest_info').addClass('shown');
}


function hide_guest_info() {
    $('div#guest_info').removeClass('shown');
}


function send_guest_status() {
    request_data = {
        'guest_status': parse_current_guest_status(),
        'has_car': $('#have_car_btn').text() == 'да' ? true : false,
        'mats': $('#mats_count').text(),
        'tents': $('#tents_count').text(),
    };
    $.get(urls.update_guest_status, request_data, () => {
        if ($('button#show_menu').is(':visible')) {
            hide_guest_info();
        }
    });
}


$(function(){
    $('#guest_status_btn').on('click', change_user_status);
    $('#have_car_btn').on('click', change_car_status);
    $('#increase_mats_btn').on('click', () => increase_equip_count($('#mats_count'), $('#mats_count_form')));
    $('#decrease_mats_btn').on('click', () => decrease_equip_count($('#mats_count'), $('#mats_count_form')));
    $('#increase_tents_btn').on('click', () => increase_equip_count($('#tents_count'), $('#tents_count_form')));
    $('#decrease_tents_btn').on('click', () => decrease_equip_count($('#tents_count'), $('#tents_count_form')));
    $('#send_guest_status').on('click', send_guest_status);
    
    $('button#show_menu').on('click', show_guest_info);
    $('button#hide_menu').on('click', hide_guest_info);

    if (user_is_authenticated == 'False'){
        $('button#send_guest_code').on('click', send_guest_code_handler);
        $('#guest_reg_form').removeClass('hidden');
    }
    else {
        load_content();
    }
});
