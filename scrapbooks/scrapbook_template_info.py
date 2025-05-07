'''
Everything about scrapbook themes
History
Apr 16 2024 - file creation
Apr 17 2024 - added blue_flowers theme, added rotation attribute to Box
'''

class Box():
    '''
    A class to represent dimensions of an image or textbox (in cm)
    Attributes:
        x (float): x-coordinate of the bottom left corner on cartesian plane
        y (float): y-coordinate of the bottom left corner on cartesian plane
        width (float): width of the box
        height (float): height of the box
        rotation (float = 0): rotation of the box (degrees counterclockwise)
    '''

    def __init__(self, x, y, width, height, rotation=0.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation

class Theme():
    '''
    Stores information about themes
    Attributes:
        image_pos_list (list of Box): positions of images on each page of a scrapbook
        captions_pos_list (list of Box): positions of captions for each image
        bg (string): file path of the background image of the template (should be A4 size and stored in scrapbooks/static)
        title_pos (Box): position of scrapbook title on page
        title_font (str = 'Helvetica'): font of title (must be a reportlab default or name of .ttf file stored in reportlab/fonts)
        title_size (float = 40): font size of title
        title_align (int = 0): alignment of title as int for reportlab's StyleSheet.alignment
        caption_font (str = 'Helvetica'): font of title (must be a reportlab default or name of .ttf file stored in reportlab/fonts)
        caption_size (float = 12): font size of title
        caption_align (int = 0): alignment of caption as int for reportlab's StyleSheet.alignment
        media_num (int = 4): the number of media objects per page
    '''
    def __init__(self, image_pos_list, captions_pos_list, bg, title_pos,
                 title_font='Helvetica', title_size='40', title_align=0,
                 caption_font='Helvetica', caption_size=12, caption_align=0,
                 media_num=4):

        self.media_num = media_num
        self.image_pos_list = image_pos_list
        self.captions_pos_list = captions_pos_list
        self.bg = bg
        self.title_pos = title_pos
        self.title_font = title_font
        self.title_size = title_size
        self.title_align = title_align
        self.caption_font = caption_font
        self.caption_size = caption_size
        self.caption_align = caption_align

# theme 1
blue_flowers = Theme(image_pos_list=[Box(1.56, 17.53, 8.48, 8.47, 6.9),
                                     Box(12.09, 16.19, 8.65, 8.63, -8.3),
                                     Box(1.22, 5.85, 8.62, 8.61, -8.1),
                                     Box(11.57, 0.71, 8.9, 8.87, -10.6)],
                   captions_pos_list=[Box(1.56, 14.33, 8.48, 3),
                                     Box(12.09, 24.82, 8.65, 2.5),
                                     Box(1.22, 2.65, 8.62, 3),
                                     Box(11.57, 9.58, 8.9, 2.5)],
                   bg='static/template1BG.png',
                   title_pos=Box(0.66, 14.77, 19.69, 1.1),
                   title_font='Daughter_of_Fortune',
                   title_size=25,
                   title_align=1,
                   caption_font='Times-Roman',
                   caption_size=12)

# theme 2
pink_stars = Theme(image_pos_list=[Box(1.7, 15.95, 8.28, 8.28),
                                   Box(11.64, 18.19, 8.28, 8.28),
                                   Box(1.8, 3.3, 8.28, 8.28),
                                   Box(11.42, 6.12, 8.28, 8.28)],
                   captions_pos_list=[Box(1.7, 12.95, 8.28, 3),
                                      Box(11.64, 15.19, 8.28, 3),
                                      Box(1.8, 0.3, 8.28, 3),
                                      Box(11.42, 3.12, 8.28, 3)],
                   bg='static/template2BG.png',
                   title_pos=Box(3.32, 26.82, 16.6, 1.88),
                   title_font='Daughter_of_Fortune',
                   title_size=45,
                   caption_font='Helvetica',
                   caption_size=10,
                   caption_align=1)

# dictionary of themes for each template
themes = {
    'template1': blue_flowers,
    'template2': pink_stars
}