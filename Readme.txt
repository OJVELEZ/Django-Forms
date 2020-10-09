Crear ambiente virtual	
	
	1-pip install virtualenv
	2-virtualenv venvf
	3-cd venvf/Scripts
	4-Ejecutar activate.bat
		en linux o mac source venv(bin/activate)
	5-Desde el ambiente virtual	
		pip install django
	6-Crear proyecto en django llamado JuanisPizza
		django-admin startproject JuanisPizza
	7-Renombrar carpeta JuanisPizza -> JuanisPizza-project 
	8-Iniciar servidor 
		python manage.py runserver
	9-Crear app pizza
		django-admin  startapp pizza
	10-Editar urls.py
		path('', views.home, name='home'),
		path('order', views.order, name='order'),
	11-Editar settings agregar la app pizza	en INSTALLED_APPS	
		'pizza',
	12-Editar views.py 
		def home(request):
			return render(request, 'pizza/home.html')

		def order(request):
			return render(request, 'pizza/order.html')	
	13- Crear directorios
			templates/pizza			
			archivos
				home.html
				order.html
	14-home.html		
		<h1>Juanis Pizza</h1>
		<a href="{% url 'order' %}">Ordenar una pizza</a>
	
	15-order.html
		Se debe colocar en el action
			la página hacia donde se dirige luego del submit	
				acá se queda en order
			el metodo si funcionará como get o post
				get
					http://localhost:8000/order?topping1=23&topping2=22&size=Small
					Cuando quiere a futuro referenciar alguno de los parametros
					Cuando no va a cambiar
					
				post
					http://localhost:8000/order
					Cuando va a cambiar
					no se ven los parametros
					
			

		<form action="{ url 'order'}" method="get">  
			<label for="topping1">Escoge Topping 1:</label>
			<input id="topping1" type="text" name="topping1" >  

			<label for="topping2">Escoge Topping 2:</label>
			<input id="topping2" type="text" name="topping2" >    
			
			<label for="size">Escoge el tamaño:</label>
			<select id="size" name="size" >
				<option value="Small">Personal</option>
				<option value="Medium">Mediana</option>
				<option value="Large">Familiar</option>
			</select>
			<input type="submit" value="Ordenar">
		</form>
	
		
		16-Probar formularion order
			csrf ERROR
			Cross site scripting error
			Se debe adicionar despues del form action	
				{% csrf_token %}
				
			reiniciar servidor y funciona


		17-Crear archivo pizza/forms.py
			from django import forms

			class PizzaForm(forms.Form):
				topping1 = forms.CharField(label='Escoge Topping 1', max_length=100)
				topping2 = forms.CharField(label='Escoge Topping 2', max_length=100)
				size = forms.ChoiceField(label='Tamaño', choices=[('Personal', 'Small'), ('Mediana', 'Medium'), ('Familiar', 'Large')])		
				
				
		18-Editar views.py
			agregar
				from .forms import PizzaForm
			editar 	
				def order(request):
					form = PizzaForm() 
					return render(request, 'pizza/order.html', {'pizzaform': form}) //LE PASA POR PARAMETRO LA CLASE PIZZAFORM PARA QUE LA RENDERICE
				
		19-Editar order.html
			Borrar el código que habiamos hecho relacionado a label, input y select, excepto el submit
			Reemplazar por
				<form action="{% url 'order' %}" method="post">
					{% csrf_token %}
					{{ pizzaform }} //Esta linea reemplaza todo el copdigo!!! realizar en render de lo definido en la clase PizzaForm de forms.py
					<input type="submit" value="Ordenar">
				</form>
			
		20-Capturar los parametros enviados por POSTS
			En views.py
				def order(request):
					if request.method == "POST":
						filled_form = PizzaForm(request.POST)
						if filled_form.is_valid():
							note = 'Gracias por ordenar su Pizza %s de %s y %s , la prepararemos con agilidad y cariño :)' %(filled_form.cleaned_data['size'],
							filled_form.cleaned_data['topping1'],
							filled_form.cleaned_data['topping2'])
							new_form = PizzaForm()
							return render(request, 'pizza/order.html', {'pizzaform': new_form, 'note': note})
					else:
						form = PizzaForm()
						return render(request, 'pizza/order.html', {'pizzaform': form})
						
			En order.html agregar		
					<h2>{{ note }}</h2>
					
		21-Almacenar en Base de datos, editar models.py
		
			class Size(models.Model):
				title = models.CharField(max_length=100)
				def __str__(self):
					return self.title
			class Pizza(models.Model):
				topping1 = models.CharField(max_length=100)
				topping2 = models.CharField(max_length=100)
				size = models.ForeignKey(Size, on_delete=models.CASCADE)	
		
		22-Editar admin.py en pizza para que sean administrables desde admin de django
			from.models import Pizza,Size

			admin.site.register(Pizza)
			admin.site.register(Size)

		23-Ejecutar la migracion
			python manage.py makemigrations
			python manage.py migrate
			python manage.py showmigrations
			
			Crear un superuser
				python manage.py createsuperuser
				ovelez, 12345678
				
		24-Crear una form model
			Comentar Pizza for en forms.py
			IMPORTANTE debe heredar de forms.ModelForm sino no funciona
			
			class PizzaForm(forms.ModelForm):
				class Meta:
						model = Pizza
						fields = ['topping1', 'topping2', 'size']
			

		25-Pruebas de widgets
			comentar la clase Pizzaform
			descomentar la anterior y probar esto
				toppings = forms.MultipleChoiceField(choices=[('pep','Pepperoni'),('cheese','Queso'),('cam','Camarones')], widget=forms.CheckboxSelectMultiple)
				class PizzaForm(forms.ModelForm):
					class Meta:
							model = Pizza
							fields = ['topping1', 'topping2', 'size']
							labels = {
							"topping1": "Escoge Topping 1",
							"topping2": "Escoge Topping 2",
							}
							widgets = {'size':forms.CheckboxSelectMultiple}		

				class PizzaForm(forms.ModelForm):
							size = forms.ModelChoiceField(queryset=Size.objects, empty_label=None, widget=forms.RadioSelect)
							class Meta:
									model = Pizza
									fields = ['topping1', 'topping2', 'size']
									labels = {
									"topping1": "Escoge Topping 1",
									"topping2": "Escoge Topping 2",
									}					
		
		26-Aceptar datos del usuario
			editar order.html
				actual: <form action="{% url 'order' %}" method="post">
				cambiar por: <form enctype="multipart/form-data" action="{% url 'order' %}" method="post">
				
			pip install pillow /Vam,os a necesitar para trabajar con imagenes

			forms.py	
				class PizzaForm(forms.ModelForm):
					image = forms.ImageField()
			
			views.py
				filled_form = PizzaForm(request.POST, request.FILES)
				
			Probar y luego reversar cambios
			
		27-FormSet permite tomar una forma y repetirla varias veces
			Para el ejemplo, una persona podría pedir varias pizzas usando el mismo form
				
			Editar order.html
				<br> </br>

				Quieres más de una pizza?

				<form action="{% url 'pizzas' %}" method="get">
					{{ multiple_form }}
					<input type="submit" value="Get Pizzas">
				</form>			
				
		28- Editar urls.py
			path('pizzas', views.pizzas, name='pizzas'),
			
			Editar forms.py
				class MultiplePizzaForm(forms.Form):
					number = forms.IntegerField(min_value=2, max_value=6)
			
				
			
			
			
		
					
		
		
			
			
			
				
			
		
		
		
			
				
				
			
			
			
		
		
	