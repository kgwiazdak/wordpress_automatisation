import warnings
from dataclasses import dataclass

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


@dataclass
class Scrapper:
    def __init__(self, file_path):
        self.file_path = file_path
        self.book = None
        self.classes_dict = {}
        self._load_book()
        self._extract_text()

    def _load_book(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            warnings.filterwarnings("ignore", category=FutureWarning)
            self.book = epub.read_epub(self.file_path)

    def _extract_text(self):
        # Iterate over all document items in the book
        for item_document in [item for item in self.book.get_items() if item.get_type() == ebooklib.ITEM_DOCUMENT]:
            text = item_document.get_content().decode('utf-8')
            bs_text = BeautifulSoup(text, 'html.parser')
            for element in bs_text.find_all(class_=True):
                classes = element.get("class")
                if classes:
                    for cls in classes:
                        text_content = element.get_text(strip=True)
                        if text_content:  # Optional: skip empty text
                            self.classes_dict.setdefault(cls, []).append(text_content)


def print_everything(text_list, number_of_lines=None):
    if number_of_lines:
        text_list = text_list[:number_of_lines]
    for text in text_list:
        print(text)
        pass
    print()


def text_to_class(text):
    classes = []
    for key, values in classes_dict.items():
        for value in values:
            if text in value:
                classes.append(key)
    return classes


def find_proper_section_name(all_text, section_names, first_line):
    for i, section_name in enumerate(section_names):
        index = all_text.find(f"{section_name}{first_line}")
        if index != -1:
            section_names.pop(i)
            return section_name, index
    raise ValueError(f"Could not find proper section name for {first_line}")


def show_content(classes_dict):
    read = []

    def append_and_print(line):
        read.append(line)
        print(line)

    section_names = get_section_names(classes_dict)
    number_of_sections = len(section_names)
    all_text = classes_dict['Basic-Graphics-Frame'][0]
    paragraphs = classes_dict['Tekst_PLAT_VervolgAlinea']
    first_paragraphs_lines = classes_dict['Tekst_PLAT_EersteAlinea']
    j = 0

    print_everything(classes_dict["Tekst_PLAT_Initiaal_4r"])
    for i in range(number_of_sections):
        first_line = first_paragraphs_lines[i]
        section_name, index = find_proper_section_name(all_text, section_names, first_line)
        last_line = all_text[index - 100:index - 1]
        if read and last_line in read[-1]:
            print()
            append_and_print(section_name)
            append_and_print(first_line)
            continue
        while last_line not in paragraphs[j - 1]:
            append_and_print(paragraphs[j])
            j += 1
        print()
        append_and_print(section_name)
        append_and_print(first_line)
    while j < len(paragraphs):
        append_and_print(paragraphs[j])
        j += 1


def print_text(classes_dict):
    show_authors(classes_dict)
    show_title_and_intro(classes_dict)
    show_content(classes_dict)
    show_literature(classes_dict)


def show_literature(classes_dict):
    print_everything(classes_dict["Literatuur_LITERATUURKOP"])
    print_everything(classes_dict["Literatuur_LITERATUURTXT"])


def show_title_and_intro(classes_dict):
    print_everything(classes_dict['Kop-groot'])
    print_everything(classes_dict['Intro_INTRO'])
    print_everything(classes_dict['Intro_IN-HET-KORT-TXT'])


def show_authors(classes_dict):
    print_everything(classes_dict['Auteurs_AUTEURSNAAM'])
    print_everything(classes_dict['Auteurs_AUTEURSVERMELDING'])


def get_section_names(classes_dict):
    try:
        section_names = classes_dict['Tekst_TUSSENKOP'] + classes_dict['Tekst_TUSSENKOPCURSIEF']
    except KeyError:
        section_names = classes_dict['Tekst_TUSSENKOP']
    return section_names


if __name__ == "__main__":
    file_paths = [
        # r"C:\Users\user\PycharmProjects\pythonProject8\Krzysztof\Beijenberg\000-000_Bleijenberg.epub",
        # r"C:\Users\user\PycharmProjects\pythonProject8\Krzysztof\Groot\543-545_Groot.epub",
        # r"C:\Users\user\PycharmProjects\pythonProject8\Krzysztof\Pieters\000-000_Pieters.epub",
        # r"C:\Users\user\PycharmProjects\pythonProject8\Krzysztof\Pomp\000-000_Pomp.epub",
        # r"C:\Users\user\PycharmProjects\pythonProject8\Krzysztof\Sniekers\536-537_Sniekers2.epub",
        # r"C:\Users\user\PycharmProjects\pythonProject8\Krzysztof\Thiel\540-542_Thiel.epub", #TODO
        r"C:\Users\user\PycharmProjects\pythonProject8\Krzysztof\vVerschuer\000-000_vVerschuer.epub",
        # r"C:\Users\user\PycharmProjects\pythonProject8\Krzysztof\Wisman\538-539_Wisman.epub"
    ]
    for file_path in file_paths:
        reader = Scrapper(file_path)
        classes_dict = reader.classes_dict
        print_text(classes_dict)
