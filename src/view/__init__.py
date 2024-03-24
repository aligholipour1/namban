from gi.repository import Gdk, Gtk
import settings
import domain
from pathlib import Path

class trashIcon(Gtk.Image):
    def __init__(self):
        super().__init__()
        self.set_from_icon_name("trash-empty")
        # self.set_size_request(15,15)

class pencilIcon(Gtk.Image):
    def __init__(self):
        super().__init__()
        self.set_from_icon_name("draw-freehand")

class profileConnectButton(Gtk.Switch):
    def __init__(self, app:domain.app, profile:domain.profile):
        super().__init__()
        self.add_css_class('server-button')

class Label(Gtk.Label):
    def __init__(self,label,classes=[],**more):
        super().__init__(label=label,**more)
        self.set_css_classes(classes+['label'])

class LeftFloat(Gtk.AspectFrame):
    def __init__(self,widget):
        super().__init__(
            halign=Gtk.Align.START,
            obey_child=True
        )
        self.set_child(widget)

class profileInformation(Gtk.Fixed):
    def __init__(self,profile:domain.profile):
        super().__init__()
        self.prof = profile
        self.update()
        self.add_css_class('server-information')
    def update(self):
        try:
            self.remove(self.title)
            self.title = None
            self.remove(self.inform)
            self.inform = None
        except:...

        self.title = Label(
            self.prof.name,
            classes=[
                'color-high',
                'font-l'
                ]
            )
        serversAspectFrame = Gtk.AspectFrame()
        serversAspectFrame.add_css_class('server-aspect-frame')
        self.servers = Gtk.Grid()
        serversAspectFrame.set_child(
            self.servers
        )
        for i, serv in enumerate([self.prof.server1,self.prof.server2]):
            self.servers.attach(
                LeftFloat(
                    Label(
                        f'{i+1}: {str(serv)}',
                        classes=['font-s','color-low']
                    )
                ),0,i,1,1
            )
        self.put(
            self.title,
            0,5
        )
        self.put(
            serversAspectFrame,
            60,0
        )

class Button(Gtk.Button):
    def __init__(self, child, onClick, classes=[],size=None):
        super().__init__()
        self.set_child(child)
        self.set_css_classes(classes+['button'])
        # self.set_relief(Gtk.ReliefStyle.NONE)
        if size:
            self.set_size_request(*size)
            self.set_hexpand(False)
            self.set_vexpand(False)

class profile(Gtk.Box):
    def __init__(self,app:domain.app,profile:domain.profile):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.add_css_class('server')
        self.fixed = Gtk.Fixed()
        self.append(
            self.fixed
        )
        self.fixed.put(
            profileConnectButton(app,profile),
            235,4
        )
        self.fixed.put(
            Button(
                trashIcon(),None,[]
            )
            ,
            190,0
        )
        self.fixed.put(
            Button(
                pencilIcon(),None,[]
            )
            ,
            150,0
        )
        self.fixed.put(
            profileInformation(profile),
            10,0
        )

class profileList(Gtk.Grid):
    def __init__(self, app:domain.app):
        super().__init__()
        self.add_css_class('server-list')
        for i, p in enumerate(app.data.profiles):
            self.attach(
                profile(app,p),
                0,i,1,1
            )

class addButton(Gtk.Overlay):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.button = Gtk.Button()
        self.button.set_child(
            Label('+')
        )
        self.button.add_css_class('add-btn')
        self.set_child(self.button)

class wondowContainer(Gtk.Fixed):
    def __init__(self, app):
        super().__init__()
        self.put(
            profileList(app),0,0
        )
        self.put(
            addButton(app),10,350
        )
        


class window(Gtk.ApplicationWindow):
    def __init__(self, app=None):
        super().__init__(application=app,title=settings.WINDOW_TITLE)
        self.set_default_size(300,400)
        self.set_child(
            wondowContainer(app)
        )
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path(
            str(Path(
                __file__
            ).parent / "style.css"
            )
        )
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            cssProvider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

__all__ = [
    window
]