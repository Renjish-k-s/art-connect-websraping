from django.shortcuts import render,redirect
from .models import Artisttable,Arttable,Usertable,Ordertable
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # Import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Usertable, Arttable, Ordertable, Artisttable,Message
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q  

def get_user_messages(request, other_user_id):
    """
    Retrieve messages between the current user and another user
    """
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'User not logged in'}, status=401)
    
    current_user_id = request.session['user_id']
    
    # Fetch messages between the two users using Q objects
    messages = Message.objects.filter(
        Q(sender_id=current_user_id, receiver_id=other_user_id) | 
        Q(sender_id=other_user_id, receiver_id=current_user_id)
    ).order_by('timestamp')
    
    # Mark messages as read
    Message.objects.filter(
        Q(sender_id=other_user_id, receiver_id=current_user_id, is_read=False)
    ).update(is_read=True)
    
    # Convert messages to a list of dictionaries
    message_list = [{
        'sender': msg.sender_id,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime("%I:%M %p"),
        'is_read': msg.is_read
    } for msg in messages]
    
    return JsonResponse({'messages': message_list})

def get_user_list(request):
    """ Retrieve list of all users with their last message and unread count, sorted by unread messages """
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'User not logged in'}, status=401)

    current_user_id = request.session['user_id']

    # Fetch all users except the current user
    users = Usertable.objects.exclude(id=current_user_id)

    user_list = []
    for user in users:
        # Get the last message (if any) using Q objects
        last_message = Message.objects.filter(
            Q(sender_id=current_user_id, receiver_id=user.id) |
            Q(sender_id=user.id, receiver_id=current_user_id)
        ).order_by('-timestamp').first()

        # Count unread messages
        unread_count = Message.objects.filter(
            sender_id=user.id, receiver_id=current_user_id, is_read=False
        ).count()

        user_data = {
            'id': user.id,
            'name': user.name,
            'avatar': user.name[:2].upper(),
            'last_message': last_message.content if last_message else 'No messages yet',
            'time': last_message.timestamp.strftime("%I:%M %p") if last_message else '',
            'unread': unread_count
        }
        user_list.append(user_data)

    # Sort users by unread messages count in descending order
    user_list.sort(key=lambda x: x['unread'], reverse=True)

    return JsonResponse({'users': user_list})


@csrf_exempt
def send_message(request):
    """
    Send a new message
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'User not logged in'}, status=401)
    
    sender_id = request.session['user_id']
    receiver_id = request.POST.get('receiver_id')
    content = request.POST.get('content')
    
    if not receiver_id or not content:
        return JsonResponse({'error': 'Missing receiver or content'}, status=400)
    
    # Create new message
    new_message = Message.objects.create(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        timestamp=timezone.now(),
        is_read=False
    )
    
    return JsonResponse({
        'message': {
            'sender': sender_id,
            'content': content,
            'timestamp': new_message.timestamp.strftime("%I:%M %p")
        }
    })


























def art_upload(request):
    id = request.session.get('user_id', 1)  # Default to 1 for testing, use session ID in production
    results = Usertable.objects.filter(id=id)  # Get user details
    details = Artisttable.objects.filter(userid=id)  # Get artist details
    art_list = Arttable.objects.filter(userid=id, status=1)  # Get user art list

    if request.POST:
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        price = request.POST.get("price")
        arttype = request.POST.get("arttype")
        img = request.FILES.get("img")

        if img:
            fs = FileSystemStorage(location="media/art_photos/")
            filename = fs.save(img.name, img)
            file_url = f"art_photos/{filename}"
        else:
            file_url = ""  # Handle case when no image is uploaded

        Art_obj = Arttable(title=title, desc=desc, price=price, img=file_url, userid=id, status=1, arttype=arttype)
        Art_obj.save()
        messages.success(request, "Art uploaded successfully!")  # Success message

    # Fetch orders for the user's products
    user_products = Arttable.objects.filter(userid=id).values_list('id', flat=True)
    orders = Ordertable.objects.filter(product_id__in=user_products)

    order_details = []
    for order in orders:
        try:
            buyer = Usertable.objects.get(id=order.user_id)  # Buyer details
            product = Arttable.objects.get(id=order.product_id)  # Product details

            order_details.append({
                "buyer_name": buyer.name,
                "buyer_email": buyer.email,
                "product_title": product.title,
                "price": product.price,
                "del_date": order.delivery_date,
                "order_id": order.id  # Needed for passing order ID in the button
            })
        except Usertable.DoesNotExist:
            continue  # Skip if buyer does not exist
        except Arttable.DoesNotExist:
            continue  # Skip if product does not exist

    # ✅ Merge `context` properly
    context = {
        'results': results,
        'details': details,
        'art_list': art_list,
        'orders': order_details  # Include orders in the context
    }

    return render(request, 'artist_registered.html', context)




def artist_page(request):
    return render(request,'artist.html')



def artist_reg(request):
    id = request.session.get('user_id')  # Default to 7 for testing, use session ID in production
    results = Usertable.objects.filter(id=id)  # Get user details

    context = {
        'results': results  # Pass queryset to the template
    }

  


    if request.POST and request.FILES.get("profile_photo"):
        bio=request.POST.get("bio")
        phone=request.POST.get("phone")
        location=request.POST.get("location")
        insta=request.POST.get("insta")
        website=request.POST.get("website")

        selected_categories = request.POST.getlist('art_cat')  # Get selected checkboxes
        categories_str = ",".join(selected_categories)

        profile_photo = request.FILES["profile_photo"]
        fs = FileSystemStorage(location="media/profile_photos/")
        filename = fs.save(profile_photo.name, profile_photo)
        file_url = f"profile_photos/{filename}"  # Relative path for the database

        
        Usertable.objects.filter(id=id).update(status=1)
        Artisttable_obj=Artisttable(bio=bio,phone=phone,location=location,insta=insta,website=website,art_categories=categories_str,profile_photo=file_url,userid=id)
        Artisttable_obj.save()
    return render(request,'artist_dash.html',context)


@csrf_exempt
def update_delivery_date(request, order_id):
    if request.method == "POST":
        new_date = request.POST.get("date_delivery")  # Get date from form
        try:
            order = Ordertable.objects.get(id=order_id)
            order.delivery_date = new_date  # Update delivery date
            order.save()  # Save changes
            return redirect('art_upload')  # Redirect after updating
        except Ordertable.DoesNotExist:
            return HttpResponse("Order not found", status=404)
    return redirect('art_upload')















def artist_dash(request):

    return render(request, 'artist_dash.html')







