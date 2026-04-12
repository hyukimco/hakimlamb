import sys
import requests # Used to fetch data online

from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.bubble import Bubble
from kivy.uix.image import AsyncImage
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy_garden.mapview import MapView, MapMarkerPopup, MapSource
from kivy.uix.image import Image


class PopupLabel(BoxLayout):
    def __init__(self, text:str='Example', width=100, height=100, is_first=False, **kwargs):
        super(PopupLabel, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size      = [width, height]
        self.padding   = [0,0,0,0]

        # self.height   = height
        L = Label(
            text      = text,
            font_size = 12,
            text_size = self.size,
            halign    = "left",
            valign    = "top",
            size_hint = (1, 1),
            color     = (0, 0, 0, 1) # Black
        )
        L.size = L.texture_size
        self.add_widget(L)

class PopupButton(ButtonBehavior, Image):
    def __init__(self, source='', **kwargs):
        super(PopupButton, self).__init__(**kwargs)
        self.source        = source
        self.size_hint     = (None, None)
        self.size          = (15, 15)
        self.allow_stretch = True
        self.keep_ratio    = True  # Prevents distortion

class ToolButton(ButtonBehavior, Image):
    def __init__(self, source='', **kwargs):
        super(ToolButton, self).__init__(**kwargs)
        self.source        = source
        self.size_hint     = (None, None)
        self.size          = (40, 40)
        self.allow_stretch = True
        self.keep_ratio    = True  # Prevents distortion

class CustomBubble(Bubble):
    def __init__(
        self,
        main_text   = "Main text. ",
        authorship  = "Authorship",
        origin      = "Origin",
        target      = "Target",
        **kwargs
        ):
        wid      = 400
        hei      = 100
        side_pad = 20
        b_pad    = 2
        t_pad    = 1
        super(CustomBubble, self).__init__(**kwargs)
        with self.canvas.before:
            Color(rgba = (0.8, 0.8, 0.8, 1)) # Gray
            RoundedRectangle(pos   = [self.pos[0],  self.pos[1]  ], 
                            size   = [wid, hei ], 
                            radius = [10]
                            )
            Color(rgba = (1, 1, 1, 1))       # White
            RoundedRectangle(pos    = [self.pos[0]+side_pad, self.pos[1]+b_pad ], 
                             size   = [wid-2*side_pad, hei-t_pad-b_pad ], 
                             radius = [12]
                             )

        box_layout = BoxLayout(orientation="horizontal")
        left_box   = BoxLayout(orientation = "vertical", 
                               padding     = [side_pad+4, 40, 4, 0],
                               spacing     = 0,
                               size_hint   = (None, 1),
                               width       = wid-side_pad )

        txt = """This is an example text.
        """
        left_box.add_widget( PopupLabel( width=wid-2*side_pad, height=hei*0.5, text = txt,        is_first = False
                                           ) )
        left_box.add_widget( PopupLabel( width=wid-2*side_pad, height=hei*0.15, text = authorship, is_first = False
                                           ) )
        left_box.add_widget( PopupLabel( width=wid-2*side_pad, height=hei*0.15, text = origin,     is_first = False
                                           ) )
        left_box.add_widget( PopupLabel( width=wid-2*side_pad, height=hei*0.15, text = target,     is_first = False
                                           ) )

        right_box = BoxLayout(orientation="vertical", size_hint=(None, 1), width = 50, spacing=12, padding=[3,0,0,1] )
        
        right_box.add_widget( PopupButton(source = 'img/copy.png'    ) )
        right_box.add_widget( PopupButton(source = 'img/cite.png'    ) )
        right_box.add_widget( PopupButton(source = 'img/external.png') )

        box_layout.add_widget( left_box  )
        box_layout.add_widget( right_box )

        self.add_widget(box_layout)


class MySearchBar(BoxLayout):
    def __init__(self, size_hint=(None,None), size=[100,50], **kwargs ):
        super(MySearchBar, self).__init__(**kwargs)
        #
        self.size_hint = size_hint
        self.size      = (size[0], Window.width - 150)
        #
        self.orientation = 'horizontal'
        self.padding     = 0
        self.spacing     = 0
        #
        ti = TextInput(text="Search...", 
                        focus     = True, 
                        multiline = False, 
                        halign    = 'left')
        self.add_widget( ti )



class MediaTypes(FloatLayout):
    def __init__(self, size_hint=(None,None), width=100, height=20, bound_button=None, **kwargs ):
        super(MediaTypes, self).__init__(**kwargs)
        #
        self.box     = BoxLayout(orientation = 'vertical', 
                            pos_hint    = {'x':0.5},
                            size_hint_x = 0.5,
                            y = 50
                            )
        self.options = ['Article', 'Book', 'Thesis', 'Policy', 'Documentary', 'All Media']
        #
        for option in self.options:
            btn = Button(
                text             = option,
                size_hint        = (None, None),
                height           = 20,
                width            = 200,
                background_color = (0.5, 0.5, 0.8, 1),
                halign           = 'left',
                color            = (1, 1, 1, 1)
            )
            self.box.add_widget( btn )
            btn.bind( on_release = lambda btn: on['app']().dismiss_media_button(btn_txt=btn.text, to_be_removed=self ) )
        #
        self.add_widget( self.box )


class SDGTypes(FloatLayout):
    def __init__(self, size_hint=(None,None), width=100, height=20, bound_button=None, **kwargs ):
        super(SDGTypes, self).__init__(**kwargs)
        #
        self.box     = BoxLayout(orientation = 'vertical', 
                            pos_hint    = {'x':0.5},
                            size_hint_x = 0.5,
                            y = 50
                            )
        self.options     = ['1 - No Poverty',
                       '2 - Zero Hunger', 
                       '3 - Good Health...', 
                       '4 - Quality Education', 
                       '5 - Gender Equality',
                       '6 - Clean Water...',
                       '7 - Clean Energy...',
                       '8a - Decent Work',
                       '8b - Economic Growth',
                       '9 - Industry...',
                       '10 - Reduced Inequalities',
                       '11 - Sustainable Cities...',
                       '12a - Responsible Consumption',
                       '12b - Responsible Production',
                       '13 - Climate Action',
                       '14 - Life below Water',
                       '15 - Life on Land',
                       '16 - Peace, Justice...',
                       '17 - Partnerships...',
                       'All']
        #
        for option in self.options:
            btn = Button(
                text             = option,
                size_hint        = (None,None),
                width            = 200,
                height           = 20,
                background_color = (0.5, 0.5, 0.8, 1),
                color            = (1, 1, 1, 1),
            )
            self.box.add_widget( btn )
            btn.bind( on_release = lambda btn: on['app']().dismiss_sdg_button(btn_txt=btn.text, to_be_removed=self ) )
        #
        self.add_widget( self.box )


class ScienceTypes(FloatLayout):
    def __init__(self, size_hint=(None,None), width=100, height=20, bound_button=None, **kwargs ):
        super(ScienceTypes, self).__init__(**kwargs)
        #
        self.box     = BoxLayout(orientation = 'vertical', 
                            pos_hint    = {'x':0.5},
                            size_hint_x = 0.5,
                            y = 50
                            )
        #
        fields      = 'Trending,Miscellaneous,Natural Sciences,Engineering,Life Sciences,Social Sciences,Arts & Humanities'.split(',')
        field_trend = 'Alt Protein,Alt Leather,Bioremediation,Organ-on-a-chip,Precision Fermentation'
        field_nat   = 'Polymers and Plastics,Polymers - Leather,Polymers - Silk'.split(',')
        field_eng   = 'Energy,Environmental Sciences,Sustainability'.split(',')
        field_life  = 'Food Science,Food Science - Protein,Nutrition'.split(',')
        field_sochum = 'Demography,Law,Religious Studies'.split(',')
        field_other  = ['All']
        # ----------------------------
        for field, options in zip(fields, (field_other, field_nat, field_eng, field_life, field_sochum)):
            #
            self.box.add_widget(Button(text=field, 
                                       size_hint        = (None,None),
                                        width            = 200,
                                        height           = 20,
                                        background_color = (0.8, 0.8, 0.8, 1),
                                        color            = (1, 1, 1, 1),
                                        halign           = 'left'
                                       )
                                )
            for option in options:
                btn = Button(
                    text             = option,
                    size_hint        = (None,None),
                    width            = 200,
                    height           = 20,
                    background_color = (0.95, 0.95, 0.95, 1),
                    color            = (1, 1, 1, 1),
                    halign           = 'left'
                )
                btn.bind( on_release = lambda btn: on['app']().dismiss_science_button(btn_txt=btn.text, to_be_removed=self ) )
                self.box.add_widget(btn)
        #---------------------------
        self.add_widget( self.box )


# class ScienceTypes(BoxLayout):
#     def __init__(self, size_hint=(None,None), size=[1,1], **kwargs ):
#         super(ScienceTypes, self).__init__(**kwargs)
#         #
#         self.size_hint = size_hint
#         self.size      = size
#         #
#         self.orientation = 'vertical'
#         self.padding     = 0
#         self.spacing     = 0
#         #
#         main_button = Button(text='Science', size_hint=(1, None), height=40)
#         #
#         self.dropdown    = DropDown()
#         fields      = 'Trending,Miscellaneous,Natural Sciences,Engineering,Life Sciences,Social Sciences,Arts & Humanities'.split(',')
#         field_trend = 'Alt Protein,Alt Leather,Bioremediation,Organ-on-a-chip,Precision Fermentation'
#         field_nat   = 'Polymers and Plastics,Polymers - Leather,Polymers - Silk'.split(',')
#         field_eng   = 'Energy,Environmental Sciences,Sustainability'.split(',')
#         field_life  = 'Food Science,Food Science - Protein,Nutrition'.split(',')
#         field_sochum = 'Demography,Law,Religious Studies'.split(',')
#         field_other  = ['All']
#         #
#         for field, options in zip(fields, (field_other, field_nat, field_eng, field_life, field_sochum)):
#             #
#             self.dropdown.add_widget(Button(text=field, halign='left'))
#             for option in options:
#                 btn = Button(
#                     text             = option,
#                     size_hint        = (None,None),
#                     width            = 200,
#                     height           = 20,
#                     background_color = (0.95, 0.95, 0.95, 1),
#                     color            = (1, 1, 1, 1),
#                     halign           = 'left'
#                 )
#                 btn.bind( on_release = lambda btn: self.dropdown.select(btn.text))
#                 self.dropdown.add_widget(btn)
#         #
#         main_button.bind(on_release=self.dropdown.open)
#         self.dropdown.bind(on_select=lambda instance, value: setattr(main_button, 'text', value))
#         #
#         self.add_widget(main_button)




class MapApp(App):
    def build(self):
        global on
        on = dict()
        #
        root    = FloatLayout(size_hint=(1, 1))
        #
        #
        box_bed = BoxLayout(orientation="vertical", size_hint=(1, 1))
        top_box = BoxLayout(size_hint=(1, None), height=50, orientation="horizontal")

        img_box = BoxLayout( size_hint= (None, None), size = (50,50) )
        img_box.add_widget(Image(source    = 'img/logo.jpg', 
                                 size_hint = (1,1) ), 
                                ) 
        top_box.add_widget( img_box )
        top_box.add_widget( MySearchBar(size=(200,50), size_hint=(None,None)) )
        top_box.add_widget( ToolButton(source='img/view.png') )
        top_box.add_widget( ToolButton(source='img/refresh.png') )
        #
        box_bed.add_widget( top_box ) #----------------------------

        map_view = MapView(
            lat        = 50.6394,
            lon        = 3.057,
            zoom       = 10,
            map_source = MapSource(sys.argv[1], attribution="") if len(sys.argv) > 1 else "osm"
        )

        marker = MapMarkerPopup(lat=50.6394, lon=3.057, popup_size=("400dp", "100dp"))
        marker.add_widget(CustomBubble(main_text='This is a text'))
        map_view.add_marker(marker)

        box_bed.add_widget(map_view) #----------------------------

        on['bottom_box'] = BoxLayout(size_hint=(1, None), height=50, orientation="horizontal")

        with on['bottom_box'].canvas.before:
            Color(rgba = (0.95, 0.95, 0.95, 1)) # White-ish
            RoundedRectangle(pos   = [on['bottom_box'].pos[0],  on['bottom_box'].pos[1] ], 
                            size   = [ Window.width, on['bottom_box'].size[1]+5]   , 
                            radius = [10, 10, 0, 0]
                            )
        #
        on['bottom_box'].add_widget( ToolButton( source='img/target.png') )
        on['bottom_box'].add_widget( ToolButton( source='img/green.png') )
        on['bottom_box'].add_widget( ToolButton( source='img/procrueltyfree.png') )
        on['bottom_box'].add_widget( ToolButton( source='img/crueltyfree.png') )
        #
        on['media_button'] = Button(text='Media', size_hint=(None, None), width=40, height=40)
        on['media_button'].bind( on_release = self.show_media_popup )
        #
        on['sdg_button'] = Button(text='SDG', size_hint=(None, None), width=40, height=40)
        on['sdg_button'].bind( on_release = self.show_sdg_popup )
        #
        on['science_button'] = Button(text='Sci', size_hint=(None, None), width=40, height=40)
        on['science_button'].bind( on_release = self.show_science_popup )
        #
        on['bottom_box'].add_widget( on['media_button'] )
        on['bottom_box'].add_widget( on['sdg_button'] )
        on['bottom_box'].add_widget( on['science_button'] )
        #
        box_bed.add_widget( on['bottom_box'] ) #----------------------------
        root.add_widget( box_bed )

        on['app'] = App.get_running_app
        return root
    
    def show_media_popup(self, instance):
        # Create and add the popup
        media_dropdown = MediaTypes( size_hint = (None, None), 
                                         width = 200, 
                                         height= 600, 
                                         bound_button = on['media_button']  )
        self.root.add_widget(media_dropdown)

    def dismiss_media_button(self, btn_txt, to_be_removed, *args, **kwargs):
        on['media_button'].text = btn_txt
        to_be_removed.parent.remove_widget( to_be_removed )

    def show_sdg_popup(self, instance):
        # Create and add the popup
        sdg_dropdown = SDGTypes( size_hint = (None, None), 
                                         width = 200, 
                                         height= 600, 
                                         bound_button = on['sdg_button']  )
        self.root.add_widget(sdg_dropdown)

    def dismiss_sdg_button(self, btn_txt, to_be_removed, *args, **kwargs):
        on['sdg_button'].text = btn_txt
        to_be_removed.parent.remove_widget( to_be_removed )



    def show_science_popup(self, instance):
        # Create and add the popup
        sdg_dropdown = ScienceTypes( size_hint = (None, None), 
                                         width = 200, 
                                         height= 600, 
                                         bound_button = on['science_button']  )
        self.root.add_widget(sdg_dropdown)

    def dismiss_science_button(self, btn_txt, to_be_removed, *args, **kwargs):
        on['science_button'].text = btn_txt
        to_be_removed.parent.remove_widget( to_be_removed )



if __name__ == '__main__':
    MapApp().run()
