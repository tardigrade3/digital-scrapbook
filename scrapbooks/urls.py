'''
URL paths for scrapbook app

Mar 19 2024 - added "new/" path
Mar 27 2024 - added "save/" path
Apr 10 2024 – added "edit_media/" path
Apr 12 2024 – added "confirm_delete/" and "delete/" paths for Media objects
May 19 2024 - added "confirm_delete/" and "delete/" paths for Scrapbook objects
'''

from django.urls import path
from . import views
urlpatterns = [
    path("new/", views.new_scrapbook_project, name="new_scrapbook"), # the view where the user enters information to create a new scrapbook project
    path("<str:scrapbook_id>/", views.scrapbook_project, name="scrapbook_project"), # the view where the user can upload content to a scrapbook progect
    path("<str:scrapbook_id>/save/", views.create_pdf, name="create_pdf"), #the view which allows the user to create a pdf of their images_in_static and text
    path("<str:scrapbook_id>/edit/", views.edit_scrapbook, name="edit_scrapbook"), # the view where the user can edit the settings of a scrapbook project
    path("<str:scrapbook_id>/confirm_delete/", views.confirm_delete_scrapbook, name="confirm_delete_scrapbook"), # view to confirm delete of scrapbook project
    path("<str:scrapbook_id>/delete/", views.delete_scrapbook, name="delete_scrapbook"), # delete scrapbook project
    path("<str:scrapbook_id>/<int:media_id>/", views.edit_media, name="edit_media"), # the view where the user can edit a media object
    path("<str:scrapbook_id>/<int:media_id>/confirm_delete/", views.confirm_delete_media, name="confirm_delete_media"), # the view where the user can delete a media object
    path("<str:scrapbook_id>/<int:media_id>/delete/", views.delete_media, name="delete_media"), # the view where the user can delete a media object
]