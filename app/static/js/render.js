
	function content_load_cb(data, textStatus, jqXHR)
	{
		console.log("Replacing content")
		var content = $("#content");
		var cachest = $(".cachestate");
		var filtst  = $(".filterstate");
		console.log("content", content);
		console.log("data", data);
		console.log("textStatus", textStatus);

		cachest.text(data['cachestate']);
		filtst.text(data['filterstate']);
		content.html(data['contents']);
		document.title = "ReadProxy - " + data['title']


		// Clear the callback on the events so we don't set another callback every reload
		$('#refetch_link_1').off('click');
		$('#refetch_link_2').off('click');

		$("#refetch_link_1").html('Re-Fetch');
		$("#refetch_link_2").html('Re-Fetch');


		$('#refetch_link_1').click(load_nocache);
		$('#refetch_link_2').click(load_nocache);


	};
	function content_load_fail(jqXHR, textStatus, errorThrown)
	{

		$("#refetch_link_1").html('Re-Fetch');
		$("#refetch_link_2").html('Re-Fetch');

		$('#refetch_link_1').click(load_nocache);
		$('#refetch_link_2').click(load_nocache);

		alert("Failed to fetch content!\nError: " + errorThrown + "\nStatus text: " + textStatus);
	}


	function load_cache(url)
	{

		$('#refetch_link_1').off('click');
		$('#refetch_link_2').off('click');

		$("#refetch_link_1").html('Loading...').off('click');
		$("#refetch_link_2").html('Loading...').off('click');


		$.ajax({
			url      : url,
			success  : content_load_cb,
			error    : content_load_cb,
			dataType : "json",
			cache    : false,

		})

	}


	function load_nocache(event)
	{
		event.stopImmediatePropagation();

		$('#refetch_link_1').off('click');
		$('#refetch_link_2').off('click');

		$("#refetch_link_1").html('Refetching').off('click');
		$("#refetch_link_2").html('Refetching').off('click');


		console.log("Load nocache");

		$.ajax({
			url      : url,
			success  : content_load_cb,
			error    : content_load_fail,
			dataType : "json",

		})
	}


