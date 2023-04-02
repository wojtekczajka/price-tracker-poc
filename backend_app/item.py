class Item:
    def __init__(self, name=""):
        self.name = name

    def get_name(self):
        return self.name

    def get_plot_path(self):
        plot_path = 'plots/' + self.get_name() + '.html'
        return plot_path
