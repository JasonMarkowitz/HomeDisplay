function train_status_nyp() {
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

function train_status_HOB() {
$.ajax({
	url: "http://10.100.0.86:5000/get_inbound_trains_HOB",
	datatype: 'jsonp',
	success: function(inbound_trains_HOB){
		var inboundtrainsHOB = inbound_trains_HOB;
		var tr_info_str_HOB = ""
		if (inboundtrainsHOB == "" ) { 
			var tr_info_str_HOB = "No Trains to HOB"
			console.log("No HOB");
		};
		for (train in inboundtrainsHOB) {
			var tr_time_HOB = inboundtrainsHOB[train].time;
			var tr_number_HOB = inboundtrainsHOB[train].number;
			var tr_status_HOB = inboundtrainsHOB[train].status;
			tr_info_str_HOB += tr_time_HOB + ' ' + tr_number_HOB + ' ' + tr_status_HOB + "<br>"
			// document.getElementById("tr_time").innerHTML = tr_time;
			// document.getElementById("tr_number").innerHTML = tr_number;
		        //document.getElementById("tr_status").innerHTML = tr_status;
			train++;
			console.log("Train Checked");
		};
		document.getElementById("tr_info_str_HOB").innerHTML = tr_info_str_HOB;	
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

train_status_nyp();
setInterval(train_status_nyp, 180000);

train_status_HOB();
setInterval(train_status_HOB, 180000);

train_issues();
setInterval(train_issues, 180000);
