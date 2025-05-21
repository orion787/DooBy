from tkinter import Tk
from dooby.core import init_db
from dooby.gui.main_page import DooByApp
from models import Partner

engine = init_db("partners.db")

root = Tk()
app = DooByApp(root, Partner, title="Учет партнёров", logo_path="resources//logo.png")
root.mainloop()
