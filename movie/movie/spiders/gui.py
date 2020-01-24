import tkinter as tk
import tkinter.ttk as ttk
import movie_module as mm
import sql_module as sm

movie_reel_path = r'./images/movie_reel.png'
bg_color = '#577399'#'#242038'
text_color = '#F7F7FF'


class Application(tk.Frame):
    # will store all text that is retrieved from the entry box
    entry_text = ''

    def __init__(self, master=None):
        super().__init__(master)
        # all root modifications done here
        self.master = master
        self.master.title('Movie-Finder')
        self.master.geometry('800x600') # sets the size of the gui
        self.master.config(bg=bg_color) # sets the background color
        # self.pack()
        self.create_widgets()

    def create_widgets(self):
        ''' Title and Description '''
        # create the main title label #
        self.movie_reel_image = tk.PhotoImage(file=movie_reel_path) # creates the movie label icon
        self.movie_reel_image = self.movie_reel_image.subsample(15,15)
        # the actual label
        self.title_label = tk.Label(self.master, text='Movie Finder!', image=self.movie_reel_image, compound=tk.RIGHT, bg=bg_color, fg=text_color)
        self.title_label.config(font=('Varela Round',44))
        self.title_label.pack(side='top')

        self.info_label = tk.Label(self.master, text='Ever wanted to look up a movie and get all the information you wanted in one place?\nWell now you can! Simply type in the movie you are interested in and press the button!', bg=bg_color, fg=text_color)

        self.info_label.config(font=('Varela Round',14))
        self.info_label.pack()
        ''' End Title and Description '''

        ''' Main content '''
        # now we need a new frame for the entry box and button
        self.content = tk.Frame(self.master, bg=bg_color, bd=0, width=50, height=50, relief=tk.FLAT) 
        self.entry_box = tk.Entry(self.content)
        self.entry_box.focus_set() # focuses on the entry box when the app starts
        self.entry_box.grid(column=0, row=0)
        
        self.submit_button = tk.Button(self.content, text='Get Info!', highlightbackground='#495867', fg='black', command=lambda:self.get_movie_information(self.entry_box.get())) 
        self.submit_button.config(font=('Varela Round',15))
        self.submit_button.grid(column=1, row=0, padx=(20,0))
        # need to move frame up a tiny bit...
        self.content.pack(expand=True) # here
        ''' End Main Content '''

        ''' Footer '''
        self.footer = tk.Frame(self.master, bg=bg_color, bd=0, height=30, relief=tk.FLAT)
        # create button to quit and button to view watch-list
        self.quit_button = tk.Button(self.footer, text='Quit', highlightbackground='#495867', fg='black', command=self.master.destroy)
        self.quit_button.config(font=('Varela Round',15))
        self.quit_button.pack(side='left')
        
        self.watch_list_button = tk.Button(self.footer, text='Open Watch List', highlightbackground='#495867', fg='black' ,command=lambda:self.display_watch_list())
        self.watch_list_button.config(font=('Varela Round',15))
        self.watch_list_button.pack(side='right')
        self.footer.pack(fill='both', side='bottom')
        ''' End Footer '''


    ''' Uses the movie_module.py file to scrape the rotten tomato page for the movie information.
        Right now, it will only scrape the page and print to console. '''
    def get_movie_information(self, text):
        try:
            # remove any leading or trailing whitespace
            text = text.strip()
            # check that text is non-empty
            if len(text) == 0:
                print('No movie specified.')
                return

            table = mm.handle(text)
            # print(table)
            # add table into database
            sm.handle_query(table)

            self.entry_box.delete(0,tk.END) # clears the entry box
        except Exception as e:
            print(e)

    # TODO
    ''' Opens the watch_list database '''
    def display_watch_list(self):
        sm.show_movie_table()

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
