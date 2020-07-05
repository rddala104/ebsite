# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from datetime import datetime
from ebsite.models import *
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactForm,RegisterForm, RegisterFormUpdate, AddAddress, MurForm
from base64 import b64encode
from django.views import generic
from django.views.generic import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe


def home(request):  
    return render(request, 'ebsite/mapage.html')
        
def list_articles(request, year, month=1):
    return HttpResponse('Articles de %s/%s' % (year, month)) 

def detail(request, id):
    try:
        essai = Articles.objects.filter(id=id)
        return render(request, 'ebsite/lire.html', {'essai':essai})
    except Articles.DoesNotExist:
        return render(request, 'ebsite/lire.html', {'error': 'No data found.'})
  
def view_article(request, id_article):
    if id_article > 100:
        return redirect('afficher_article', id_article=42)
    return HttpResponse('<h1>Mon article ici</h1>')

    
def view_redirection(request):
    return HttpResponse('Vous avez été redirigé')

def boutique(request):
    # article = Articles.objects.all()
    article = Articles.objects.get_queryset().order_by('id')
    paginator = Paginator(article, 8)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    context = {
        'articles':articles,
        'paginate': True
    }   
    return render(request, 'ebsite/addition.html', context)
    
def bienvenito(request):
    return render(request,'ebsite/bienvenue.html') 

def muraidee(request):
    murs=mur.objects.all()
    return render(request,'ebsite/murmessage.html', {'murs':murs}) 

@login_required(login_url='/sign-in')
def envoimess(request):
    murs=mur.objects.all()
    # client = get_object_or_404(Client, user_id=request.user.id)
    # cart_message = mur(message=message, pseudo=prenom_contact)
    # cart_message.save()
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # add_address_form = AddAddress(request.POST)
        form = MurForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            pseudo = form.cleaned_data['pseudo']
            message = form.cleaned_data['message']
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            cart_message = mur(message=message, pseudo=pseudo)
            cart_message.save()
            return render(request,'ebsite/mercimessage.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MurForm()

    return render(request, 'ebsite/murmessage.html', {'form': form,'murs':murs})

@login_required(login_url='/sign-in')
def authentification(request):
    client = get_object_or_404(Client, user_id=request.user.id)
    contact = Contact.objects.filter(client_id=client.id)
    return render(request, 'ebsite/authentification.html', {'contact':contact})
    
def contact(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ContactForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']
        envoyeur = form.cleaned_data['envoyeur']
        renvoi = form.cleaned_data['renvoi']

        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        envoi = True
    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'ebsite/contact.html', locals())

def sign_in(request):
    if request.user.is_authenticated:
        return redirect(reverse('authentification'))
    else:
        form = RegisterForm()


        if request.method == 'POST':
            if 'register' in request.POST:
                form = RegisterForm(request.POST)
                if form.is_valid():
                    # On crée l'utilisateur et le client
                    user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                                first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    client = Client(user_id=user.id)
                    client.save()

                    # On connecte le client
                    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)

                    if request.GET.get('next', False):
                        return redirect(request.GET['next'])
                    else:
                        return redirect(reverse('authentification'))
            else:
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    if user.is_active:
                        client = Client.objects.filter(user_id=user.id).first()
                        __move_session_cart_to_database_cart(request, client.id)
                        login(request, user)
                        if request.GET.get('next', False):
                            return redirect(request.GET['next'])
                        else:
                            return redirect(reverse('authentification'))
                    else:
                        messages.add_message(request, messages.ERROR,
                                            'Votre compte a été désactivé, veuillez-contacter le service client.')
                else:
                    messages.add_message(request, messages.ERROR,
                                        'Les identifiants que vous avez saisis sont incorrects !')

        return render(request, 'ebsite/signin.html', {
            'get': request.GET,
            'form': form
        })     
        


def sign_out(request):
    logout(request)
    return redirect(reverse('bienvenue'))

def __move_session_cart_to_database_cart(request, client_id):
    """
    Cette fonction permet de copier le panier stocké en session d'un utilisateur non identifé vers la base de données
    juste avant son identification et supprime ensuite le panier stocké en session.
    :param request: l'objet request transmis depuis la fonction parent pour accéder à la session courante
    :param client_id: l'id du client
    :return:
    """
    if 'cart' in request.session:
        for product_id, qty in request.session['cart'].items():
            if CartLine.objects.filter(product_id=product_id, client_id=client_id).exists():
                cart_line = CartLine.objects.get(product_id=product_id, client_id=client_id)
                cart_line.quantity += int(qty)
            else:
                cart_line = CartLine(product_id=product_id, client_id=client_id, quantity=qty)
            cart_line.save()
        del request.session['cart']
    return


def __create_order_from_database_cart(request):
    """
    Cette fonction permet créer un objet Order et les objets OrderDetail associés à partir
    :param request:
    :return:
    """

    client = Client.objects.get(user_id=request.user.id)
    order = Order(status=Order.WAITING,
                  client_id=client.id,
                  shipping_address_id=request.session['shipping_address'],
                  invoicing_address_id=request.session['invoicing_address'],
                  order_date=datetime.now()
                  )
    order.save()

    cart = CartLine.objects.filter(client_id=client.id)
    for cart_line in cart:
        order_detail = OrderDetail(order_id=order.id,
                                   article_id=cart_line.product_id,
                                   qty=cart_line.quantity,
                                   product_unit_price=cart_line.product.prix_article,
                                   )
        order_detail.save()

    cart.delete()

    return order


def add_to_cart(request, product_id, qty):
    """
    Cette fonction permet d'ajouter un produit au panier. Si l'utilisateur n'est pas connecté, le produit est ajouté
    dans un panier virtuel géré grâce au système de sessions ; sinon, il est persisté en BDD.
    :type request:
    :param request:
    :param product_id: Id du produit à ajouter au panier
    :param qty: Nombre d'exemplaire du produit à ajouter au panier
    :return:
    """
    if not request.user.is_authenticated:
        if 'cart' not in request.session:
            cart = dict()
        else:
            cart = request.session['cart']

        if product_id in cart:
            cart[product_id] = int(cart[product_id]) + int(qty)
        else:
            cart[product_id] = qty

        request.session['cart'] = cart
    else:
        client = Client.objects.get(user_id=request.user.id)
        if CartLine.objects.filter(product_id=product_id, client_id=client.id).exists():
            cart_line = CartLine.objects.get(product_id=product_id, client_id=client.id)
            cart_line.quantity += int(qty)
        else:
            cart_line = CartLine(product_id=product_id, client_id=client.id, quantity=qty)
        cart_line.save()

    lien_panier = '<a style="margin-top:-7px" class="pull-right btn btn-default" href="' + reverse(
                  'display_cart') + '"><i class="fa fa-shopping-cart"></i> Voir le panier</a>'
    lien_dismit = '<button data-dismiss="alert" style="margin-top:-7px; margin-right:10px;" ' +\
                  'class="pull-right btn btn-default"><i class="fa fa-close"></i> Continuer mes achats</button>'
    messages.add_message(request, messages.SUCCESS,
                         'Le produit a été correctement ajouté à votre panier. ' + lien_panier + lien_dismit
                         )
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse('bienvenue'))


def clear_cart(request):
    """
    Cette fonction permet de vider le panier. Si l'utilisateur n'est pas connecté, la fonction vide le panier virtuel
    stocké en session ; sinon, les objets précédemment persistés en BDD sont supprimés.
    :param request:
    :return:
    """
    if not request.user.is_authenticated and 'cart' in request.session:
        del request.session['cart']
    else:
        client = Client.objects.get(user_id=request.user.id)
        CartLine.objects.filter(client_id=client.id).delete()

    return redirect(request.META.get('HTTP_REFERER'))


def display_cart(request):
    total = 0
    if not request.user.is_authenticated:
        if 'cart' in request.session:
            cart = list()
            for product_id, qty in request.session.get('cart').items():
                cart_line = CartLine(product_id=product_id, quantity=qty)
                total += cart_line.total()
                list.append(cart, cart_line)
        else:
            cart = None
    else:
        # client = Client.objects.get(user_id=request.user.id)
        client = get_object_or_404(Client, user_id=request.user.id)
        cart = CartLine.objects.filter(client_id=client.id)
        for cart_line in cart:
            total += cart_line.total()
    return render(request, 'ebsite/cart.html', {'cart': cart, 'grand_total': total})


@login_required(login_url='/sign-in')
def shipping(request):
    client = Client.objects.get(user_id=request.user.id)
    addresses_list = Contact.objects.filter(client_id=client.id)

    if request.method == 'POST' and request.POST['shipping_address'] and request.POST['invoicing_address']:
        request.session['shipping_address'] = int(request.POST['shipping_address'])
        request.session['invoicing_address'] = int(request.POST['invoicing_address'])

    if 'shipping_address' in request.session and 'invoicing_address' in request.session:
        shipping_address = request.session['shipping_address']
        invoicing_address = request.session['invoicing_address']
    else:
        shipping_address = 0
        invoicing_address = 0

    if request.GET.get('next', False):
        return redirect(request.GET['next'])
    else:
        return render(request, 'ebsite/shipping.html', {'addresses': addresses_list,
                                                 'shipping_address': shipping_address,
                                                 'invoicing_address': invoicing_address})


@login_required(login_url='/sign-in')
def add_address(request):
    if request.method == 'POST':
        add_address_form = AddAddress(request.POST)

        if add_address_form.is_valid():
            client = Client.objects.get(user_id=request.user.id)
            address = add_address_form.save(commit=False)
            address.client_id = client.id
            address.save()
            if request.GET.get('next', False):
                return redirect(request.GET['next'])
            else:
                redirect('addresses')
    else:
        add_address_form = AddAddress()
    return render(request, 'ebsite/add_address.html', {'add_address_form': add_address_form})


@login_required(login_url='/sign-in')
def checkout(request):

    if 'shipping_address' not in request.session or 'invoicing_address' not in request.session:
        return redirect(reverse('shipping'))

    total = 0
    client = Client.objects.get(user_id=request.user.id)
    cart = CartLine.objects.filter(client_id=client.id)
    for cart_line in cart:
        total += cart_line.total()
    total_cents = int(round(total*100))

    if request.method == 'POST':
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here https://dashboard.stripe.com/account
        stripe.api_key = "sk_test_y9cvSjqey9ynfA8UQ3Wupcxb00m4dMugtN"

        # Get the credit card details submitted by the form
        token = request.POST.get('stripeToken', None)

        order = __create_order_from_database_cart(request)

        # Create the charge on Stripe's servers - this will charge the user's card
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=total_cents,  # amount in cents, again
                    currency="eur",
                    card=token,
                    description='Charge for order ' + str(order.id)
                )
                order.status = Order.PAID
                order.stripe_charge_id = charge.id
                order.save()
                return redirect(reverse('confirmation'))
            except stripe.error.CardError:
                # The card has been declined
                pass
    return render(request, 'ebsite/checkout.html', {'cart': cart,
                                             'grand_total': total,
                                             'grand_total_cents': total_cents,
                                             'user_email': request.user.email})


@login_required(login_url='/sign-in')
def confirmation(request):

    return render(request, 'ebsite/confirmation.html')


@login_required(login_url='/sign-in')
def account(request):
    form = RegisterFormUpdate(instance=request.user)
    if request.method == 'POST':
        form = RegisterFormUpdate(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.add_message(request, messages.SUCCESS, "Vos informations ont été correctement mises à jour.")
            return redirect('account')
    return render(request, 'ebsite/account.html', {'form': form})


@login_required(login_url='/sign-in')
def orders(request):
    client = Client.objects.get(user_id=request.user.id)
    return render(request, 'ebsite/orders.html', {'orders': client.orders()})


@login_required(login_url='/sign-in')
def addresses(request):
    client = Client.objects.get(user_id=request.user.id)
    return render(request, 'ebsite/addresses.html', {'addresses': client.addresses()})


def handler404(request, exception):
     return render(request,'ebsite/404.html')

def handler500(request):
     return render(request,'ebsite/500.html')