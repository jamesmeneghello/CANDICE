<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
		<link rel="stylesheet" href="/static/styles/bootstrap-1.3.0.min.css" />
		<script type="text/javascript" src="/static/scripts/jquery-1.6.3.min.js"></script>

		<style type="text/css">
			html {overflow: hidden;}
			body
			{
				margin: 0;
				padding: 0;
				margin-top:40px;
				
			}
			#iframe {overflow: hidden;}
			#iframe, iframe
			{
				width: 100%;
				height: 100%;
			}
		</style>

		<script type="text/javascript">
			$(document).ready(main);

			function main()
			{
				registerEvents();
				resizeFrame();
			}

			function registerEvents()
			{
				$(window).resize(function(){resizeFrame();});
			}

			function resizeFrame()
			{
				$("#iframe").height(WindowHeight() - getObjHeight(document.getElementById("toolbar")));
			}

			function WindowHeight()
			{
				var de = document.documentElement;
				return self.innerHeight || (de && de.clientHeight) || document.body.clientHeight;
			}

			function getObjHeight(obj)
			{
				if (obj.offsetWidth)
				{
					return obj.offsetHeight;
				}

				return obj.clientHeight;
			}
		</script>
	</head>

	<body>
		{% block topbar %}{% endblock %}

		{% block content %}{% endblock %}
	</body>
</html>