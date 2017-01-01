var a_center_counter=0;
var a_corner_counter=0;
var a_beacon_counter=0;
var a_score_counter=0;
var a_capball_previous;
var a_park_previous;
var t_center_counter=0;
var t_corner_counter=0;
var t_score_counter=0;
var t_beacon_previous;
var t_capball_previous;
var total_score_counter=0;

jQuery(document).ready(function() {
    $("#a_center_incr").click(function(){
        a_center_counter+=15;
        a_score_counter+=15;
        $("#a_center_vortex").val(a_center_counter);
        $("#a_score").val(a_score_counter);
        $('#a_score').trigger('change');
    });
    $("#a_center_decr").click(function(){
        a_center_counter-=15;
        a_score_counter-=15;
        $("#a_center_vortex").val(a_center_counter);
        $("#a_score").val(a_score_counter);
        $('#a_score').trigger('change');
    });
    $("#a_corner_incr").click(function(){
        a_corner_counter+=5;
        a_score_counter+=5;
        $("#a_corner_vortex").val(a_corner_counter);
        $("#a_score").val(a_score_counter);
        $('#a_score').trigger('change');
    });
    $("#a_corner_decr").click(function(){
        a_corner_counter-=5;
        a_score_counter-=5;
        $("#a_corner_vortex").val(a_corner_counter);
        $("#a_score").val(a_score_counter);
        $('#a_score').trigger('change');
    });
    $("#a_beacon_incr").click(function(){
        a_beacon_counter+=30;
        a_score_counter+=30;
        $("#a_beacon").val(a_beacon_counter);
        $("#a_score").val(a_score_counter);
        $('#a_score').trigger('change');
    });
    $("#a_beacon_decr").click(function(){
        a_beacon_counter-=30;
        a_score_counter-=30;
        $("#a_beacon").val(a_beacon_counter);
        $("#a_score").val(a_score_counter);
        $('#a_score').trigger('change');
    });

    $("select[name=a_capball]").focus(function () {
        a_capball_previous = this.value;
    }).change(function() {
        a_score_counter+=(this.value - a_capball_previous);
        $("#a_score").val(a_score_counter);
        $('#a_score').trigger('change');
        a_capball_previous = this.value;
    });

    $("select[name=a_park]").focus(function () {
        a_park_previous = this.value;
    }).change(function() {
        a_score_counter+=(this.value - a_park_previous);
        $("#a_score").val(a_score_counter);
        $('#a_score').trigger('change');
        a_park_previous = this.value;
    });

    $("#t_center_incr").click(function(){
        t_center_counter+=5;
        t_score_counter+=5;
        $("#t_center_vortex").val(t_center_counter);
        $("#t_score").val(t_score_counter);
        $('#t_score').trigger('change');
    });
    $("#t_center_decr").click(function(){
        t_center_counter-=5;
        t_score_counter-=5;
        $("#t_center_vortex").val(t_center_counter);
        $("#t_score").val(t_score_counter);
        $('#t_score').trigger('change');
    });
    $("#t_corner_incr").click(function(){
        t_corner_counter+=1;
        t_score_counter+=1;
        $("#t_corner_vortex").val(t_corner_counter);
        $("#t_score").val(t_score_counter);
        $('#t_score').trigger('change');
    });
    $("#t_corner_decr").click(function(){
        t_corner_counter-=1;
        t_score_counter-=1;
        $("#t_corner_vortex").val(t_corner_counter);
        $("#t_score").val(t_score_counter);
        $('#t_score').trigger('change');
    });

    $("select[name=t_beacon]").focus(function () {
        t_beacon_previous = this.value;
    }).change(function() {
        t_score_counter+=(this.value - t_beacon_previous);
        $("#t_score").val(t_score_counter);
        $('#t_score').trigger('change');
        t_beacon_previous = this.value;
    });

    $("select[name=t_capball]").focus(function () {
        t_capball_previous = this.value;
    }).change(function() {
        t_score_counter+=(this.value - t_capball_previous);
        $("#t_score").val(t_score_counter);
        $('#t_score').trigger('change');
        t_capball_previous = this.value;
    });

    $("#a_score").change(function(){
        total_score_counter = parseInt(this.value) + parseInt($("#t_score").val());
        console.log("Total Score: " + total_score_counter);
        $("#total_score").val(total_score_counter);
    });
    $("#t_score").change(function(){
        total_score_counter = parseInt(this.value) + parseInt($("#a_score").val());
        console.log("Total Score: " + total_score_counter);
        $("#total_score").val(total_score_counter);
    });

    // hide advanced scoring fields
    $("input#adv_metrics").change(function () {
        if (this.checked) {
            $('div#particle_speed.form-group').show();
            $('div#capball_speed.form-group').show();
            $('div#match_notes.form-group').show();
        } else {
            $('div#particle_speed.form-group').hide();
            $('div#capball_speed.form-group').hide();
            $('div#match_notes.form-group').hide();
        }
    });

    // Pivot the Pit Scouting Information for team competition view
    $("a#pit_report").click(function () {
        $("table#pit_report.table.table-responsive").each(function () {
            var $this = $(this);
            var newrows = [];
            $this.find("tr").each(function () {
                var i = 0;
                $(this).find("td,th").each(function () {
                    i++;
                    if (newrows[i] === undefined) {
                        newrows[i] = $("<tr></tr>");
                    }
                    newrows[i].append($(this));
                });
            });
            $this.find("tr").remove();
            $.each(newrows, function () {
                $this.append(this);
            });
        });
        return false;
    });
});