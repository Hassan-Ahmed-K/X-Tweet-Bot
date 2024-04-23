import tkinter as tk
from tkinter import ttk, messagebox
import tweepy
import os
from dotenv import load_dotenv
# import PIL
from PIL import Image, ImageTk  
import time
# from PyInstaller.utils.hooks import collect_all

# datas, binaries, hiddenimports = collect_all('PIL')

# Define colors and fonts
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4CAF50"
BUTTON_TEXT_COLOR = "white"
ERROR_COLOR = "red"
SUCCESS_COLOR = "green"
FONT = ("Arial", 12)  # Change the font to AX_icon.svgrial

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
api_key = os.getenv("api_key")
api_secret_key = os.getenv("api_secret_key")
bearer_token = os.getenv("bearer_token")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")

def post_tweet():
    if tweet_radio_var.get() == 1: 
        tweet_text = tweet_entry.get()
        if len(tweet_text) > 0:
            try:
                client = tweepy.Client(bearer_token, api_key, api_secret_key, access_token, access_token_secret)
                api_auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
                api = tweepy.API(api_auth)
                client.create_tweet(text=tweet_text)
                messagebox.showinfo("Success", "Tweet posted successfully!")
                tweet_entry.delete(0, tk.END) 
            except Exception as e:
                messagebox.showerror("Error", f"Error posting tweet: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter some text to tweet.")
    else:
        file_path = tweet_entry.get()
        if os.path.exists(file_path):
            try:
                client = tweepy.Client(bearer_token, api_key, api_secret_key, access_token, access_token_secret)
                api_auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
                api = tweepy.API(api_auth)
                interval = int(interval_entry.get())
                with open(file_path, 'r') as file:
                    tweets = file.read().split("\n")
                    print(tweets)
                for tweet in tweets:
                    tweet = tweet.strip()
                    client.create_tweet(text=tweet)
                    time.sleep(interval*60)
                    
                messagebox.showinfo("Success", "Tweets posted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error posting tweets: {e}")
        else:
            messagebox.showwarning("Warning", "File not found.")

def save_keys():
    client_id_val = client_id_entry.get()
    client_secret_val = client_secret_entry.get()
    api_key_val = api_key_entry.get()
    api_secret_key_val = api_secret_key_entry.get()
    bearer_token_val = bearer_token_entry.get()
    access_token_val = access_token_entry.get()
    access_token_secret_val = access_token_secret_entry.get()
    
    # Clear the entry fields
    client_id_entry.delete(0, tk.END)
    client_secret_entry.delete(0, tk.END)
    api_key_entry.delete(0, tk.END)
    api_secret_key_entry.delete(0, tk.END)
    bearer_token_entry.delete(0, tk.END)
    access_token_entry.delete(0, tk.END)
    access_token_secret_entry.delete(0, tk.END)
    
    # Write the API keys to the .env file
    with open(".env", "w") as f:
        f.write(f"client_id={client_id_val}\n") 
        f.write(f"client_secret={client_secret_val}\n")
        f.write(f"api_key={api_key_val}\n")
        f.write(f"api_secret_key={api_secret_key_val}\n")
        f.write(f"bearer_token={bearer_token_val}\n")
        f.write(f"access_token={access_token_val}\n")
        f.write(f"access_token_secret={access_token_secret_val}\n")
        
    messagebox.showinfo("Success", "API keys saved successfully!")

# Create the main window
root = tk.Tk()
root.title("X Bot")
# root.geometry("500x400+100+50")
root.configure(bg=BG_COLOR)


# Hide notebook bar style
style = ttk.Style()
style.configure('TNotebook',background=BG_COLOR,borderwidth=0, height=0, width=0)  # 'nw' positions tabs at the top

# Create the notebook (tabs)
notebook = ttk.Notebook(root, style='TNotebook')

# Create the header bar with Twitter icon
header_bar = tk.Frame(root,bg=BG_COLOR)
header_bar.pack(fill="x")

# Load the Twitter icon image
twitter_icon_image = Image.open("Twitter X Icon PNG.jpeg")
twitter_icon_image = twitter_icon_image.resize((50, 40))  # Resize the image if needed
twitter_icon = ImageTk.PhotoImage(twitter_icon_image)
twitter_icon_label = tk.Label(header_bar, image=twitter_icon, bg=BG_COLOR)
twitter_icon_label.pack(side="left")


# Create a button for the Tweet tab
tweet_button = tk.Button(header_bar, text="Tweet Tab", command=lambda: notebook.select(tweet_tab), font=("Arial", 10))
tweet_button.pack(side="right", padx=5)

# Create a button for the API Keys tab
api_keys_button = tk.Button(header_bar, text="API Keys Tab", command=lambda: notebook.select(keys_tab),  font=("Arial", 10))
api_keys_button.pack(side="right", padx=5)

# Create the tweet tab
tweet_tab = tk.Frame(notebook, bg=BG_COLOR, padx=20, pady=20)
notebook.add(tweet_tab)

tweet_radio_var = tk.IntVar(value=1)
tweet_radio_entry_text = tk.Radiobutton(tweet_tab, text="Tweet Text", variable=tweet_radio_var, value=1, bg=BG_COLOR, font=FONT)
tweet_radio_entry_text.grid(row=0, column=0, sticky='w')

space= tk.Label(tweet_tab, text=" ", bg=BG_COLOR, font=FONT)
space.grid(row=0, column=2, sticky="w")


tweet_radio_entry_file = tk.Radiobutton(tweet_tab, text="Tweet from File", variable=tweet_radio_var, value=2, bg=BG_COLOR, font=FONT)
tweet_radio_entry_file.grid(row=0, column=1, sticky='w')

tweet_label = tk.Label(tweet_tab, text="Enter Tweet OR File Path (.txt):", bg=BG_COLOR, font=FONT)
tweet_label.grid(row=2, column=0, sticky="w")

tweet_entry = tk.Entry(tweet_tab,width=50, font=FONT)
tweet_entry.grid(row=3, column=0, padx=10,columnspan=3, pady=5, sticky="w")

interval_label = tk.Label(tweet_tab, text="Interval (minutes):", bg=BG_COLOR, font=FONT)
interval_label.grid(row=4, column=0, sticky="w")

interval_entry = tk.Entry(tweet_tab, font=FONT)
interval_entry.insert(0, "1") 
interval_entry.grid(row=5, column=0, padx=10, pady=5, sticky="w")

tweet_button = tk.Button(tweet_tab, text="Post Tweet", command=post_tweet, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT)
tweet_button.grid(row=6, column=0, pady=10, sticky="w")
# Create the API keys tab
keys_tab = tk.Frame(notebook, bg=BG_COLOR,padx=20,pady=20)
notebook.add(keys_tab)

client_id_label = tk.Label(keys_tab, text="Client ID:", bg=BG_COLOR, font=FONT)
client_id_label.grid(row=0, column=0, sticky="w")

client_id_entry = tk.Entry(keys_tab, font=FONT)
client_id_entry.grid(row=0, column=1, padx=10, pady=5,sticky="we")
if(client_id):
    client_id_entry.insert(0,client_id)



client_secret_label = tk.Label(keys_tab, text="Client Secret:", bg=BG_COLOR, font=FONT)
client_secret_label.grid(row=1, column=0, sticky="w")
if(client_id):
    client_id_entry.insert(0,client_id)

client_secret_entry = tk.Entry(keys_tab, font=FONT)
client_secret_entry.grid(row=1, column=1, padx=10, pady=5)
if(client_secret):
    client_secret_entry.insert(0,client_secret)

api_key_label = tk.Label(keys_tab, text="API Key:", bg=BG_COLOR, font=FONT)
api_key_label.grid(row=2, column=0, sticky="w")

api_key_entry = tk.Entry(keys_tab, font=FONT)
api_key_entry.grid(row=2, column=1, padx=10, pady=5)
if(api_key):
    api_key_entry.insert(0,api_key)

api_secret_key_label = tk.Label(keys_tab, text="API Secret Key:", bg=BG_COLOR, font=FONT)
api_secret_key_label.grid(row=3, column=0, sticky="w")

api_secret_key_entry = tk.Entry(keys_tab, font=FONT)
api_secret_key_entry.grid(row=3, column=1, padx=10, pady=5)
if(api_secret_key):
    api_secret_key_entry.insert(0,api_secret_key)

bearer_token_label = tk.Label(keys_tab, text="Bearer Token:", bg=BG_COLOR, font=FONT)
bearer_token_label.grid(row=4, column=0, sticky="w")

bearer_token_entry = tk.Entry(keys_tab, font=FONT)
bearer_token_entry.grid(row=4, column=1, padx=10, pady=5)
if(bearer_token):
    bearer_token_entry.insert(0,bearer_token)

access_token_label = tk.Label(keys_tab, text="Access Token:", bg=BG_COLOR, font=FONT)
access_token_label.grid(row=5, column=0, sticky="w")


access_token_entry = tk.Entry(keys_tab, font=FONT)
access_token_entry.grid(row=5, column=1, padx=10, pady=5)
if(access_token):
    access_token_entry.insert(0,access_token)

access_token_secret_label = tk.Label(keys_tab, text="Access Token Secret:", bg=BG_COLOR, font=FONT)
access_token_secret_label.grid(row=6, column=0, sticky="w")

access_token_secret_entry = tk.Entry(keys_tab, font=FONT)
access_token_secret_entry.grid(row=6, column=1, padx=10, pady=5)
if(access_token_secret_entry):
    access_token_secret_entry.insert(0,access_token_secret)

save_keys_button = tk.Button(keys_tab, text="Save Keys", command=save_keys, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT)
save_keys_button.grid(row=7, column=0, columnspan=2, pady=10)

# Pack the notebook and run the main loop
notebook.pack(expand=True, fill="both")
root.mainloop()
