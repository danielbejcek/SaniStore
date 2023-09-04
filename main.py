
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.event import EventDispatcher
from HoverButton import HoverBehavior
from kivy.uix.textinput import TextInput
from DataFrame import *
import pandas as pd

# Class that allows transitions between screens.
# Using this we are preventing creating redundant switch screen methods within each class.
class Transition:
    def transition(self, screen_name):
        self.manager.transition = WipeTransition()
        self.manager.transition.duration = 1
        self.manager.current = screen_name

    def home_page(self, instance):
        self.manager.transition.duration = 1
        self.manager.current = "Second"
        self.manager.transition = WipeTransition()


# Custom class HoverButton(original creator: 'Olivier POYEN') fills the role as a highlighter of a button.
# Once mouse is hovering over a specified widget, its custom events (on_enter,on_leave) are fired,
# allowing us to modify the properties of the widget.
class HoverButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)

        # Empty dictionary which consists of keys and values. Each key is a image before being selected with a mouse hover.
        # each value of a key is a image which is highlighted after it has been selected with a mouse hover.
        # Whenever we want to add additional button, that includes a highlight function, we just need to update the path within this dictionary.
        self.images_path = {"Images/inventory_text.png": "Images/inventory_text_selected.png",
                            "Images/import_text.png": "Images/import_text_selected.png",
                            "Images/home_text.png": "Images/home_text_selected.png",
                            "Images/home_button_icon.png":"Images/home_button_icon_selected.png",
                            "Images/notebook_closed.png":"Images/notebook_closed_selected.png",
                            "Images/notebook_opened.png":"Images/notebook_opened_selected.png"}

    # "on_button_hover" method loops trough the 'images_path' dictionary and looks for a element that is equal to a instance atribute.
    # In this case it's looking for a background_normal within the "inventory_button" widget. Once it finds a equal string,
    # it changes the source image for a highlighted one.
    def on_button_hover(self, instance):
        for key in self.images_path:
            if instance.background_normal in key:
                instance.background_normal = self.images_path[key]


    # Similar method to the previous one. Once the mouse hover leaves the designated area of a button.
    # It loops trough the dictionary and after it finds a corresponding string, it changes it back to the non-highlighted image.
    def on_button_hover_exit(self, instance):
        for key, value in self.images_path.items():
            if instance.background_normal in value:
                instance.background_normal = key

class WelcomeScreen(Screen, Transition):
    def __init__(self,  **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)

        self.logo_image = Image(
            source="Images/Logo.png",
            size_hint=(1.5,1.5),
            opacity=0,
            pos_hint={"center_x": .5, "center_y": 1})
        self.ids.LY1.add_widget(self.logo_image)
        fade_in_image = Animation(opacity=1, duration=1)
        fade_in_image.start(self.logo_image)
        # In order for this function to perform as inteded, lambda needs to be used here.
        Clock.schedule_once(lambda dt: self.transition("Second"), 2)



class MainScreen(Screen, Transition):
    def __init__(self, **kwargs):
        super(MainScreen,self).__init__(**kwargs)
        self.inventory_button = HoverButton(
            background_normal="Images/inventory_text.png",
            background_down="Images/inventory_text.png",
            font_size=15,
            size_hint=(.8, 1))

        self.ids.LY2.add_widget(self.inventory_button)
        self.inventory_button.bind(on_enter=self.inventory_button.on_button_hover, on_leave=self.inventory_button.on_button_hover_exit)
        # In order for a transition to work, we need to combine this on_release event with lambda.
        self.inventory_button.bind(on_release=lambda x: self.transition("Third"))



        self.import_button = HoverButton(
            background_normal="Images/import_text.png",
            background_down="Images/import_text.png",
            font_size=15,
            size_hint=(.8, 1))
        self.ids.LY2.add_widget(self.import_button)
        self.import_button.bind(on_enter=self.import_button.on_button_hover, on_leave=self.import_button.on_button_hover_exit)



    def on_leave(self, *args):
        pass




class InventoryScreen(Screen, Transition):
    def __init__(self, **kwargs):
        super(InventoryScreen, self).__init__(**kwargs)

        self.home_button = HoverButton(
            background_normal="Images/home_button_icon.png",
            background_down="Images/home_button_icon.png",
            size_hint=(.065,.1),
            pos_hint={"center_x": .93,"top_y": .95})
        self.home_button.bind(on_enter=self.home_button.on_button_hover, on_leave=self.home_button.on_button_hover_exit)
        self.home_button.bind(on_release=self.home_page)
        self.ids.LY3.add_widget(self.home_button)

        self.current_state_image = Image(
            source="Images/current_state.png",
            size_hint=(.5, .5),
            pos_hint={"center_x": .16, "center_y": .9})
        self.ids.LY3.add_widget(self.current_state_image)

        self.notebook_button = HoverButton(
            background_normal="Images/notebook_closed.png",
            background_down="Images/notebook_closed.png",
            size_hint=(.04, .1),
            pos_hint={"center_x": .38, "center_y": .91})
        self.notebook_button.bind(on_enter=self.notebook_button.on_button_hover)
        self.notebook_button.bind(on_leave=self.notebook_button.on_button_hover_exit)
        self.notebook_button.bind(on_release=self.background_change)
        self.ids.LY3.add_widget(self.notebook_button)

    def on_pre_enter(self, *args):
            self.add_widgets(self.ids.LY4)
            self.ids.LY4.bind(minimum_height=self.ids.LY4.setter('height'))

    def background_change(self, instance):
        if instance.background_normal and instance.background_down == "Images/notebook_closed.png":
            instance.size_hint=(.08,.1)
            instance.background_normal = "Images/notebook_opened.png"
            instance.background_down = "Images/notebook_opened.png"

            self.ids.LY4.clear_widgets()
            self.add_widgets(self.ids.LY5)


        elif instance.background_normal and instance.background_down == "Images/notebook_opened.png":
            instance.size_hint=(.04,.1)
            instance.background_normal="Images/notebook_closed.png"
            instance.background_down="Images/notebook_closed.png"

            self.ids.LY5.clear_widgets()
            self.on_pre_enter()




    def add_widgets(self, layer):
        if self.notebook_button.background_normal and self.notebook_button.background_down == "Images/notebook_closed.png":

            for component, amount in zip(components["Komponent"], components["Množství"]):
                self.component_label= Label(
                    text=component,
                    size_hint=(1,None),
                    font_size=30,
                    bold=True)

                self.amount_input = Label(
                    text=str(amount),
                    size_hint=(1,None),
                    font_size=45,
                    bold=True)
                layer.add_widget(self.component_label)
                layer.add_widget(self.amount_input)
                for divider in range(2):
                    self.divider_line = Image(
                        source="Images/divider.png",
                        size_hint_y=None,
                        height=10)
                    layer.add_widget(self.divider_line)


        elif self.notebook_button.background_normal and self.notebook_button.background_down == "Images/notebook_opened.png":

            for component, amount in zip(components["Komponent"], components["Množství"]):
                self.component_label= Label(
                    text=component,
                    size_hint=(.8,1),
                    font_size=15)

                self.amount_input = Label(
                    text=str(amount),
                    size_hint=(.8,1),
                    font_size=20)
                layer.add_widget(self.component_label)
                layer.add_widget(self.amount_input)
                for divider in range(2):
                    self.divider_line = Image(
                        source="Images/divider.png",
                        size_hint_y=None,
                        height=7,
                        width=1,
                        allow_stretch=True)
                    layer.add_widget(self.divider_line)


    def on_leave(self, *args):
        self.ids.LY5.clear_widgets()
        self.ids.LY4.clear_widgets()
class ImportScreen(Screen, Transition):
    def __init__(self,**kwargs):
        super(ImportScreen, self).__init__(**kwargs)
        pass




class WindowManager(ScreenManager):
    pass

class SaniStore(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="First"))
        sm.add_widget(MainScreen(name="Second"))
        sm.add_widget(InventoryScreen(name="Third"))
        sm.add_widget(ImportScreen(name="Fourth"))
        return sm


if __name__ == "__main__":
    SaniStore().run()
