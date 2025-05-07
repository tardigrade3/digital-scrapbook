'''
Models for the scrapbooks app
History:
(forgot to add history until recently)
Feb 23 2024 - Improved documentation, added image attribute to Media
Mar 04 2024 - Altered Media.scrapbook, but now I think it's the same as it was before
Mar 19 2024 – added Irha's changes to Scrapbook class, created Email class, added theme choices
Apr 09 2024 - changed location of Media.image multiple times; made questionable life choices
Apr 14 2024 - updated scrapbook theme names
Apr 16 2024 - changed character limit for Scrapbook.scrapbook_name and Media.caption
Apr 17 2024 - removed default image for Media
May 20 2024 - added auto-delete for Media image files
'''
import os

from django.db import models
import uuid

from django.dispatch import receiver


class Scrapbook(models.Model):
    '''
    A class to represent a scrapbook project
    Attributes:
        :param scrapbook_code: a unique code to identify each scrapbook
        :param scrapbook_name: the title of the scrapbook
        :param scrapbook_theme: the theme layout
    '''
    scrapbook_code = models.CharField(max_length=6) # the code entered to access the scrapbook
    scrapbook_name = models.CharField(max_length=100)

    THEME_CHOICES = (
        ('template1', 'Blue Flowers'),
        ('template2', 'Pink Stars')
    )

    scrapbook_theme = models.CharField(max_length=100, default='template1', choices=THEME_CHOICES)

    def __str__(self):
        return self.scrapbook_code

    @classmethod
    def new_scrapbook(cls, name='Untitled Scrapbook', theme='template1'):
        '''
        Creates a new scrapbook project and generates a unique scrapbook code
        :param name: the name of the scrapbook
        :param theme: the theme of the scrapbook
        :return: Scrapbook
        '''
        return cls(scrapbook_code=uuid.uuid4().hex[:6].upper(), scrapbook_name=name, scrapbook_theme=theme)

class Media(models.Model):
    '''
    A class to represent a photo with a caption
    :param scrapbook: the key of the Scrapbook object the Media object belongs to
    :param caption: the caption of the photo
    :param image: the photo
    '''
    scrapbook = models.ForeignKey(Scrapbook, on_delete=models.CASCADE) # each Media object is related to a single Scrapbook
    caption = models.CharField(max_length=400)
    image = models.ImageField(upload_to='images/')

# from https://stackoverflow.com/questions/16041232/django-delete-filefield
@receiver(models.signals.post_delete, sender=Media)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding Media object is deleted.
    """

    if instance.image:
        if os.path.isfile(instance.image.path):
            print(f'deleting {instance.image.path}')
            os.remove(instance.image.path)
