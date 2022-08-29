$(document).ready(function() {
    function filterItems() {
		let index = 0;
		let obj = $("#artikl_" + index);

		let minPrice = $('#hidden_minimum_price').val();
		let maxPrice = $('#hidden_maximum_price').val();
		let markeElements = $(".marka");
		let checkedMarke = []
		let velicineElements = $(".velicina");
		let checkedVelicine = []

		for (e of markeElements) {
			let value = e.getAttribute("value")
			let checked = e.checked
			if (checked) {
				checkedMarke.push(value)
			}
		}

		for (e of velicineElements) {
			let value = e.getAttribute("value")
			let checked = e.checked
			if (checked) {
				checkedVelicine.push(value)
			}
		}

		while (obj[0] != undefined) {
			let cijenaObjekta = parseFloat($('#artikl_' + index + '_cijena')[0].innerHTML);
			let markaObjekta = $('#artikl_' + index + '_marka')[0].innerHTML;
			let velicinaObjekta = $('#artikl_' + index + '_velicina')[0].innerHTML;

			if((cijenaObjekta < maxPrice && cijenaObjekta > minPrice)
            && (checkedVelicine.includes(velicinaObjekta) || checkedVelicine.length == 0)
            && (checkedMarke.includes(markaObjekta) || checkedMarke.length == 0)) {
				obj.removeClass("d-none");
			}
			else {
				obj.addClass("d-none");
			}
			index++;
			obj = $("#artikl_" + index);
		}
    }


	$(".marka").change(function() {
	    filterItems();
	})
	$(".velicina").change(function() {
		filterItems();
	})
	$('#price_range').slider({
		range:true,
		min:0,
		max:5000,
		values:[0,5000],
		step:1,
		slide:function(event,ui){
			$('#price_show').html(ui.values[0] + ' - ' + ui.values[1]);
			$('#hidden_minimum_price').val(ui.values[0]);
			$('#hidden_maximum_price').val(ui.values[1]);
			filterItems();
		}
	});
});