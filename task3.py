import json
import tkinter as tk
from tkinter import ttk, messagebox

def load_phones():
    with open("phones.json", "r", encoding="utf-8") as f:
        return json.load(f)

class PhoneApp:
    def __init__(self, root, phones):
        self.root = root
        self.phones = phones
        self.filtered = phones.copy()

        root.title("Телефони Apple (Rozetka)")

        top_frame = tk.Frame(root)
        top_frame.pack(pady=5)

        self.search_entry = tk.Entry(top_frame, width=40)
        self.search_entry.pack(side="left", padx=5)

        search_btn = tk.Button(top_frame, text="Пошук", command=self.search)
        search_btn.pack(side="left")

        sort_btn = tk.Button(top_frame, text="Сортувати за ціною", command=self.sort)
        sort_btn.pack(side="left", padx=10)

        self.tree = ttk.Treeview(root, columns=("Назва", "Ціна"), show="headings")
        self.tree.heading("Назва", text="Назва")
        self.tree.heading("Ціна", text="Ціна (грн)")
        self.tree.pack(padx=10, pady=10)

        self.tree.bind("<Double-1>", self.show_details)

        self.update_tree()

    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.filtered:
            self.tree.insert("", "end", values=(p["title"], p["price"]))

    def search(self):
        term = self.search_entry.get().lower()
        self.filtered = [p for p in self.phones if term in p["title"].lower()]
        self.update_tree()

    def sort(self):
        self.filtered.sort(key=lambda x: x.get("price", 0))
        self.update_tree()

    def show_details(self, _event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        title, price = item["values"]
        phone = next((p for p in self.phones if p["title"] == title), None)
        if phone:
            info = f"Назва: {phone['title']}\nЦіна: {phone['price']} грн\nID: {phone['id']}\nРейтинг: {phone.get('rating') or 'Немає'}"
            messagebox.showinfo("Деталі", info)

if __name__ == "__main__":
    phones = load_phones()
    root = tk.Tk()
    app = PhoneApp(root, phones)
    root.mainloop()

