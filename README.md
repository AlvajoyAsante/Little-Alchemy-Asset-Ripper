# Little-Alchemy-Asset-Ripper

Downloads icons from Little Alchemy, processes them, creates a spritesheet, and provides a Pygame quiz. Handles cases where there are more images than names via the pygame quiz.

## Features

*   Downloads and resizes images (32x32).
*   Handles transparency (alpha channel).
*   Indexed color conversion (256 colors).
*   Spritesheet creation with padding and optional text labels.
*   Pygame-based interactive quiz.
*   Handles more images than provided names (unnamed images are included in the spritesheet without labels, and the quiz only uses named elements).

## Requirements

*   Python 3.7+
*   `Pillow`, `requests`, `pygame`: `pip install Pillow requests pygame`

## Usage

1.  `git clone <repository_url>`
2.  `cd Little-Alchemy-Asset-Ripper`
3.  `python element_downloader.py`

## Configuration

Modify these variables in `if __name__ == "__main__":`:

*   `url_template`: Image URL template (`{number}` placeholder).
*   `start_number`, `end_number`: Image number range.
*   `output_folder`, `spritesheet_output`: Output paths.
*   `names`: List of element names (order matters). Fewer names than images are handled gracefully.
*   `images_per_row`, `padding`: Spritesheet layout options.

## Spritesheet & Quiz

The spritesheet is saved as `elements_spritesheet.png`. The Pygame quiz tests element identification (y/n).

## License

[MIT](github.com/AlvajoyAsante/Little-Alchemy-Asset-Ripper/LICENSE)

## Acknowledgements

*   Little Alchemy
*   Little Alchemy hints website
*   AI was used in the development of the project.

---
©️ 2024 - Alvajoy Asante
