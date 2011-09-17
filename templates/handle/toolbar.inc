{% extends 'handle/base.inc' %}

{% block topbar %}
	<div id="toolbar" class="topbar">
		<div class="fill">
			<div class="container">
				<h3><a href="#">CANDICE</a></h3>
				{% block barcontent %}{% endblock %}
				<ul class="nav">
					<li><a href="{{url|safe}}">Request Site</a></li>
				</ul>
			</div>
		</div>
	</div>
{% endblock %}

{% block content %}
<div id='iframe'>
	<iframe src="{{page|safe}}"></iframe>
</div>
{% endblock %}