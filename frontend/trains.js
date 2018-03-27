function train_status() {
$.ajax({
	url: "http://10.100.0.86:5000/get_inbound_trains",
	datatype: 'jsonp',
	success: function(inbound_trains){
		var inboundtrains = inbound_trains;
		var tr_info_str = ""
		for (train in inboundtrains) {
			var tr_time = inboundtrains[train].time;
			var tr_number = inboundtrains[train].number;
			var tr_status = inboundtrains[train].status;
			tr_info_str += tr_time + ' ' + tr_number + ' ' + tr_status + "<br>"
			// document.getElementById("tr_time").innerHTML = tr_time;
			// document.getElementById("tr_number").innerHTML = tr_number;
		        //document.getElementById("tr_status").innerHTML = tr_status;
			train++;
		}
		document.getElementById("tr_info_str").innerHTML = tr_info_str;	
	},
	
});
};
train_status()
setInterval(train_status, 180000)
