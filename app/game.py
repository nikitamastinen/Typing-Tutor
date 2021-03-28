import threading
from copy import copy
import time

import pygame
import sys


class Game:
    left_text_shift = 20
    right_text_shift = 20
    top_text_shift = 20
    bottom_text_shift = 50
    max_text_length = 400
    text_size = 24
    screen_height = 500
    screen_width = 400
    shift_btw_lines = 10

    number_of_symbols = 0
    number_of_errors = 0
    number_of_time_units = 0
    is_last_symbol_wrong = False

    reloading_statistics_time = 0.5

    is_finished = False

    def __init__(self, text):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_height, self.screen_width))
        self.font = pygame.font.SysFont('Verdana', self.text_size, bold=True)
        self.color = pygame.Color('black')
        self.screen.fill(pygame.Color('white'))
        self.text = text[0:min(self.max_text_length, len(text))]
        self.text = self.text.replace('\n', ' ')

    def init_game(self):
        start_message = self.font.render(f"Press space to start...", False, pygame.Color('grey'))
        self.screen.blit(
            start_message, (self.left_text_shift, self.top_text_shift)
        )
        pygame.display.update()
        while True:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYUP and event.unicode == ' ':
                    start_message = self.font.render(f"Press space to start...", False, pygame.Color('white'))
                    self.screen.blit(
                        start_message, (self.left_text_shift, self.top_text_shift)
                    )
                    pygame.display.update()
                    return

    def change_state(self, prefix, is_wrong_symbol):
        words = self.text
        max_width, max_height = self.screen.get_size()
        x, y = self.right_text_shift, self.top_text_shift
        current_length = 0
        for index, string in enumerate(words):
            copy_index = index
            copy_string = copy(string)
            word_width, word_height = self.font.size(copy_string)
            if x + word_width >= max_width - self.right_text_shift:
                x = self.left_text_shift  # Reset the x.
                y += word_height  # Start on new row.
            for word in string:
                current_length += 1
                word_width, word_height = self.font.size(word)
                if current_length <= prefix:
                    word_surface = self.font.render(word, False, pygame.Color('green'))
                elif current_length == prefix + 1 and is_wrong_symbol:
                    word_surface = self.font.render(word, False, pygame.Color('red'))
                else:
                    word_surface = self.font.render(word, False, pygame.Color('black'))
                self.screen.blit(word_surface, (x, y))
                x += word_width
        pygame.display.update()

    def show_statistics(self):
        while not self.is_finished:
            if not self.number_of_time_units == 0:
                spm = int(60 * self.number_of_symbols / (self.number_of_time_units * self.reloading_statistics_time))
            else:
                spm = 0
            accuracy = int(100 - self.number_of_errors / len(self.text) * 100)
            result = self.font.render(f"SYMBOLS PER MINUTE: {spm}", False, pygame.Color('grey'))
            errors = self.font.render(f"ACCURACY: {accuracy}", False, pygame.Color('grey'))

            self.screen.fill(
                rect=pygame.Rect(self.right_text_shift,
                                 self.screen_width - self.bottom_text_shift -
                                 self.font.size('S')[0] - self.shift_btw_lines,
                                 self.screen_width, self.screen_height), color=pygame.Color('white')
            )
            self.screen.blit(
                result, (
                    self.right_text_shift,
                    self.screen_width - self.bottom_text_shift -
                    self.font.size('S')[0] - self.shift_btw_lines
                )
            )
            self.screen.blit(
                errors, (self.right_text_shift, self.screen_width - self.bottom_text_shift)
            )
            pygame.display.update()
            time.sleep(self.reloading_statistics_time)
            self.number_of_time_units += 1

    def run(self):
        self.change_state(prefix=0, is_wrong_symbol=False)
        correct_prefix = 0
        while True:
            if correct_prefix == len(self.text):
                self.is_finished = True
                pass
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                try:
                    if event.type == pygame.KMOD_SHIFT:
                        pass
                    elif event.unicode == self.text[correct_prefix] and event.type == pygame.KEYUP:
                        self.is_last_symbol_wrong = False
                        self.number_of_symbols += 1
                        correct_prefix += 1
                        self.change_state(prefix=correct_prefix, is_wrong_symbol=False)
                    elif event.type == pygame.KEYUP and event.unicode != '':
                        if not self.is_last_symbol_wrong:
                            self.number_of_errors += 1
                            self.is_last_symbol_wrong = True
                        self.change_state(prefix=correct_prefix, is_wrong_symbol=True)
                    else:
                        pass
                except Exception:
                    pass

    def play(self):
        timer_task = threading.Thread(target=self.show_statistics, args=[], daemon=False)
        timer_task.start()
        self.run()
