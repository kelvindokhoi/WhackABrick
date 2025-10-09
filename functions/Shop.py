from functions.FilePaths import x2_image_path,x3_image_path,x4_image_path,x5_image_path,x6_image_path,x7_image_path,x8_image_path,x9_image_path,x10_image_path,max_image_path
from functions.FilePaths import enhanced_cursor_image_path
from functions.FilePaths import gold_buff_image_path
from functions.FilePaths import brick17_image_path
from functions.Resource_Reader import image_loader
from functions.Buffs import BUFF
from functions.Colors import * #type:ignore
from functions.All_Buttons import BuyButtonObject


from pygame.font import Font
import pygame

class ShopObject:
    def __init__(self) -> None:
        #score multipliers
        self.multiplier_image_dimension = (250,120)
        self.x2_image = image_loader(x2_image_path,self.multiplier_image_dimension)
        self.x3_image = image_loader(x3_image_path,self.multiplier_image_dimension)
        self.x4_image = image_loader(x4_image_path,self.multiplier_image_dimension)
        self.x5_image = image_loader(x5_image_path,self.multiplier_image_dimension)
        self.x6_image = image_loader(x6_image_path,self.multiplier_image_dimension)
        self.x7_image = image_loader(x7_image_path,self.multiplier_image_dimension)
        self.x8_image = image_loader(x8_image_path,self.multiplier_image_dimension)
        self.x9_image = image_loader(x9_image_path,self.multiplier_image_dimension)
        self.x10_image = image_loader(x10_image_path,self.multiplier_image_dimension)
        self.max_image = image_loader(max_image_path,self.multiplier_image_dimension)
        self.shift_everything_x = 100
        self.score_multiplier_position = (300+self.shift_everything_x,200)
        self.score_multiplier_name_position = (220+self.shift_everything_x, 330)
        self.score_multiplier_explanation_position = (300+self.shift_everything_x, 400)
        self.score_multiplier_explanation_font = pygame.font.SysFont('Corbel',32)
        self.score_multiplier_font = pygame.font.SysFont('Corbel',62)
        self.score_multiplier_font.set_bold(True)
        self.multiplier_explanation_text = self.score_multiplier_explanation_font.render("Increases your point multiplier.", True, black,white)

        self.gold_font = pygame.font.SysFont('Corbel',62)
        self.gold_font.set_bold(True)

        self.gold_position = (20,140)

        self.num_button_x = 2
        self.num_button_y = 2
        self.buy_button_size = (200,80)
        self.buy_button_hover_size = (self.buy_button_size[0]-10,self.buy_button_size[1]-5)
        self.buy_button_space_scalar_x = 300 + 300
        self.buy_button_space_scalar_y = 300 - 20

        self.all_buy_buttons = [[None for _ in range(self.num_button_x)]for _ in range(self.num_button_y)]
        for a in range(self.num_button_x):
            for b in range(self.num_button_y):
                center = (320+self.shift_everything_x+self.buy_button_space_scalar_x*a+self.buy_button_size[0]*a,400+self.buy_button_space_scalar_y*b+b*self.buy_button_size[1])
                self.all_buy_buttons[b][a] = BuyButtonObject(self.buy_button_size,self.buy_button_hover_size,center) #type: ignore
        
        # Placeholder image for AutoClick (square 1:1)
        self.autoclick_image_dimension = (120, 120)
        self.autoclick_image = image_loader(enhanced_cursor_image_path, self.autoclick_image_dimension)
        self.autoclick_name = "AutoClick"
        self.autoclick_price = 50

        # AutoClick item positions
        self.autoclick_image_position = (
            self.all_buy_buttons[0][1].rect.centerx +80 - self.autoclick_image_dimension[0] // 2,
            self.all_buy_buttons[0][1].rect.top - self.autoclick_image_dimension[1] - 30
        )
        self.autoclick_name_position = (
            self.all_buy_buttons[0][1].rect.centerx -25 ,
            self.autoclick_image_position[1] + self.autoclick_image_dimension[1]
        )
        self.autoclick_name_text = self.score_multiplier_font.render(self.autoclick_name, True, yellow, white)
        self.autoclick_explanation_font = pygame.font.SysFont('Corbel',32)
        self.autoclick_explanation_text = self.autoclick_explanation_font.render("Makes the cursor bigger and autoclicks.", True, black, white)
        self.autoclick_explanation_position = (self.autoclick_name_position[0], self.autoclick_name_position[1] + 60)

        # Gold Buff item
        self.gold_buff_image_dimension = (200, 200)
        self.gold_buff_image = image_loader(gold_buff_image_path, self.gold_buff_image_dimension)
        self.gold_buff_base_price = 10

        # Gold Buff item positions
        self.gold_buff_image_position = (
            self.all_buy_buttons[1][0].rect.centerx +80 - self.gold_buff_image_dimension[0] // 2,
            self.all_buy_buttons[1][0].rect.top - self.gold_buff_image_dimension[1] - 30
        )
        self.gold_buff_name_position = (
            self.all_buy_buttons[1][0].rect.centerx -25 ,
            self.gold_buff_image_position[1] + self.gold_buff_image_dimension[1]
        )
        self.gold_buff_explanation_font = pygame.font.SysFont('Corbel',32)
        self.gold_buff_explanation_text = self.gold_buff_explanation_font.render("Adds 2 gold each when you finish the game.", True, black, white)
        self.gold_buff_explanation_position = (self.gold_buff_name_position[0], self.gold_buff_name_position[1] + 60)

        # Brick 17 Pro Max item
        self.brick17_image_dimension = (200, 200)
        self.brick17_image = image_loader(brick17_image_path, self.brick17_image_dimension)
        self.brick17_name = "Brick 17 Pro Max"
        self.brick17_price = 999

        # Brick 17 item positions
        self.brick17_image_position = (
            self.all_buy_buttons[1][1].rect.centerx +80 - self.brick17_image_dimension[0] // 2,
            self.all_buy_buttons[1][1].rect.top - self.brick17_image_dimension[1] - 30
        )
        self.brick17_name_position = (
            self.all_buy_buttons[1][1].rect.centerx -25 ,
            self.brick17_image_position[1] + self.brick17_image_dimension[1]
        )
        self.brick17_name_text = self.score_multiplier_font.render(self.brick17_name, True, yellow, white)
        self.brick17_explanation_font = pygame.font.SysFont('Corbel',32)
        self.brick17_explanation_text = self.brick17_explanation_font.render("Deletes the whole board on click.", True, black, white)
        self.brick17_explanation_position = (self.brick17_name_position[0], self.brick17_name_position[1] + 60)
        
        # Feedback + click-tracking
        self.feedback_text = None
        self.feedback_timer = 0

        # mouse-edge detection + debounce
        self._mouse_was_pressed = False
        self._last_click_time = 0
        self._click_debounce_ms = 200  # ms between allowed clicks
    
    def determine_multiplier_image(self,buffs):
        if BUFF.X10SCOREMULTIPLIER in buffs:
            return 'Maxed Out!!!',self.max_image,11
        elif BUFF.X9SCOREMULTIPLIER in buffs:
            return 'X10 Score Multiplier',self.x10_image,10
        elif BUFF.X8SCOREMULTIPLIER in buffs:
            return 'X9 Score Multiplier', self.x9_image,9
        elif BUFF.X7SCOREMULTIPLIER in buffs:
            return 'X8 Score Multiplier', self.x8_image,8
        elif BUFF.X6SCOREMULTIPLIER in buffs:
            return 'X7 Score Multiplier', self.x7_image,7
        elif BUFF.X5SCOREMULTIPLIER in buffs:
            return 'X6 Score Multiplier', self.x6_image,6
        elif BUFF.X4SCOREMULTIPLIER in buffs:
            return 'X5 Score Multiplier', self.x5_image,5
        elif BUFF.X3SCOREMULTIPLIER in buffs:
            return 'X4 Score Multiplier', self.x4_image,4
        elif BUFF.X2SCOREMULTIPLIER in buffs:
            return 'X3 Score Multiplier', self.x3_image,3
        else:
            return 'X2 Score Multiplier', self.x2_image,2
    
    def blit_shop_items(self, screen, buffs, playerGold, cursor_Rect):
        multiplier_name, multiplier_image, multiplier_price = self.determine_multiplier_image(buffs)
        multiplier_name_text = self.score_multiplier_font.render(multiplier_name, True, yellow, white)
        gold_text = self.score_multiplier_font.render(f"Gold: {playerGold}", True, yellow, white)

        image_rect = multiplier_image.get_rect(topleft=self.score_multiplier_position)
        name_rect = multiplier_name_text.get_rect(topleft=self.score_multiplier_name_position)
        self.mult_exp_rect = image_rect.union(name_rect)

        screen.blit(multiplier_image, self.score_multiplier_position)
        screen.blit(multiplier_name_text, self.score_multiplier_name_position)
        screen.blit(gold_text, self.gold_position)

        # Hover popup for multiplier explanation
        if cursor_Rect.colliderect(self.mult_exp_rect):
            screen.blit(self.multiplier_explanation_text, self.score_multiplier_explanation_position)

        # Draw buy buttons
        hover_explanation_font = pygame.font.SysFont('Corbel', 28)
        for a in range(self.num_button_x):
            for b in range(self.num_button_y):
                button = self.all_buy_buttons[b][a]
                is_hovering = button.if_hover(cursor_Rect)
                button.blit_button(screen)

                # Hover explanation
                if is_hovering and a == b == 0:
                    explanation_text = f"Buy upgrade for {multiplier_price**2 if multiplier_price != 11 else 0} gold"
                    text_surface = hover_explanation_font.render(explanation_text, True, black, white)
                    text_rect = text_surface.get_rect(midleft=(button.rect.right + 20, button.rect.centery))
                    screen.blit(text_surface, text_rect)

        # --- Draw feedback text (non-blocking) ---
        if self.feedback_text:
            elapsed = pygame.time.get_ticks() - self.feedback_timer
            if elapsed < 2000:  # 2 seconds
                feedback_surface = hover_explanation_font.render(self.feedback_text, True, red, white)
                feedback_rect = feedback_surface.get_rect(center=(screen.get_width() // 2, 100))
                screen.blit(feedback_surface, feedback_rect)
            else:
                self.feedback_text = None
        
        # Draw AutoClick image and name
        autoclick_image_rect = self.autoclick_image.get_rect(topleft=self.autoclick_image_position)
        autoclick_name_rect = self.autoclick_name_text.get_rect(topleft=self.autoclick_name_position)
        autoclick_hover_rect = autoclick_image_rect.union(autoclick_name_rect)
        screen.blit(self.autoclick_image, self.autoclick_image_position)
        screen.blit(self.autoclick_name_text, self.autoclick_name_position)

        # Hover popup for AutoClick explanation
        if cursor_Rect.colliderect(autoclick_hover_rect):
            screen.blit(self.autoclick_explanation_text, self.autoclick_explanation_position)

        # Hover explanation for AutoClick
        slot_button = self.all_buy_buttons[0][1]
        if slot_button.if_hover(cursor_Rect):
            hover_explanation_font = pygame.font.SysFont('Corbel', 28)
            text = f"Buy AutoClick for {self.autoclick_price} gold"
            hover_surface = hover_explanation_font.render(text, True, black, white)
            text_rect = hover_surface.get_rect(midleft=(slot_button.rect.right + 20, slot_button.rect.centery))
            screen.blit(hover_surface, text_rect)

        # Draw Gold Buff image and name
        num_gold_buffs = buffs.count(BUFF.GOLDBUFF)
        next_level = num_gold_buffs + 1
        gold_buff_name_text = self.score_multiplier_font.render(f"Gold Buff x{next_level}", True, yellow, white)
        gold_buff_image_rect = self.gold_buff_image.get_rect(topleft=self.gold_buff_image_position)
        gold_buff_name_rect = gold_buff_name_text.get_rect(topleft=self.gold_buff_name_position)
        gold_buff_hover_rect = gold_buff_image_rect.union(gold_buff_name_rect)
        screen.blit(self.gold_buff_image, self.gold_buff_image_position)
        screen.blit(gold_buff_name_text, self.gold_buff_name_position)

        # Hover popup for Gold Buff explanation
        if cursor_Rect.colliderect(gold_buff_hover_rect):
            screen.blit(self.gold_buff_explanation_text, self.gold_buff_explanation_position)

        # Hover explanation for Gold Buff
        gold_slot_button = self.all_buy_buttons[1][0]
        if gold_slot_button.if_hover(cursor_Rect):
            hover_explanation_font = pygame.font.SysFont('Corbel', 28)
            cost = self.gold_buff_base_price * (2 ** num_gold_buffs)
            text = f"Buy Gold Buff for {cost} gold"
            hover_surface = hover_explanation_font.render(text, True, black, white)
            text_rect = hover_surface.get_rect(midleft=(gold_slot_button.rect.right + 20, gold_slot_button.rect.centery))
            screen.blit(hover_surface, text_rect)

        # Draw Brick 17 Pro Max image and name
        brick17_image_rect = self.brick17_image.get_rect(topleft=self.brick17_image_position)
        brick17_name_rect = self.brick17_name_text.get_rect(topleft=self.brick17_name_position)
        brick17_hover_rect = brick17_image_rect.union(brick17_name_rect)
        screen.blit(self.brick17_image, self.brick17_image_position)
        screen.blit(self.brick17_name_text, self.brick17_name_position)

        # Hover popup for Brick 17 Pro Max explanation
        if cursor_Rect.colliderect(brick17_hover_rect):
            screen.blit(self.brick17_explanation_text, self.brick17_explanation_position)

        # Hover explanation for Brick 17 Pro Max
        brick_slot_button = self.all_buy_buttons[1][1]
        if brick_slot_button.if_hover(cursor_Rect):
            hover_explanation_font = pygame.font.SysFont('Corbel', 28)
            text = f"Buy Brick 17 Pro Max for {self.brick17_price} gold"
            hover_surface = hover_explanation_font.render(text, True, black, white)
            text_rect = hover_surface.get_rect(midleft=(brick_slot_button.rect.right + 20, brick_slot_button.rect.centery))
            screen.blit(hover_surface, text_rect)




    def if_clicked(self, events, buffs, playerGold, music):
        """
        Handles all click logic for multiplier and buy buttons.
        Properly detects clicks (not holds), prevents freezing, and shows messages.
        """
        now = pygame.time.get_ticks()

        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                pos = ev.pos
                playerGold, buffs = self._handle_purchase_at_pos(pos, buffs, playerGold, now, music)

        return playerGold, buffs


    def _handle_purchase_at_pos(self, pos, buffs, playerGold, now, music):
        # --- Check if clicked multiplier or buy buttons ---
        clicked_multiplier_area = hasattr(self, "mult_exp_rect") and self.mult_exp_rect.collidepoint(pos)

        clicked_buy_button = False
        clicked_slot_a, clicked_slot_b = None, None
        for a in range(self.num_button_x):
            for b in range(self.num_button_y):
                button = self.all_buy_buttons[b][a]
                if button.rect.collidepoint(pos):
                    clicked_buy_button = True
                    clicked_slot_a, clicked_slot_b = a, b
                    break
            if clicked_buy_button:
                break

        if not (clicked_multiplier_area or clicked_buy_button):
            return playerGold, buffs

        now_time = pygame.time.get_ticks()

        # --- Handle slot [0][1] for AutoClick ---
        if clicked_slot_a == 1 and clicked_slot_b == 0:
            if BUFF.AUTOCLICK in buffs:
                self.feedback_text = "AutoClick already purchased!"
                self.feedback_timer = now_time
                return playerGold, buffs
            if playerGold < self.autoclick_price:
                self.feedback_text = f"Not enough gold! Need {self.autoclick_price}."
                self.feedback_timer = now_time
                return playerGold, buffs

            # Purchase succeeds
            playerGold -= self.autoclick_price
            buffs.append(BUFF.AUTOCLICK)
            music.play_get_coin_sound()
            self.feedback_text = "Purchased AutoClick!"
            self.feedback_timer = now_time
            return playerGold, buffs

        # --- Handle slot [1][0] for Gold Buff ---
        elif clicked_slot_a == 0 and clicked_slot_b == 1:
            num_gold_buffs = buffs.count(BUFF.GOLDBUFF)
            cost = self.gold_buff_base_price * (2 ** num_gold_buffs)
            if playerGold < cost:
                self.feedback_text = f"Not enough gold! Need {cost}."
                self.feedback_timer = now_time
                return playerGold, buffs

            # Purchase succeeds
            playerGold -= cost
            buffs.append(BUFF.GOLDBUFF)
            music.play_get_coin_sound()
            next_level = num_gold_buffs + 1
            self.feedback_text = f"Purchased Gold Buff x{next_level}!"
            self.feedback_timer = now_time
            return playerGold, buffs

        # --- Handle slot [1][1] for Brick 17 Pro Max ---
        elif clicked_slot_a == 1 and clicked_slot_b == 1:
            if BUFF.BRICK17 in buffs:
                self.feedback_text = "Brick 17 Pro Max already purchased!"
                self.feedback_timer = now_time
                return playerGold, buffs
            if playerGold < self.brick17_price:
                self.feedback_text = f"Not enough gold! Need {self.brick17_price}."
                self.feedback_timer = now_time
                return playerGold, buffs

            # Purchase succeeds
            playerGold -= self.brick17_price
            buffs.append(BUFF.BRICK17)
            music.play_get_coin_sound()
            self.feedback_text = "Purchased Brick 17 Pro Max!"
            self.feedback_timer = now_time
            return playerGold, buffs

        # --- Existing multiplier logic ---
        multiplier_name, _, multiplier_price = self.determine_multiplier_image(buffs)

        # Already maxed
        if multiplier_price == 11:
            self.feedback_text = "Multiplier is already maxed!"
            self.feedback_timer = now_time
            return playerGold, buffs

        cost = multiplier_price ** 3

        # Not enough gold
        if playerGold < cost:
            self.feedback_text = f"Not enough gold! Need {cost}."
            self.feedback_timer = now_time
            return playerGold, buffs

        # Purchase succeeds
        playerGold -= cost
        next_buff = getattr(BUFF, f"X{multiplier_price}SCOREMULTIPLIER")
        if next_buff not in buffs:
            buffs.append(next_buff)
        music.play_get_coin_sound()
        self.feedback_text = f"Purchased {multiplier_name}!"
        self.feedback_timer = now_time

        return playerGold, buffs