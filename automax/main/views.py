from django.shortcuts import render,HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  Listing,LikedListing
from .forms import ListingForm
from users.forms import LocationForm 
from django.contrib import messages
from django.shortcuts import redirect
from .filters import ListingFilter
from django.http import JsonResponse
from imp import reload

def main_view(request):
    return render(request, "views/main.html", {"name": "AutoMax"})


@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    user_liked_listings = LikedListing.objects.filter(
        profile=request.user.profile).values_list('listing')
    liked_listings_ids = [l[0] for l in user_liked_listings]
    context = {
       
        'listing_filter': listing_filter,
        'liked_listings_ids': liked_listings_ids,
       
    }
    return render(request, "views/home.html",context)

@login_required
def list_view(request):
     if request.method == 'POST':
            try:
                listing_form = ListingForm(request.POST, request.FILES)
                location_form = LocationForm(request.POST, )
                if listing_form.is_valid() and location_form.is_valid():
                    listing = listing_form.save(commit=False)
                    listing_location = location_form.save()
                    listing.seller = request.user.profile
                    listing.location = listing_location
                    listing.save()
                    messages.info(
                        request, f'{listing.model} Listing Posted Successfully!')
                    return redirect('home')
                else:
                    raise Exception()
            except Exception as e:
                print(e)
                messages.error(
                    request, 'An error occured while posting the listing.')
     elif request.method == 'GET':
         listing_form = ListingForm()
         Location_Form = LocationForm()
     return render(request, 'views/list.html', {'listing_form': listing_form,'Location_Form': Location_Form})
         

@login_required
def listing_view(request,id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        
        return render(request,'views/listing.html', {'listing': listing, })
    except Exception as e :
        messages.error(
                    request, 'An error occured while  the listing.')
        print(e)
        return redirect('home')
    
    
@login_required
def edit_view(request,id):
    try:
        print(id)
        listing= Listing.objects.get(id=id)
        if listing  is None:
            raise Exception
        
        
        if request.method == 'POST':
            listing_form = ListingForm(
                request.POST, request.FILES, instance=listing)
            location_form = LocationForm(
                request.POST, instance=listing.location)
            if listing_form.is_valid and location_form.is_valid:
                listing_form.save()
                location_form.save()
                messages.info(request, f'Listing {id} updated successfully!')
                return redirect('home')
            else:
                messages.error(
                    request, f'An error occured while trying to edit the listing.')
                return reload()
            
        else :
            listing_form= ListingForm(instance=listing)
            location_form =LocationForm(instance=listing.location)
        context={
            'listing_form':listing_form,
            'location_form':location_form
                
        }
        return render(request,'views/edit.html',context)
    except Exception as e :
        messages.error(request,"An something error is occur while updating your listing ")
        return redirect('home')
    

@login_required
def like_listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)

    liked_listing, created = LikedListing.objects.get_or_create(
        profile=request.user.profile, listing=listing)

    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()

    return JsonResponse({
        'is_liked_by_user': created,
    })