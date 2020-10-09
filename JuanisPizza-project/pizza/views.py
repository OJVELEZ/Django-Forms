from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory

def home(request):
    return render(request, 'pizza/home.html')

def order(request):
    multiple_form = MultiplePizzaForm

    if request.method == "POST":
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            note = 'Gracias por ordenar su Pizza %s de %s y %s , la prepararemos con agilidad y cariño :)' %(filled_form.cleaned_data['size'],
            filled_form.cleaned_data['topping1'],
            filled_form.cleaned_data['topping2'])
            new_form = PizzaForm()
            return render(request, 'pizza/order.html', {'pizzaform': new_form, 'note': note, 'multiple_form': multiple_form})
    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaform': form, 'multiple_form':multiple_form})

def pizzas(request):
    number_of_pizzas = 2
    filled_mutiple_pizza_form = MultiplePizzaForm(request.GET)
    if filled_mutiple_pizza_form.is_valid():
        number_of_pizzas = filled_mutiple_pizza_form.cleaned_data['number']

    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()

    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            for form in formset:
                print(form.cleaned_data['topping1'])

            note = 'las Pizzas han sido ordenadas :)'    
        else:
            note = 'La orden no pudo ser procesada, por favor intenta nuevamente.'     
        return render(request, 'pizza/pizzas.html', {'note':note,'formset':formset})              
    else:
        return render(request, 'pizza/pizzas.html', {'formset':formset})    


        



