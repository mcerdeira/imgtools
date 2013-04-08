<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<meta http-equiv="Cache-control" content="public">
<meta name="description" content="Glitch image transformation playground">
<meta name="keywords" content="image transformation glitch gleetch PIL python">
<title>GliTch Playground (beta)</title>
<link rel="stylesheet" type="text/css" href="/css/main.css"/>
</head>

<body>
   <div id="wrapper">		 
		 <div id="header">
			<div id="small">
				<img src="/img/logo.png"><br/>
			</div>			
         </div>

		 <br>
		 <br>		 
		 
		 <div id="content">		       
			   	<form method="post" action="/submited/">		
					Image Url: <input type="text" name="url" value="{{original}}" style="width: 500px"/><br><br>			
					Effects: <br><br>
					
					%for i in range(0, len(actions)-1):
					<input id="chk{{i}}" type="checkbox" name="{{actions[i]}}" value="{{actions[i]}}"> {{actions[i]}}<br>
					%end
					
					<br>
					
					<input type="submit" value="Submit" /> <br><br>
					%if result != '':
						Image Link:<br/><br/>
						<textarea rows="5" name="link" style="width: 520px; height: 84px;">{{result}}</textarea><br/><br/>			
						
						Embed:<br/><br/>
						<textarea rows="5" name="link" style="width: 520px; height: 84px;"><img src='{{result}}'></textarea><br/><br/>		
						
						Result: <br/><br/>
						<img src='{{result}}'><br/>				
						Original: <br/><br/>
						<img src='{{original}}'>
					%else:
						Wanna try it? <a href="https://github.com/mcerdeira/imgtools/blob/master/README.md" TARGET="_new">Read the docs </a>
						or maybe you wanna <a href="mailto:martincerdeira@gmail.com">Contact Us!</a>
					%end
				</form>			   
		 </div>
		 <div id="footer">
			   GliTch is powered by: Python - PIL - Bottle - Heroku 			   
	     </div>		 
   </div>
</body>
</html>
