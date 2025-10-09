from functions.FilePaths import x2_image_path,x3_image_path,x4_image_path,x5_image_path,x6_image_path,x7_image_path,x8_image_path,x9_image_path,x10_image_path,max_image_path
from functions.FilePaths import enhanced_cursor_image_path
from functions.FilePaths import gold_buff_image_path
from functions.FilePaths import brick17_image_path
from functions.FilePaths import boss_killer_image_path, chain_master_image_path
from functions.Resource_Reader import image_loader
from functions.Buffs import BUFF
from functions.Colors import * #type:ignore
from functions.All_Buttons import BuyButtonObject


from pygame.font import Font
import pygame

class ShopObject:
    def __init__(self) -> None:
        # Grid setup: 3 columns x 2 rows
        self.num_button_x = 3
        self.num_button_y = 2
        
        # Buy button settings
        self.buy_button_size = (200, 80)
        self.buy_button_hover_size = (self.buy_button_size[0]-10, self.buy_button_size[1]-5)
        
        # Grid spacing
        self.grid_start_x = 350
        self.grid_start_y = 450
        self.spacing_x = 550  # Horizontal space between items
        self.spacing_y = 320  # Changed from 350 to 320 (30px smaller vertical gap)
                
        # Fonts
        self.item_name_font = pygame.font.SysFont('Corbel', 48)
        self.item_name_font.set_bold(True)
        self.explanation_font = pygame.font.SysFont('Corbel', 28)
        self.gold_font = pygame.font.SysFont('Corbel', 62)
        self.gold_font.set_bold(True)
        
        # Gold position
        self.gold_position = (20, 140)
        
        # Create buy buttons grid
        self.all_buy_buttons = [[None for _ in range(self.num_button_x)] for _ in range(self.num_button_y)]
        for row in range(self.num_button_y):
            for col in range(self.num_button_x):
                center_x = self.grid_start_x + col * self.spacing_x
                center_y = self.grid_start_y + row * self.spacing_y
                button_y = center_y - 80  # Button is 40px lower than item center
                self.all_buy_buttons[row][col] = BuyButtonObject(
                    self.buy_button_size,
                    self.buy_button_hover_size,
                    (center_x, button_y)
                )
        
        # === ITEM 1: Score Multiplier (0,0) ===
        self.multiplier_image_dimension = (200, 100)
        self.x2_image = image_loader(x2_image_path, self.multiplier_image_dimension)
        self.x3_image = image_loader(x3_image_path, self.multiplier_image_dimension)
        self.x4_image = image_loader(x4_image_path, self.multiplier_image_dimension)
        self.x5_image = image_loader(x5_image_path, self.multiplier_image_dimension)
        self.x6_image = image_loader(x6_image_path, self.multiplier_image_dimension)
        self.x7_image = image_loader(x7_image_path, self.multiplier_image_dimension)
        self.x8_image = image_loader(x8_image_path, self.multiplier_image_dimension)
        self.x9_image = image_loader(x9_image_path, self.multiplier_image_dimension)
        self.x10_image = image_loader(x10_image_path, self.multiplier_image_dimension)
        self.max_image = image_loader(max_image_path, self.multiplier_image_dimension)
        
        # === ITEM 2: AutoClick (1,0) ===
        self.autoclick_image_dimension = (120, 120)
        self.autoclick_image = image_loader(enhanced_cursor_image_path, self.autoclick_image_dimension)
        self.autoclick_name = "AutoClick"
        self.autoclick_price = 50
        
        # === ITEM 3: Gold Buff (2,0) ===
        self.gold_buff_image_dimension = (150, 150)
        self.gold_buff_image = image_loader(gold_buff_image_path, self.gold_buff_image_dimension)
        self.gold_buff_base_price = 10
        
        # === ITEM 4: Brick 17 Pro Max (0,1) ===
        self.brick17_image_dimension = (150, 150)
        self.brick17_image = image_loader(brick17_image_path, self.brick17_image_dimension)
        self.brick17_name = "Brick 17 Pro Max"
        self.brick17_price = 999
        
        # === ITEM 5: Boss Killer (1,1) ===
        self.boss_killer_unlock_level = 2
        self.boss_killer_image_dimension = (120, 120)
        self.boss_killer_image = image_loader(boss_killer_image_path, self.boss_killer_image_dimension)
        self.boss_killer_name = "Boss Killer"
        self.boss_killer_price = 100
        
        # === ITEM 6: Chain Master (2,1) ===
        self.chain_master_unlock_level = 4
        self.chain_master_image_dimension = (120, 120)
        self.chain_master_image = image_loader(chain_master_image_path, self.chain_master_image_dimension)
        self.chain_master_name = "Chain Master"
        self.chain_master_price = 150
        
        # Feedback + click-tracking
        self.feedback_text = None
        self.feedback_timer = 0
    
    def determine_multiplier_image(self, buffs):
        if BUFF.X10SCOREMULTIPLIER in buffs:
            return 'Maxed Out!!!', self.max_image, 11
        elif BUFF.X9SCOREMULTIPLIER in buffs:
            return 'X10 Multiplier', self.x10_image, 10
        elif BUFF.X8SCOREMULTIPLIER in buffs:
            return 'X9 Multiplier', self.x9_image, 9
        elif BUFF.X7SCOREMULTIPLIER in buffs:
            return 'X8 Multiplier', self.x8_image, 8
        elif BUFF.X6SCOREMULTIPLIER in buffs:
            return 'X7 Multiplier', self.x7_image, 7
        elif BUFF.X5SCOREMULTIPLIER in buffs:
            return 'X6 Multiplier', self.x6_image, 6
        elif BUFF.X4SCOREMULTIPLIER in buffs:
            return 'X5 Multiplier', self.x5_image, 5
        elif BUFF.X3SCOREMULTIPLIER in buffs:
            return 'X4 Multiplier', self.x4_image, 4
        elif BUFF.X2SCOREMULTIPLIER in buffs:
            return 'X3 Multiplier', self.x3_image, 3
        else:
            return 'X2 Multiplier', self.x2_image, 2
    
    def get_item_layout(self, row, col):
        """Get the center position for an item at grid position (row, col)"""
        button = self.all_buy_buttons[row][col]
        center_x = button.rect.centerx
        # Items positioned relative to original grid, not button position
        center_y = self.grid_start_y + row * self.spacing_y
        
        # Image position (above button)
        image_y = center_y - 220
        # Name position (below image)
        name_y = center_y - 120
        # Explanation position (below name)
        explanation_y = center_y - 70
        
        return center_x, image_y, name_y, explanation_y
    
    def blit_shop_items(self, screen, buffs, playerGold, cursor_Rect, max_level):
        # Display gold
        gold_text = self.gold_font.render(f"Gold: {playerGold}", True, yellow, white)
        screen.blit(gold_text, self.gold_position)
        
        # Draw all buy buttons first
        for row in range(self.num_button_y):
            for col in range(self.num_button_x):
                button = self.all_buy_buttons[row][col]
                button.if_hover(cursor_Rect)
                button.blit_button(screen)
        
        # === ITEM 1: Score Multiplier (0,0) ===
        multiplier_name, multiplier_image, multiplier_price = self.determine_multiplier_image(buffs)
        center_x, image_y, name_y, explanation_y = self.get_item_layout(0, 0)
        
        image_rect = multiplier_image.get_rect(center=(center_x, image_y))
        screen.blit(multiplier_image, image_rect)
        
        name_text = self.item_name_font.render(multiplier_name, True, yellow)
        name_rect = name_text.get_rect(center=(center_x, name_y))
        screen.blit(name_text, name_rect)
        
        if cursor_Rect.colliderect(image_rect.union(name_rect)):
            explanation_text = self.explanation_font.render("Increases point multiplier", True, black, white)
            explanation_rect = explanation_text.get_rect(center=(center_x, explanation_y))
            screen.blit(explanation_text, explanation_rect)
        
        if self.all_buy_buttons[0][0].if_hover(cursor_Rect):
            cost = multiplier_price ** 3 if multiplier_price != 11 else 0
            hover_text = self.explanation_font.render(f"Cost: {cost} gold", True, black, white)
            hover_rect = hover_text.get_rect(midleft=(self.all_buy_buttons[0][0].rect.right + 10, self.all_buy_buttons[0][0].rect.centery))
            screen.blit(hover_text, hover_rect)
        
        # === ITEM 2: AutoClick (1,0) ===
        center_x, image_y, name_y, explanation_y = self.get_item_layout(0, 1)
        
        image_rect = self.autoclick_image.get_rect(center=(center_x, image_y))
        screen.blit(self.autoclick_image, image_rect)
        
        name_text = self.item_name_font.render(self.autoclick_name, True, yellow)
        name_rect = name_text.get_rect(center=(center_x, name_y))
        screen.blit(name_text, name_rect)
        
        if cursor_Rect.colliderect(image_rect.union(name_rect)):
            explanation_text = self.explanation_font.render("Bigger cursor + autoclick", True, black, white)
            explanation_rect = explanation_text.get_rect(center=(center_x, explanation_y))
            screen.blit(explanation_text, explanation_rect)
        
        if self.all_buy_buttons[0][1].if_hover(cursor_Rect):
            hover_text = self.explanation_font.render(f"Cost: {self.autoclick_price} gold", True, black, white)
            hover_rect = hover_text.get_rect(midleft=(self.all_buy_buttons[0][1].rect.right + 10, self.all_buy_buttons[0][1].rect.centery))
            screen.blit(hover_text, hover_rect)
        
        # === ITEM 3: Gold Buff (2,0) ===
        num_gold_buffs = buffs.count(BUFF.GOLDBUFF)
        next_level = num_gold_buffs + 1
        center_x, image_y, name_y, explanation_y = self.get_item_layout(0, 2)
        
        image_rect = self.gold_buff_image.get_rect(center=(center_x, image_y))
        screen.blit(self.gold_buff_image, image_rect)
        
        name_text = self.item_name_font.render(f"Gold Buff x{next_level}", True, yellow)
        name_rect = name_text.get_rect(center=(center_x, name_y))
        screen.blit(name_text, name_rect)
        
        if cursor_Rect.colliderect(image_rect.union(name_rect)):
            explanation_text = self.explanation_font.render("+2 gold when game ends", True, black, white)
            explanation_rect = explanation_text.get_rect(center=(center_x, explanation_y))
            screen.blit(explanation_text, explanation_rect)
        
        if self.all_buy_buttons[0][2].if_hover(cursor_Rect):
            cost = self.gold_buff_base_price * (2 ** num_gold_buffs)
            hover_text = self.explanation_font.render(f"Cost: {cost} gold", True, black, white)
            hover_rect = hover_text.get_rect(midleft=(self.all_buy_buttons[0][2].rect.right + 10, self.all_buy_buttons[0][2].rect.centery))
            screen.blit(hover_text, hover_rect)
        
        # === ITEM 4: Brick 17 Pro Max (0,1) ===
        center_x, image_y, name_y, explanation_y = self.get_item_layout(1, 0)
        
        image_rect = self.brick17_image.get_rect(center=(center_x, image_y))
        screen.blit(self.brick17_image, image_rect)
        
        name_text = self.item_name_font.render(self.brick17_name, True, yellow)
        name_rect = name_text.get_rect(center=(center_x, name_y))
        screen.blit(name_text, name_rect)
        
        if cursor_Rect.colliderect(image_rect.union(name_rect)):
            explanation_text = self.explanation_font.render("Deletes whole board", True, black, white)
            explanation_rect = explanation_text.get_rect(center=(center_x, explanation_y))
            screen.blit(explanation_text, explanation_rect)
        
        if self.all_buy_buttons[1][0].if_hover(cursor_Rect):
            hover_text = self.explanation_font.render(f"Cost: {self.brick17_price} gold", True, black, white)
            hover_rect = hover_text.get_rect(midleft=(self.all_buy_buttons[1][0].rect.right + 10, self.all_buy_buttons[1][0].rect.centery))
            screen.blit(hover_text, hover_rect)
        
        # === ITEM 5: Boss Killer (1,1) ===
        if max_level >= self.boss_killer_unlock_level:
            center_x, image_y, name_y, explanation_y = self.get_item_layout(1, 1)
            
            image_rect = self.boss_killer_image.get_rect(center=(center_x, image_y))
            screen.blit(self.boss_killer_image, image_rect)
            
            name_text = self.item_name_font.render(self.boss_killer_name, True, yellow)
            name_rect = name_text.get_rect(center=(center_x, name_y))
            screen.blit(name_text, name_rect)
            
            if cursor_Rect.colliderect(image_rect.union(name_rect)):
                explanation_text = self.explanation_font.render("Reduces boss hits by 1", True, black, white)
                explanation_rect = explanation_text.get_rect(center=(center_x, explanation_y))
                screen.blit(explanation_text, explanation_rect)
            
            if self.all_buy_buttons[1][1].if_hover(cursor_Rect):
                hover_text = self.explanation_font.render(f"Cost: {self.boss_killer_price} gold", True, black, white)
                hover_rect = hover_text.get_rect(midleft=(self.all_buy_buttons[1][1].rect.right + 10, self.all_buy_buttons[1][1].rect.centery))
                screen.blit(hover_text, hover_rect)
        else:
            # Show locked message
            center_x, image_y, name_y, explanation_y = self.get_item_layout(1, 1)
            locked_text = self.item_name_font.render("Locked", True, (128, 128, 128))
            locked_rect = locked_text.get_rect(center=(center_x, name_y))
            screen.blit(locked_text, locked_rect)
            
            unlock_text = self.explanation_font.render(f"Unlock at Level {self.boss_killer_unlock_level}", True, (128, 128, 128))
            unlock_rect = unlock_text.get_rect(center=(center_x, explanation_y))
            screen.blit(unlock_text, unlock_rect)
        
        # === ITEM 6: Chain Master (2,1) ===
        if max_level >= self.chain_master_unlock_level:
            center_x, image_y, name_y, explanation_y = self.get_item_layout(1, 2)
            
            image_rect = self.chain_master_image.get_rect(center=(center_x, image_y))
            screen.blit(self.chain_master_image, image_rect)
            
            name_text = self.item_name_font.render(self.chain_master_name, True, yellow)
            name_rect = name_text.get_rect(center=(center_x, name_y))
            screen.blit(name_text, name_rect)
            
            if cursor_Rect.colliderect(image_rect.union(name_rect)):
                explanation_text = self.explanation_font.render("Doubles chaining chance", True, black, white)
                explanation_rect = explanation_text.get_rect(center=(center_x, explanation_y))
                screen.blit(explanation_text, explanation_rect)
            
            if self.all_buy_buttons[1][2].if_hover(cursor_Rect):
                hover_text = self.explanation_font.render(f"Cost: {self.chain_master_price} gold", True, black, white)
                hover_rect = hover_text.get_rect(midleft=(self.all_buy_buttons[1][2].rect.right + 10, self.all_buy_buttons[1][2].rect.centery))
                screen.blit(hover_text, hover_rect)
        else:
            # Show locked message
            center_x, image_y, name_y, explanation_y = self.get_item_layout(1, 2)
            locked_text = self.item_name_font.render("Locked", True, (128, 128, 128))
            locked_rect = locked_text.get_rect(center=(center_x, name_y))
            screen.blit(locked_text, locked_rect)
            
            unlock_text = self.explanation_font.render(f"Unlock at Level {self.chain_master_unlock_level}", True, (128, 128, 128))
            unlock_rect = unlock_text.get_rect(center=(center_x, explanation_y))
            screen.blit(unlock_text, unlock_rect)
        
        # === Draw feedback text ===
        if self.feedback_text:
            elapsed = pygame.time.get_ticks() - self.feedback_timer
            if elapsed < 2000:  # 2 seconds
                feedback_surface = self.explanation_font.render(self.feedback_text, True, red, white)
                feedback_rect = feedback_surface.get_rect(center=(screen.get_width() // 2, 100))
                screen.blit(feedback_surface, feedback_rect)
            else:
                self.feedback_text = None
    
    def if_clicked(self, events, buffs, playerGold, music, max_level):
        """Handles all click logic for shop items"""
        now = pygame.time.get_ticks()
        
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                pos = ev.pos
                playerGold, buffs = self._handle_purchase_at_pos(pos, buffs, playerGold, now, music, max_level)
        
        return playerGold, buffs
    
    def _handle_purchase_at_pos(self, pos, buffs, playerGold, now, music, max_level):
        """Handle purchase logic based on which button was clicked"""
        
        # Check which button was clicked
        clicked_row, clicked_col = None, None
        for row in range(self.num_button_y):
            for col in range(self.num_button_x):
                button = self.all_buy_buttons[row][col]
                if button.rect.collidepoint(pos):
                    clicked_row, clicked_col = row, col
                    break
            if clicked_row is not None:
                break
        
        if clicked_row is None:
            return playerGold, buffs
        
        # === Handle purchases based on position ===
        
        # (0,0) - Score Multiplier
        if clicked_row == 0 and clicked_col == 0:
            multiplier_name, _, multiplier_price = self.determine_multiplier_image(buffs)
            
            if multiplier_price == 11:
                self.feedback_text = "Multiplier is already maxed!"
                self.feedback_timer = now
                return playerGold, buffs
            
            cost = multiplier_price ** 3
            if playerGold < cost:
                self.feedback_text = f"Not enough gold! Need {cost}."
                self.feedback_timer = now
                return playerGold, buffs
            
            playerGold -= cost
            next_buff = getattr(BUFF, f"X{multiplier_price}SCOREMULTIPLIER")
            if next_buff not in buffs:
                buffs.append(next_buff)
            music.play_get_coin_sound()
            self.feedback_text = f"Purchased {multiplier_name}!"
            self.feedback_timer = now
        
        # (0,1) - AutoClick
        elif clicked_row == 0 and clicked_col == 1:
            if BUFF.AUTOCLICK in buffs:
                self.feedback_text = "AutoClick already purchased!"
                self.feedback_timer = now
                return playerGold, buffs
            
            if playerGold < self.autoclick_price:
                self.feedback_text = f"Not enough gold! Need {self.autoclick_price}."
                self.feedback_timer = now
                return playerGold, buffs
            
            playerGold -= self.autoclick_price
            buffs.append(BUFF.AUTOCLICK)
            music.play_get_coin_sound()
            self.feedback_text = "Purchased AutoClick!"
            self.feedback_timer = now
        
        # (0,2) - Gold Buff
        elif clicked_row == 0 and clicked_col == 2:
            num_gold_buffs = buffs.count(BUFF.GOLDBUFF)
            cost = self.gold_buff_base_price * (2 ** num_gold_buffs)
            
            if playerGold < cost:
                self.feedback_text = f"Not enough gold! Need {cost}."
                self.feedback_timer = now
                return playerGold, buffs
            
            playerGold -= cost
            buffs.append(BUFF.GOLDBUFF)
            music.play_get_coin_sound()
            next_level = num_gold_buffs + 1
            self.feedback_text = f"Purchased Gold Buff x{next_level}!"
            self.feedback_timer = now
        
        # (1,0) - Brick 17 Pro Max
        elif clicked_row == 1 and clicked_col == 0:
            if BUFF.BRICK17 in buffs:
                self.feedback_text = "Brick 17 Pro Max already purchased!"
                self.feedback_timer = now
                return playerGold, buffs
            
            if playerGold < self.brick17_price:
                self.feedback_text = f"Not enough gold! Need {self.brick17_price}."
                self.feedback_timer = now
                return playerGold, buffs
            
            playerGold -= self.brick17_price
            buffs.append(BUFF.BRICK17)
            music.play_get_coin_sound()
            self.feedback_text = "Purchased Brick 17 Pro Max!"
            self.feedback_timer = now
        
        # (1,1) - Boss Killer
        elif clicked_row == 1 and clicked_col == 1:
            if max_level < self.boss_killer_unlock_level:
                self.feedback_text = f"Unlock at Level {self.boss_killer_unlock_level}!"
                self.feedback_timer = now
                return playerGold, buffs
            
            if BUFF.BOSS_KILLER in buffs:
                self.feedback_text = "Boss Killer already purchased!"
                self.feedback_timer = now
                return playerGold, buffs
            
            if playerGold < self.boss_killer_price:
                self.feedback_text = f"Not enough gold! Need {self.boss_killer_price}."
                self.feedback_timer = now
                return playerGold, buffs
            
            playerGold -= self.boss_killer_price
            buffs.append(BUFF.BOSS_KILLER)
            music.play_get_coin_sound()
            self.feedback_text = "Purchased Boss Killer!"
            self.feedback_timer = now
        
        # (1,2) - Chain Master
        elif clicked_row == 1 and clicked_col == 2:
            if max_level < self.chain_master_unlock_level:
                self.feedback_text = f"Unlock at Level {self.chain_master_unlock_level}!"
                self.feedback_timer = now
                return playerGold, buffs
            
            if BUFF.CHAIN_MASTER in buffs:
                self.feedback_text = "Chain Master already purchased!"
                self.feedback_timer = now
                return playerGold, buffs
            
            if playerGold < self.chain_master_price:
                self.feedback_text = f"Not enough gold! Need {self.chain_master_price}."
                self.feedback_timer = now
                return playerGold, buffs
            
            playerGold -= self.chain_master_price
            buffs.append(BUFF.CHAIN_MASTER)
            music.play_get_coin_sound()
            self.feedback_text = "Purchased Chain Master!"
            self.feedback_timer = now
        
        return playerGold, buffs