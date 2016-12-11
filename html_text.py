"""
Authors: Sean Donohoe and Kyle Wiese

String templates for index.html
"""

keywordTag = """
<div class="form-group">
    <h3 style="display: inline; margin-right: 10px">{}</h3><input onclick="checkUpdate('{}')" type="checkbox" value="{}" name="{}-selected"><br>
    <div id={} style="margin-left:15%; width: 95%; display:none">
        <h5 style="display:inline">Don't spend longer than</h5>
        <select name="{}-upperHour" class="form-control" style="display:inline; width:10%; margin: 5px">
           {} 
        </select>
        <p style="display:inline">hours</p>
        <select name="{}-upperMinute" class="form-control" style="display:inline; width:10%; margin: 5px">
            <option value=0 selected>0</option>
            <option value=1800>30</option>
        </select>
        <p style="display:inline">minutes here</p><br>
        <h5 style="display:inline">Interest Multiplier</h5>
        <select name="{}-multiplier" class="form-control" style="display:inline; width:10%; margin: 5px">
            <option value=1 selected>1</option>
            <option value=2>2</option>
            <option value=3>3</option>
            <option value=4>4</option>
            <option value=5>5</option>
        </select><br>
        <h5 style="display:inline">Number of {} places visited: </h5>
        <select name="{}-equality" class="form-control" style="display:inline; width:15%; margin: 5px">
            <option value="NONE" selected>Unlimited</option>
            <option value="EQ"> = </option>
            <option value="LTE"> &le; </option>
            <option vlaue="GTE"> &ge; </option>
        </select>
        <input type="number" class="form-control" style="display:inline; width:10%" name="{}-strictness" value="0" min="0" step="1"/>
    </div>
</div>
"""

keywordHourOptionTagSelected = """
<option value={} selected>{}</option>
"""

keywordHourOptionTag = """
<option value={}>{}</option>
"""

indexBegin = """
<!DOCTYPE html>
<html>
    <head>
        <title>Linear Programming</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <script>
            function checkUpdate(keyword) {
                var e = document.getElementById(keyword)
                if(e.style.display == 'block')
                    e.style.display = 'none'
                else
                    e.style.display = 'block'
            }
        </script>
        
        <script>
            $(document).ready(function () {
                $('#pathdata').on('submit', function(e) {
                    e.preventDefault();
                    document.getElementById("queryPage").style.display = 'none';
                    document.getElementById("loading").style.display = 'block';
                    $.ajax({
                        type: 'post',
                        url: '/getRoute/',
                        data: $('#pathdata').serialize(),
                        dataType: 'json',
                        success: function(data) {
                            document.getElementById("loading").style.display = 'none';
                            document.getElementById("results").style.display = 'block';
                            $.each(data, function(k, v) {
                                if (k == "path"){
                                    if (data[k].length > 0) {
                                        for (var i in data[k]) {
                                            var j = (parseInt(i)+1);
                                            $("#finalpath").append("<li class='list-group-item' style='margin: 5px'>"+ j.toString() + ") "  + data[k][i] + "</li>");
                                        }
                                    } else {
                                        document.getElementById("results").style.display = 'none';
                                        document.getElementById("nopath").style.display = 'block';
                                    }
                                }
                            });
                        }
                    });
                });
            });
        </script>
    </head>

    <body>
	<nav class="navbar navbar-default">
	  <div class="container-fluid">
	    <div class="navbar-header">
	      <a class="navbar-brand" href= "/" >CSCI 5654 Project</a>
	    </div> 
	  </div>
	</nav>

	<div class="container" id="queryPage">
	    <div class="jumbotron">
	        <h1>Maximize Your Day's Value</h1>      
	    </div>
            <form id="pathdata">
                <div class="form-group">
                    <h4>Starting Address</h4>
                    <input class="form-control" type="text" style="width:50%" name="start_address" placeholder="Starting Address (E.g. 1769 Rockies Ct, Lafayette, CO)"><br>
                    <h4>Search Radius</h4>
                    <select class="form-control" name="searchRadius" style="width: 50%">
                        <option value=805 selected>0.5 miles</option>
                        <option value=1287>0.8</option>
                        <option value=1770>1.1 miles</option>
                    </select>
                    <h4>Average Budget</h4>
                    <select class="form-control" name="budget" style="width: 50%">
                        <option value=0>$</option>
                        <option value=1>$$</option>
                        <option value=2 selected>$$$</option>
                        <option value=3>$$$$</option>
                        <option value=4>$$$$$</option>
                    </select>
                    <h4>How Much Time do You Have?</h4>
                    <select name="userHour" class="form-control" style="display:inline;width: 15%">
                        <option value=0>0</option>
                        <option value=3600 selected>1</option>
                        <option value=7200>2</option>
                        <option value=10800>3</option>
                        <option value=14400>4</option>
                        <option value=18000>5</option>
                        <option value=21600>6</option>
                        <option value=25200>7</option>
                        <option value=28800>8</option>
                    </select>
                    <p style="display:inline; margin: 5px">hours</p>
                    <select name="userMinute" class="form-control" style="display:inline;width: 15%">
                        <option value=0>0</option>
                        <option value=1800 selected>30</option> 
                    </select> 
                    <o style="display:inline; margin: 5px">minutes</p>
                </div>
                <h4>Keywords</h4>
                <div style="margin-left: 10%">
"""

indexEnd = """
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div> 
        <div class="container" id="loading" style="display: none">
            <div class="jumbotron">
	        <h1>Maximize Your Day's Value</h1>      
	    </div>
            <h4 style="text-align:center; display:inline">Calculating your adventure...</h4>
            <i class="fa fa-spinner fa-spin" style="font-size:24px; color: blue"></i>
        </div>
        <div class="container" id="results" style="display: none">
            <div class="jumbotron">
	        <h1>Maximize Your Day's Value</h1>      
	    </div>
            <h1 class="display-3">Your Route</h1>
            <div style="width:80%; margin: 0 auto; border-radius: 5px; overflow: scroll; background-color: #666666">
                <ol id="finalpath" class="list-group" style="margin: 10px">
                </ol>
            </div>
        </div>
       <div class="container" id="nopath" style="display: none">
            <div class="jumbotron">
	        <h1>Maximize Your Day's Value</h1>      
	    </div>
            <h3 style="margin: 0 auto; width: 50%">Sorry, we couldn't find a route for you!</h3>
        </div>
   </body>
</html>
"""


