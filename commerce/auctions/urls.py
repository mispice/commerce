from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing,name="create_listing"),
    path("<int:listing_id>",views.listing_page,name="listing_page"),
    path("watchlist/<int:listing_id>",views.watchlist_create,name="watchlist"),
    path("display_watchlist",views.watchlist_display,name="watchlist_display"),
    path("placebid/<int:listing_id>",views.placebid,name="placebid"),
    path("your_listings",views.your_listings,name="your_listings"),
    path("close_bid/<int:listing_id>",views.close_bid,name="close_bid"),
    path("notifications",views.notifications, name="notifications"),
    path("comments/<int:listing_id>",views.comments,name="comments"),
    path("categories",views.categories,name="categories"),
    path("categorical_listing", views.categorical_listing,name="categorical_listing"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist,name="remove_watchlist")
]
