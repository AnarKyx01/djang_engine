$( document ).ready(function(){
	$('.datepicker-month').each(function(){
		$(this).datepicker( {
		    changeMonth: true,
	        changeYear: true,
	        showButtonPanel: true,

	        onClose: function(dateText, inst) {
	            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
	            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
	            $(this).val($.datepicker.formatDate('yy-mm-dd', new Date(year, parseInt(month)+1, 0)));
		        }
	    });

	    $(".datepicker-month").focus(function () {
	        $(".ui-datepicker-calendar").hide();
	        $("#ui-datepicker-div").position({
	            my: "center top",
	            at: "center bottom",
	            of: $(this)
	        });
	    });
	});
		$('.datepicker-year').each(function(){
		$(this).datepicker( {
		    changeMonth: false,
	        changeYear: true,
	        showButtonPanel: true,

	        onClose: function(dateText, inst) {
	            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
	            $(this).val($.datepicker.formatDate('yy', new Date(year, 1)));
		        }
	    });

	    $(".datepicker-year").focus(function () {
	        $(".ui-datepicker-calendar").hide();
	        $(".ui-datepicker-month").hide()
	        $("#ui-datepicker-div").position({
	            my: "center top",
	            at: "center bottom",
	            of: $(this)
	        });
	    });
	});
	$('.datepicker').each(function(){
		$(this).datepicker({
			dateFormat: 'yy-mm-dd',
		    changeMonth: true,
	        changeYear: true,
	        showButtonPanel: true,
	    });
	});
	$('#chart_options > div:gt(0)').hide();
	$("#data_range").change(function(){
		$('#chart_options > div:gt(0)').hide();
		var str= $( "#data_range option:selected").val();
		if(str=="month"){
			$("#month_input").show();
		}
		else if(str=="year"){
			$("#year_input").show();
		}
		else if(str=="date_range"){
			$("#date_range_input").show();
		}
		else if(str="date"){
			$("#date_input").show();
		}
	}).change();
	
	$('form').on('submit', function(event){
		event.preventDefault();
		$.post($( this ).attr('action'),
				$(this).serialize(),
				function( data ){
					$('#gen_chart').empty();
					$('#gen_chart').append(data);
					
		});
	});
});