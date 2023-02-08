#!/usr/bin/python

import json
import os
import webbrowser
from tkinter import Tk, Label, Button, StringVar


def main():
    root = Tk()
    root.title("habr news app")
    root.geometry("1000x870")

    with open(f"/home/{os.getlogin()}/habr/posts.json") as file:
        posts = json.load(file)

    cur_post = 0
    post = posts[cur_post]

    post_time = StringVar(root)
    post_time.set(post['time'])
    post_title = StringVar(root)
    post_title.set(post['title'])
    post_text = StringVar(root)
    post_text.set(post['post'])
    post_link = StringVar(root)
    post_link.set(post['link'])

    def prev_post(event):
        nonlocal cur_post
        if cur_post > 0:
            cur_post = cur_post - 1
            post = posts[cur_post]
            post_time.set(post['time'])
            post_title.set(post['title'])
            post_text.set(post['post'])
            post_link.set(post['link'])

            lbl_post_title.configure(textvariable=post_title)
            lbl_post.configure(textvariable=post_text)

            btn_next.configure(state="normal")
        else:
            cur_post = 0
        if cur_post == 0:
            btn_prev.configure(state="disabled")

    def next_post(event):
        nonlocal cur_post
        if cur_post < len(posts) - 1:
            cur_post = cur_post + 1
            post = posts[cur_post]
            post_time.set(post['time'])
            post_title.set(post['title'])
            post_text.set(post['post'])
            post_link.set(post['link'])

            lbl_post_title.configure(textvariable=post_title)
            lbl_post.configure(textvariable=post_text)

            btn_prev.configure(state="normal")
        else:
            cur_post = len(posts) - 1
        if cur_post == len(posts) - 1:
            btn_next.configure(state='disabled')

    lbl_post_time = Label(textvariable=post_time, font="Calibri, 14")
    lbl_post_title = Label(textvariable=post_title, wraplength=1000, font="Calibri, 18",
                           relief="groove", background="yellow", height=3)
    lbl_post = Label(textvariable=post_text, wraplength=1000, font='Calibri, 14',
                     justify="left", relief="solid", background="lightblue", height=27, anchor='n')

    btn_prev = Button(text="<=", state="disabled", command=prev_post)
    btn_next = Button(text="=>", command=next_post)

    lbl_post_time.pack()
    lbl_post_title.pack()
    lbl_post.pack()

    btn_prev.pack(side='left')
    btn_next.pack(side="right")

    def open_in_browser(event):
        webbrowser.open(post_link.get())

    root.bind('o', open_in_browser)
    root.bind('n', next_post)
    root.bind('N', prev_post)

    root.mainloop()


if __name__ == "__main__":
    main()
