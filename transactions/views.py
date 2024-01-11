from django.shortcuts import render
from .form import AddMoneyForm
from accounts.models import UserBookAccount
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from post.models import Post
from accounts.models import PurchaseModel
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages


# mail send korar function
def send_mail_to_user(user, subject, template, added_amount=None):
    # Retrieve the user account
    user_account = UserBookAccount.objects.get(user=user)

    # Calculate the total balance
    total_balance = user_account.balance

    # If an added amount is provided, update the balance
    if added_amount is not None:
        user_account.balance += added_amount
        total_balance = user_account.balance
        user_account.save()

    message = render_to_string(template, {
        'user': user,
        'amount': added_amount,  # Pass the added amount to the template
        'total_balance': total_balance  # Pass the total balance to the template
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


@login_required
def addMoney(request):
    form = AddMoneyForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        amount = form.cleaned_data['amount']

        user_account = UserBookAccount.objects.get(user=request.user)
        user_account.balance += amount
        user_account.save()

        send_mail_to_user(request.user, "Successfully Added Money",
                          "addMoneyEmail.html", added_amount=amount)
        return render(request, 'home')

    return render(request, 'addMoney.html', {'form': form})


class BuyBookView(View):
    def get(self, request, id):
        book = get_object_or_404(Post, pk=id)
        user_account = request.user.account
        user = user_account.user
        if user_account.balance >= book.price:
            user_account.balance -= book.price
            user_account.save()
            book.save()
            purchase = PurchaseModel.objects.create(
                user=request.user, book=book)
            purchase.save()
            return render(request, 'home', {'book': book})

        else:
            messages.warning(
                request, "You cannot purchase a book with insufficient balance.")
            send_mail_to_user(
                request.user, "Book Purchase Failed", "purchaseFailEmail.html")
            return redirect('home')
