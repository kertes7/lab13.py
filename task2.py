import json

def load_phones():
    with open("phones.json", "r", encoding="utf-8") as f:
        return json.load(f)

def sort_phones(phones, by="price"):
    return sorted(phones, key=lambda x: x.get(by, 0))

def search_phones(phones, term):
    term = term.lower()
    return [p for p in phones if term in p["title"].lower()]

def print_phones(phones):
    for p in phones:
        print(f"{p['title']} — {p['price']} грн")

if __name__ == "__main__":
    phones = load_phones()
    print(f"Загальна кількість моделей: {len(phones)}\n")

    print("1. Сортування за ціною:")
    sorted_by_price = sort_phones(phones, by="price")
    print_phones(sorted_by_price)

    print("\n2. Пошук:")
    term = input("Введіть ключове слово для пошуку: ")
    found = search_phones(phones, term)
    if found:
        print(f"\nЗнайдено {len(found)} моделей:")
        print_phones(found)
    else:
        print("Нічого не знайдено.")
