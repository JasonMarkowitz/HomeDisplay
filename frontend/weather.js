function weather_main() {
$.ajax({
	url: "http://10.100.0.86:5000/weather",
	datatype: 'jsonp',
	success: function(weather){
		var weatherdata = weather;

		var now_conditions = weather["0"].conditions;
		var now_period = weather["0"].period;
		var now_temp = weather["0"].temp;
		var now_wind_info = weather["0"].wind_info;
		document.getElementById("now_conditions").innerHTML = now_conditions;
		document.getElementById("now_period").innerHTML = now_period;
		document.getElementById("now_temp").innerHTML = now_temp;
		document.getElementById("now_wind_info").innerHTML = now_wind_info;

		var later_conditions = weather["1"].conditions;
		var later_period = weather["1"].period;
		var later_temp = weather["1"].temp;
		var later_wind_info = weather["1"].wind_info;
		document.getElementById("later_conditions").innerHTML = later_conditions;
		document.getElementById("later_period").innerHTML = later_period;
		document.getElementById("later_temp").innerHTML = later_temp;
		document.getElementById("later_wind_info").innerHTML = later_wind_info;
		
		//var tomorrow_conditions = weather["2"].conditions;
		//var tomorrow_period = weather["2"].period;
		//var tomorrow_temp = weather["2"].temp;
		//var tomorrow_wind_info = weather["2"].wind_info;
		//document.getElementById("tomorrow_conditions").innerHTML = tomorrow_conditions;
		//document.getElementById("tomorrow_period").innerHTML = tomorrow_period;
		//document.getElementById("tomorrow_temp").innerHTML = tomorrow_temp;
		//document.getElementById("tomorrow_wind_info").innerHTML = now_wind_info;
	},
	
});
};
weather_main()
setInterval(weather_main, 900000)
