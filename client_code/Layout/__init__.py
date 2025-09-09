from ._anvil_designer import LayoutTemplate
from anvil import *
import anvil.server

class Layout(LayoutTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Home')

  def button_news_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('News')

  def button_events_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Events')

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Technicals')
