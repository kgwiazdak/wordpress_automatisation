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
    print()


def text_to_class(text):
    classes = []
    for key, values in classes_dict.items():
        for value in values:
            if text in value:
                classes.append(key)
    return classes


def print_text(classes_dict):
    section_names = classes_dict['Tekst_TUSSENKOP']
    number_of_sections = len(section_names)
    all = classes_dict['Basic-Graphics-Frame'][0]
    paragraphs = classes_dict['Tekst_PLAT_VervolgAlinea']
    j = 0

    print_everything(classes_dict['Kop-groot'])
    print_everything(classes_dict['Intro_INTRO'])
    print_everything(classes_dict['Intro_IN-HET-KORT-TXT'])
    print_everything(classes_dict["Tekst_PLAT_Initiaal_4r"])

    for i in range(number_of_sections):
        section_name = section_names[i]
        first_line = classes_dict['Tekst_PLAT_EersteAlinea'][i]
        index = all.find(f"{section_name}{first_line}")
        index_range = (index - 100, index - 1)
        prev_text = all[index_range[0]:index_range[1]]
        while prev_text not in paragraphs[j - 1]:
            print(paragraphs[j])
            j += 1
        print()
        print(section_name)
        print(first_line)
    while j < len(paragraphs):
        print(paragraphs[j])
        j += 1


if __name__ == "__main__":
    file_path = r"C:\Users\user\PycharmProjects\pythonProject8\Krzysztof\Beijenberg\000-000_Bleijenberg.epub"
    reader = Scrapper(file_path)
    classes_dict = reader.classes_dict
    print_text(classes_dict)
