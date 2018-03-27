function train_status() {
$.ajax({
	url: "http://10.100.0.86:5000/get_inbound_trains",
	datatype: 'jsonp',
	success: function(inbound_trains){
		var inboundtrains = inbound_trains;
		var tr_info_str = ""
		if (inboundtrains == "" ) { 
			var tr_info_str = "No Trains to NYP"
			console.log("No NYP");
		};
		for (train in inboundtrains) {
			var tr_time = inboundtrains[train].time;
			var tr_number = inboundtrains[train].number;
			var tr_status = inboundtrains[train].status;
			tr_info_str += tr_time + ' ' + tr_number + ' ' + tr_status + "<br>"
			// document.getElementById("tr_time").innerHTML = tr_time;
			// document.getElementById("tr_number").innerHTML = tr_number;
		        //document.getElementById("tr_status").innerHTML = tr_status;
			train++;
			console.log("Train Checked");
		};
		document.getElementById("tr_info_str").innerHTML = tr_info_str;	
	},
	
});
};

function train_issues() {
$.ajax({
	url: "http://10.100.0.86:5000/get_nyp_issues",
	datatype: 'jsonp',
	success: function(nyp_issues){
	var train_issues = nyp_issues;
		var tr_cancelled = train_issues[0].cancel;
		// var tr_checked = train_issues[0].checked;
		var tr_delayed = train_issues[0].delay;
	        document.getElementById("tr_cancelled").innerHTML = tr_cancelled;
	        // document.getElementById("tr_checked").innerHTML = tr_checked;
	        document.getElementById("tr_delayed").innerHTML = tr_delayed;
	}
});
};

train_status();
setInterval(train_status, 180000);

train_issues();
setInterval(train_issues, 180000);
