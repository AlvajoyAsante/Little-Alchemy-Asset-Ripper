import os
import pygame
import sys

class ImageValidator:
    def __init__(self, image_folder, names_file, output_file="validation/validation_results.txt", saved_exit_file="validation/exit.txt"):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Image Validator")
        self.image_folder = image_folder
        self.image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]
        self.image_files.sort(key=lambda x: int(os.path.splitext(x)[0]))

        self.output_file = output_file
        self.saved_exit_file = saved_exit_file

        self.font = pygame.font.SysFont("Arial", 20)
        self.validation_results = []

        
        self.current_image_index = 0
        self.current_name_index = 0

        self.load_exit()
        self.load_validation_results()

        print(f"Found {len(self.image_files)} images in {image_folder}")
        
        with open(names_file, 'r') as file:
            self.names = [line.strip() for line in file.readlines()]

        self.show_image()
        

    def save_exit(self):
        with open(self.saved_exit_file, 'w') as file:
            file.write(f"{self.current_image_index}, {self.current_name_index}\n")
        print(f"Exit saved to {self.saved_exit_file}")

    def save_validation_results(self):
        with open(self.output_file, 'w') as file:
            for name, image_file in self.validation_results:
                file.write(f"{name}, {image_file}\n")
        print(f"Validation results saved to {self.output_file}")

    def load_exit(self):
        if os.path.exists(self.saved_exit_file):
            with open(self.saved_exit_file, 'r') as file:
                saved_exit = file.read().strip()
                if saved_exit:
                    try:
                        image_index, name_index = map(int, saved_exit.split(','))
                        self.current_image_index = image_index
                        self.current_name_index = name_index
                    except Exception as e:
                        print(f"Error loading saved exit: {e}")
                        return
    
    def load_validation_results(self):
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r') as file:
                for line in file.readlines():
                    name, image_file = line.strip().split(', ')
                    self.validation_results.append((name, image_file))

    def show_image(self):
        image_path = os.path.join(
            self.image_folder, self.image_files[self.current_image_index])

        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (800, 600))
            self.word_label = self.font.render(
                self.names[self.current_name_index] + "?", True, (255, 255, 255))
        except Exception as e:
            print(f"Error displaying image: {e}")
            self.save_validation_results()
            self.save_exit()
            sys.exit()

    def show_previous_image(self):
        if self.current_image_index != 0:
            self.current_image_index -= 1
        
        self.show_image()

    def show_next_image(self):
        if self.current_image_index == len(self.image_files) - 1:
            self.current_image_index = 0
        else:
            self.current_image_index += 1
        
        self.show_image()

    def validate_yes(self):
        self.validation_results.append(
            (self.names[self.current_name_index], self.image_files[self.current_image_index]))
        
        self.current_name_index += 1

        self.show_next_image()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.show_previous_image()
                    elif event.key == pygame.K_RIGHT:
                        self.show_next_image()
                    elif event.key == pygame.K_y:
                        self.validate_yes()
                    elif event.key == pygame.K_u: # undo
                        if len(self.validation_results) > 0:
                            self.validation_results.pop()
                            self.current_name_index -= 1
                            self.show_previous_image()
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image, (0, 0))
            self.screen.blit(self.word_label, (10, 10))
            
            instructions = [
                "Left Arrow: Previous Image",
                "Right Arrow: Next Image",
                "Y: Validate Yes"
            ]
            
            for i, instruction in enumerate(instructions):
                instruction_label = self.font.render(instruction, True, (255, 255, 255))
                self.screen.blit(instruction_label, (10, 40 + i * 30))
            
            progress = self.current_name_index / len(self.names)
            progress_bar_width = 780
            progress_bar_height = 20
            progress_bar_x = 10
            progress_bar_y = 550
            

            progress_percentage = self.font.render(f"{int(progress * 100)}%", True, (255, 255, 255))
            self.screen.blit(progress_percentage, (progress_bar_x + progress_bar_width + 10, progress_bar_y+ 2))
            
            pygame.draw.rect(self.screen, (255, 255, 255), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
            pygame.draw.rect(self.screen, (0, 255, 0), (progress_bar_x, progress_bar_y, progress_bar_width * progress, progress_bar_height))

            pygame.display.flip()

        pygame.quit()

        self.save_exit()
        self.save_validation_results()

if __name__ == "__main__":
    image_folder = "ELEMENTS/RAW"
    names_file = "validation/names.txt"

    app = ImageValidator(image_folder, names_file)
    app.run()
        
