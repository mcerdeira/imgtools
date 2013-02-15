<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<meta http-equiv="Cache-control" content="public">
<title>GliTch Playground (beta)</title>
<link rel="stylesheet" type="text/css" href="/css/main.css"/>
</head>

<body>
   <div id="wrapper">
		 <br>
         <h1>GliTch Playground (beta)</h1>
		
		 <br>
		 <br>
		 <br>
		 <br>
		 
		 <div id="content">		       
			   	<form method="post" action="/submited/">		
					Image Url: <input type="text" name="url" style="width: 500px"/><br><br>			
					Effects: <br><br>
					
					%for i in range(0, len(actions)-1):
					<input id="chk{{i}}" type="checkbox" name="{{actions[i]}}" value="{{actions[i]}}"> {{actions[i]}}<br>
					%end
					
					<br>
					
					<input type="submit" value="Submit" /> <br><br>
											
					%if result != '':
						Result: <br><br>
						<img src='{{result}}'><br>				
						Original: <br><br>
						<img src='{{original}}'>
					%end
				</form>			   
		 </div>		 
		 <div id="footer">		       
			   GliTch is powered by: Python - PIL - Bottle - Heroku 			   
	     </div>		 
   </div>
</body>
</html>
