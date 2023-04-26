from chatgpt import ChatGPT
import yaml


def fluidify(split, start_chat) -> str:
    chatgpt = ChatGPT()
    chatgpt.start_session()
    chatgpt.chat(start_chat)

    book = ""

    for part in split:
        book += chatgpt.chat(part)

    chatgpt.close_session()
    return book


def load_book(path) -> str:
    with open(path, 'r') as f:
        return f.read().replace('\n', '')


def split_book(book, max_len) -> list[str]:
    return list(map(''.join, zip(*[iter(book)] * max_len)))


def save_book(book, title):
    with open(f'./output/{title}.txt', 'w') as f:
        f.write(book)


if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.CLoader)

    book = load_book(config['book']['path'])
    split = split_book(book, config['chatgpt']['max_prompt_length'])

    fluid_book = fluidify(split, config['chatgpt']['start_chat'])
    save_book(fluid_book, config['book']['title'])

    print(f"Finished fluidifying {config['book']['title']}")
    print(f"Saved {config['book']['title']} to {config['book']['path']}")