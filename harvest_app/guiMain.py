import tkinter as tk

from harvest_app.pages import guiDataLC, guiDataManip, guiMerging, guiCluster, guiAdwords

"""
Run the GUI using 'f5' to be sure that everything works.
"""

class PropApp(tk.Tk):
    padx=5
    pady=5

    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.grid()
        self.frames = {}
        for F in (
                guiDataLC.DataLCPage,
                guiDataManip.DataManipPage,
                guiMerging.MergePage,
                guiCluster.ClusteringPage,
                guiAdwords.AdwordsPage
                ):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(column=0, row=0, columnspan=2, sticky='nswe')
        self.show_frame("AdwordsPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

app = PropApp()
app.title("Targeting Model")
app.mainloop()
