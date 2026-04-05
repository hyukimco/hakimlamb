import sys
import requests # Used to fetch data online

from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.bubble import Bubble
from kivy.uix.image import AsyncImage
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
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

        txt = """yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes yes
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
        
        right_box.add_widget( PopupButton(source = 'icons/copy.png'    ) )
        right_box.add_widget( PopupButton(source = 'icons/cite.png'    ) )
        right_box.add_widget( PopupButton(source = 'icons/external.png') )

        box_layout.add_widget( left_box  )
        box_layout.add_widget( right_box )

        self.add_widget(box_layout)

class MediaTypes(BoxLayout):
    def __init__(self, size_hint=(None,None), size=[1,1], **kwargs ):
        super(MediaTypes, self).__init__(**kwargs)
        #
        self.size_hint = size_hint
        self.size      = size
        #
        self.orientation = 'vertical'
        self.padding     = 0
        self.spacing     = 0
        #
        main_button = Button(text='Media', size_hint=(1, None), height=40)
        #
        dropdown    = DropDown()
        options     = ['All','Articles', 'Books', 'Theses', 'Policies']
        #
        for option in options:
            btn = Button(
                text             = option,
                size_hint_y      = None,
                height           = 20,
                background_color = (0.5, 0.5, 0.8, 1),
                color            = (1, 1, 1, 1)
            )
            btn.bind( on_release = lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        #
        main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, value: setattr(main_button, 'text', value))
        #
        self.add_widget(main_button)



class ScienceTypes(BoxLayout):
    def __init__(self, size_hint=(None,None), size=[1,1], **kwargs ):
        super(ScienceTypes, self).__init__(**kwargs)
        #
        self.size_hint = size_hint
        self.size      = size
        #
        self.orientation = 'vertical'
        self.padding     = 0
        self.spacing     = 0
        #
        main_button = Button(text='All Sciences', size_hint=(1, None), height=40)
        #
        dropdown    = DropDown()
        fields      = 'Trending,Miscellaneous,Natural Sciences,Engineering,Life Sciences,Social Sciences,Arts & Humanities'.split(',')
        field_trend = 'Alt Protein,Alt Leather,Bioremediation,Organ-on-a-chip,Precision Fermentation'
        field_nat   = 'Polymers and Plastics,Polymers - Leather,Polymers - Silk'.split(',')
        field_eng   = 'Energy,Environmental Sciences,Sustainability'.split(',')
        field_life  = 'Food Science,Food Science - Protein,Nutrition'.split(',')
        field_sochum = 'Demography,Law,Religious Studies'.split(',')
        field_other  = ['All']
        #
        for field, options in zip(fields, (field_other, field_nat, field_eng, field_life, field_sochum)):
            #
            dropdown.add_widget(Button(text=field, halign='left'))
            for option in options:
                btn = Button(
                    text             = option,
                    size_hint_y      = None,
                    height           = 20,
                    background_color = (0.95, 0.95, 0.95, 1),
                    color            = (1, 1, 1, 1),
                    halign           = 'left'
                )
                btn.bind( on_release = lambda btn: dropdown.select(btn.text))
                dropdown.add_widget(btn)
        #
        main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, value: setattr(main_button, 'text', value))
        #
        self.add_widget(main_button)


class MapApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", size_hint=(1, 1))

        map_view = MapView(
            lat        = 50.6394,
            lon        = 3.057,
            zoom       = 10,
            map_source = MapSource(sys.argv[1], attribution="") if len(sys.argv) > 1 else "osm"
        )

        marker = MapMarkerPopup(lat=50.6394, lon=3.057, popup_size=("400dp", "100dp"))
        marker.add_widget(CustomBubble(main_text='This is a text'))
        map_view.add_marker(marker)

        root.add_widget(map_view)

        bottom_box = BoxLayout(size_hint=(None, None), height=50, orientation="horizontal")
        with bottom_box.canvas.before:
            Color(rgba = (0.95, 0.95, 0.95, 1)) # White-ish
            RoundedRectangle(pos   = [bottom_box.pos[0],  bottom_box.pos[1]  ], 
                            size   = [ Window.width, bottom_box.size[1]+5], 
                            radius = [10, 10, 0, 0]
                            )
        #
        bottom_box.add_widget(ToolButton(source='icons/target.png') )
        bottom_box.add_widget(ToolButton(source='icons/green.png') )
        bottom_box.add_widget(ToolButton(source='icons/procrueltyfree.png') )
        bottom_box.add_widget(ToolButton(source='icons/crueltyfree.png') )
        bottom_box.add_widget( MediaTypes(   size_hint=(None, None), size=(100, 40) ) )
        bottom_box.add_widget( ScienceTypes( size_hint=(None, None), size=(200, 40) ) )
        bottom_box.add_widget(ToolButton(source='icons/view.png') )
        bottom_box.add_widget(ToolButton(source='icons/refresh.png') )
        root.add_widget(bottom_box)

        return root

if __name__ == '__main__':
    MapApp().run()
