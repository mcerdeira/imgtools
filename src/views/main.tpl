<html>
	<title>Image transformation playground </title>
	<head>	
	</head>
	<body>
		<h1>Image transformation playground</h1>
		<form method="post" action="/submited/">		
			Image Url: <input type="text" name="url" style="width: 500px"/><br><br>			
			Effects: <br><br>
			
			%for i in range(0, len(actions)-1):
			<input id="chk{{i}}" type="checkbox" name="{{actions[i]}}" value="{{actions[i]}}">{{actions[i]}}<br>
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
	</body>
</html>
