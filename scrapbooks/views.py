'''
Views for the scrapbooks app
History:
Feb 23 2024 - improved documentation
Feb 29 2024 - scrapbook_project() view: added UploadContentForm to save Media object, raise 404 error if a scrapbook project does not exist
Mar 04 2024 - scrapbook_project(): tried unsuccessfully to make the form work properly
Mar 19 2024 - added new_scrapbook_project()
Mar 21 2024 - made new_scrapbook_project() less broken
Mar 25 2024 - fixed redirect when a new scrapbook is created
Mar 27 2024 - changes to new_scrapbook_project() because InfoForm was changed to a ModelForm, made edit_scrapbook() actually do stuff
Apr 02 2024 - included create_pdf(), fixed form in edit_scrapbook() & prepopulated the form with details from user_scrapbook
Apr 04 2024 - fixed create_pdf()
Apr 09 2024 - scrapbook_project(): include scrapbook media in context
Apr 12 2024 - added edit_media(), confirm_delete_media() and delete_media() views
Apr 15 2024 - create_pdf() now puts a scrapbook's media in a pdf, added ImageSettings class
Apr 16 2024 - moved ImageSettings to scrapbook_template_info.py (it is now named Box);
              in create_pdf():
              - the title and captions are now formatted as frames
              - the file name of the pdf is now based on the scrapbook title
              - the pdf now has a background image
              - most formatting settings are determined by a Theme object
Apr 17 2024 - create_pdf()s - fixed massive pdf size by resizing images, added support for themes with rotated images
May 19 2024 - caption field in media upload form in scrapbook_project() clears after submitting,
              added confirm_delete_scrapbook() and delete_scrapbook()
May 22 2024 - nonexistent Scrapbook or Media now raises a 404 error instead of 500
May 23 2024 - updated to reflect changes to names of html files
'''

# for page rendering & similar
from django.shortcuts import render, Http404, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseNotFound

# forms & models
from .models import Scrapbook, Media
from scrapbooks.forms import UploadContentForm, InfoForm, EditCaptionForm

# miscellaneous pdf generation stuff
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from scrapbooks.scrapbook_template_info import Box, Theme, themes
from PIL import Image

# ReportLab - fonts
import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# debugging
from pprint import pprint

reportlab.rl_config.warnOnMissingFontGlyphs = 0 # to avoid making reportlab angry

def scrapbook_project(request, scrapbook_id):
    '''
    The main page for a scrapbook project, where the user can upload media
    :param request:
    :param scrapbook_id: the scrapbook code of the scrapbook project the user is accessing
    :return:
    '''

    try:
        user_scrapbook = Scrapbook.objects.get(scrapbook_code=scrapbook_id) # the scrapbook project being accessed
    except Scrapbook.DoesNotExist:
        raise Http404()

    # save the media if POST
    if request.method == "POST":
        form = UploadContentForm(request.POST, request.FILES)
        if form.is_valid():
            new_media = Media(scrapbook=user_scrapbook, image=form.cleaned_data['image'], caption=form.cleaned_data['caption'])
            new_media.save()
            print(f'image location:{new_media.image}')
            form = UploadContentForm()
        else:
            print("the form isn't valid, that's why this isn't working.")

    # otherwise, just show the form
    else:
        form = UploadContentForm()

    context = {
        "scrapbook": user_scrapbook,
        "form": form,
        "scrapbook_media": user_scrapbook.media_set.all()
    }

    return render(request, "scrapbooks/scrapbook_project.html", context)

def edit_scrapbook(request, scrapbook_id):
    '''
    The page where the user can edit the settings of a scrapbook project
    :param request:
    :param scrapbook_id: the scrapbook code of the scrapbook project the user is accessing
    :return:
    '''

    try:
        user_scrapbook = Scrapbook.objects.get(scrapbook_code=scrapbook_id) # the scrapbook project being accessed
    except Scrapbook.DoesNotExist:
        raise Http404()

    # if this is a POST request, save the changes to the scrapbook
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = InfoForm(request.POST)
        print("it is indeed posting")
        # check whether it's valid, then update user_scrapbook & save changes
        if form.is_valid():
            print(f"BEFORE SAVING: name: {user_scrapbook.scrapbook_name}, theme: {user_scrapbook.scrapbook_theme}")
            user_scrapbook.scrapbook_name = form.cleaned_data['scrapbook_name']
            user_scrapbook.scrapbook_theme = form.cleaned_data['scrapbook_theme']
            user_scrapbook.save()
            print(f"AFTER SAVING: name: {user_scrapbook.scrapbook_name}, theme: {user_scrapbook.scrapbook_theme}")
    # if a GET (or any other method), prepopulate the form with details from user_scrapbook
    else:
        form = InfoForm(instance=user_scrapbook)

    context = {
        "scrapbook": user_scrapbook,
        "form": form
    }

    return render(request, "scrapbooks/edit_scrapbook_details.html", context)

def confirm_delete_scrapbook(request, scrapbook_id):
    '''
    view to confirm delete of a scrapbook project
    :param request:
    :param scrapbook_id: scrapbook code of Scrapbook object to be deleted
    :return:

    '''

    try:
        user_scrapbook = Scrapbook.objects.get(scrapbook_code=scrapbook_id)  # the scrapbook project being accessed
    except Scrapbook.DoesNotExist:
        raise Http404()

    context = {
        "scrapbook": user_scrapbook
    }

    return render(request, "scrapbooks/confirm_delete_scrapbook.html", context)

def delete_scrapbook(request, scrapbook_id):
    '''
    view for actually deleting a Media object (no associated html file, redirects to scrapbook_project())
    :param request:
    :param scrapbook_id: scrapbook_code of Scrapbook object to be deleted
    :return:
    '''

    try:
        user_scrapbook = Scrapbook.objects.get(scrapbook_code=scrapbook_id)  # the scrapbook project being accessed
    except Scrapbook.DoesNotExist:
        raise Http404()

    # delete the object and redirect to homepage
    user_scrapbook.delete()
    return HttpResponseRedirect("/")

def new_scrapbook_project(request):
    '''
    The page where the user can enter information to create a new scrapbook project
    :param request:
    '''

    # if this is a POST request, create the scrapbook and go to media upload
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = InfoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            created_scrapbook = Scrapbook.new_scrapbook(form.cleaned_data['scrapbook_name'], form.cleaned_data['scrapbook_theme']) # when InfoForm was a normal Form: Scrapbook.new_scrapbook(form.scrapbook_name, form.scrapbook_theme)
            print(f"newly created scrapbook {created_scrapbook}: name = {created_scrapbook.scrapbook_name}, theme = {created_scrapbook.scrapbook_theme}")
            created_scrapbook.save()
            # redirect to the page for uploading to the scrapbook corresponding to the entered code
            return HttpResponseRedirect(f"/Scrapbook_project/{created_scrapbook.scrapbook_code}/")

    # if a GET (or any other method), create a blank form
    else:
        form = InfoForm()

    context = {
        "form" : form
    }

    return render(request, "scrapbooks/new_scrapbook.html", context)

def create_pdf(request, scrapbook_id):
    '''
    Makes a pdf from a scrapbook's media
    :param request:
    :param scrapbook_id: the id of the scrapbook
    :return: the scrapbook pdf
    '''
    user_scrapbook = Scrapbook.objects.get(scrapbook_code=scrapbook_id)  # the scrapbook project being accessed
    response = HttpResponse(content_type='application/pdf')
    new_file_name = user_scrapbook.scrapbook_name.replace(' ', '_')
    response['Content-Disposition'] = f'attachment; filename="{new_file_name}.pdf"'

    user_scrapbook.scrapbook_name.replace(' ', '_') # name of pdf from scrapbook title

    theme = themes[user_scrapbook.scrapbook_theme]

    pdf_canvas = canvas.Canvas(response, pagesize=A4, pageCompression=1)

    # register fonts
    default_fonts = ['Courier', 'Courier-Bold', 'Courier-Oblique', 'Courier-BoldOblique',
    'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Helvetica-BoldOblique',
    'Times-Roman', 'Times-Bold', 'Times-Italic', 'Times-BoldItalic', 'Symbol','ZapfDingbats']

    if theme.title_font not in default_fonts:
        pdfmetrics.registerFont(TTFont(theme.title_font, f'{theme.title_font}.ttf'))
    if theme.caption_font not in default_fonts:
        pdfmetrics.registerFont(TTFont(theme.caption_font, f'{theme.caption_font}.ttf'))

    # set up caption formatting
    caption_style = getSampleStyleSheet()['Normal']
    caption_style.wordWrap = 'CJK' # wrapping
    caption_style.alignment = theme.caption_align
    caption_style.fontName = theme.caption_font
    caption_style.fontSize = theme.caption_size

    # set up title formatting
    title_style = getSampleStyleSheet()['Normal']
    title_style.wordWrap = 'CJK' # wrapping
    title_style.alignment = theme.title_align
    title_style.fontName = theme.title_font
    title_style.fontSize = theme.title_size

    # draw background & title on first page
    # background
    bg = ImageReader(theme.bg)
    pdf_canvas.drawImage(bg, 0, 0, 21 * cm, 29.7 * cm)

    # title
    title_pos = theme.title_pos
    title_frame = Frame(title_pos.x * cm, title_pos.y * cm, title_pos.width * cm, title_pos.height * cm,
                  id='normal')
    title = [Paragraph(user_scrapbook.scrapbook_name, title_style)]
    title_inframe = KeepInFrame(title_pos.width*cm, title_pos.height*cm, title)
    title_frame.addFromList([title_inframe], pdf_canvas)

    # pprint(vars(caption_style)) # prints all the attributes of caption_style for debugging

    for i in range(user_scrapbook.media_set.count()):
        # new page
        if i % theme.media_num == 0 and i != 0:
            pdf_canvas.showPage()
            # add background and title
            pdf_canvas.drawImage(bg, 0, 0, 21 * cm, 29.7 * cm)
            title_frame = Frame(title_pos.x * cm, title_pos.y * cm, title_pos.width * cm, title_pos.height * cm,
                          id='normal')
            title_frame.addFromList([title_inframe], pdf_canvas)

        # get dimensions for this image
        dimensions = theme.image_pos_list[i % theme.media_num]

        # convert image to usable format
        m = user_scrapbook.media_set.all()[i]
        image_data = Image.open(m.image)

        # for rotation of images - from https://stackoverflow.com/questions/5252170/specify-image-filling-color-when-rotating-in-python-with-pil-and-setting-expand
        #image_data = image_data.rotate(dimensions.rotation, expand=True)
        # converted to have an alpha layer
        im2 = image_data.convert('RGBA')
        # rotated image
        rot = im2.rotate(dimensions.rotation, expand=1)
        # a transparent image same size as rotated image
        all_transparent = Image.new('RGBA', rot.size, (0,) * 4)
        # create a composite image using the alpha layer of rot as a mask
        image_data = Image.composite(rot, all_transparent, rot)

        image_original_size = image_data.size # size of original image (rotated)

        # scale image
        width_factor = dimensions.width * cm / image_original_size[0]
        height_factor = dimensions.height * cm / image_original_size[1]
        scaling_factor = min(width_factor, height_factor)
        resolution_factor = 3 # set higher resolution factor for higher resolution images

        image_data = image_data.resize((int(image_original_size[0] * scaling_factor * resolution_factor), int(image_original_size[1] * scaling_factor * resolution_factor)), Image.ANTIALIAS)

        img = ImageReader(image_data)


        # draw image and caption on canvas
        pdf_canvas.drawImage(img, dimensions.x * cm + (dimensions.width * cm - img.getSize()[0] / resolution_factor) / 2,
                             dimensions.y * cm + (dimensions.height * cm - img.getSize()[1] / resolution_factor) / 2,
                             (img.getSize()[0] / resolution_factor), (img.getSize()[1] / resolution_factor), mask='auto')

        # draw caption
        caption_pos = theme.captions_pos_list[i % theme.media_num]
        caption_frame = Frame(caption_pos.x * cm, caption_pos.y * cm, caption_pos.width * cm, caption_pos.height * cm,
                      id='normal')
        caption_text = [Paragraph(m.caption, caption_style)]
        caption_inframe = KeepInFrame(caption_pos.width * cm, caption_pos.height * cm, caption_text, mode='overflow')
        caption_frame.addFromList([caption_inframe], pdf_canvas)
        # frame.drawBoundary(pdf_canvas) # for debugging

    pdf_canvas.save()

    return response

def edit_media(request, scrapbook_id, media_id):
    '''
    View to edit a Media object
    :param request:
    :param scrapbook_id: scrapbook_code of associated Scrapbook object
    :param media_id: primary key of Media object to be edited
    :return:
    '''

    try:
        user_scrapbook = Scrapbook.objects.get(scrapbook_code=scrapbook_id)  # the scrapbook project being accessed
    except Scrapbook.DoesNotExist:
        raise Http404()

    try:
        this_media = user_scrapbook.media_set.get(id=media_id) # the Media object
    except Media.DoesNotExist:
        raise Http404()


    # if this is a POST request, save the changes to the scrapbook
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = EditCaptionForm(request.POST)
        print("it is indeed posting")
        # check whether it's valid, then update user_scrapbook & save changes
        if form.is_valid():
            print(f"BEFORE SAVING: caption: {this_media.caption}")
            this_media.caption = form.cleaned_data['caption']
            this_media.save()
            print(f"AFTER SAVING: caption: {this_media.caption}")
    # if a GET (or any other method), prepopulate the form with the existing caption
    else:
        form = EditCaptionForm(instance=this_media)

    context = {
        "scrapbook": user_scrapbook,
        "this_media": this_media,
        "form": form
    }

    return render(request, "scrapbooks/edit_media.html", context)

def confirm_delete_media(request, scrapbook_id, media_id):
    '''
    view to confirm delete of a Media object
    :param request:
    :param scrapbook_id: scrapbook_code of associated Scrapbook object
    :param media_id: primary key of Media object to be deleted
    :return:
    '''

    try:
        user_scrapbook = Scrapbook.objects.get(scrapbook_code=scrapbook_id)  # the scrapbook project being accessed
    except Scrapbook.DoesNotExist:
        raise Http404()

    try:
        this_media = user_scrapbook.media_set.get(id=media_id)  # the Media object
    except Media.DoesNotExist:
        raise Http404()

    context = {
        "scrapbook": user_scrapbook,
        "this_media": this_media
    }

    return render(request, "scrapbooks/confirm_delete_media.html", context)

def delete_media(request, scrapbook_id, media_id):
    '''
    view for actually deleting a Media object (no associated html file, redirects to scrapbook_project())
    :param request:
    :param scrapbook_id: scrapbook_code of associated Scrapbook object
    :param media_id: primary key of Media object to be deleted
    :return:
    '''

    try:
        user_scrapbook = Scrapbook.objects.get(scrapbook_code=scrapbook_id)  # the scrapbook project being accessed
    except Scrapbook.DoesNotExist:
        raise Http404()

    try:
        this_media = user_scrapbook.media_set.get(id=media_id)  # the Media object
    except Media.DoesNotExist:
        raise Http404()

    # delete the object and redirect to the main scrapbook page
    else:
        this_media.delete()
        return HttpResponseRedirect(f"/Scrapbook_project/{user_scrapbook.scrapbook_code}/")
