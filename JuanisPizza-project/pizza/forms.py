from django import forms
from .models import Pizza, Size

# class PizzaForm(forms.Form):
#     topping1 = forms.CharField(label='Escoge Topping 1', max_length=100)
#     topping2 = forms.CharField(label='Escoge Topping 2', max_length=100)
#     size = forms.ChoiceField(label='Tamaño', choices=[('Small', 'Personal'), ('Medium', 'Mediana'), ('Large','Familiar')])


class PizzaForm(forms.ModelForm):
    
    class Meta:
            model = Pizza
            fields = ['topping1', 'topping2', 'size']
            labels = {
            "topping1": "Escoge Topping 1",
            "topping2": "Escoge Topping 2",
            }
            

class MultiplePizzaForm(forms.Form):
    number = forms.IntegerField(min_value=2, max_value=6)
