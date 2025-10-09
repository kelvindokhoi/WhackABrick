import pygame
from functions.Resource_Reader import image_loader
from functions.FilePaths import settings_image_path,settings_background_image_path
from functions.Colors import white, black, blue, lightblue, darkblue
import tkinter.messagebox as messagebox

class SettingsObject:
    def __init__(self, desktop_width, desktop_height):
        self.desktop_width = desktop_width
        self.desktop_height = desktop_height
        
        # Settings panel dimensions
        self.panel_width = 1400
        self.panel_height = 750
        self.panel_x = (desktop_width - self.panel_width) // 2
        self.panel_y = (desktop_height - self.panel_height) // 2
        
        # Load settings icon/gear for decoration
        self.settings_icon = image_loader(settings_image_path, (150, 150), alpha=True)
        self.settings_background = image_loader(settings_background_image_path,(self.desktop_width,self.desktop_height),alpha=True)
        
        # Slider dimensions
        self.slider_width = 700
        self.slider_height = 80
        self.slider_knob_radius = 40
        
        # Music slider position
        self.music_slider_x = self.panel_x + 640
        self.music_slider_y = self.panel_y + 265
        
        # Sound effect slider position
        self.sfx_slider_x = self.panel_x + 640
        self.sfx_slider_y = self.panel_y + 495
        
        # Slider values (0.0 to 1.0)
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        
        # Track which slider is being dragged
        self.dragging_music = False
        self.dragging_sfx = False
        
        # Back button (using the panel area as a simple close mechanism)
        self.close_button_rect = pygame.Rect(
            self.panel_x + self.panel_width - 100,
            self.panel_y + 20,
            80,
            80
        )
        
        # Reset button
        self.reset_button_rect = pygame.Rect(
            self.panel_x + (self.panel_width - 200) // 2,
            self.panel_y + 600,
            200,
            50
        )
        self.reset_font = pygame.font.SysFont('Corbel', 24)
    
    def handle_event(self, singular_event, cursor_rect, music_obj, player_gold, buffs):
        """Handle mouse events for the settings UI"""
        if singular_event.type == pygame.MOUSEBUTTONDOWN:
            
            # Check if clicking on music slider
            music_knob_x = self.music_slider_x + self.music_volume * self.slider_width
            music_knob_rect = pygame.Rect(
                music_knob_x,
                self.music_slider_y,
                self.slider_knob_radius * 2,
                self.slider_knob_radius * 2
            )
            
            if music_knob_rect.colliderect(cursor_rect):
                self.dragging_music = True
                return False, None
            
            # Check if clicking on SFX slider
            sfx_knob_x = self.sfx_slider_x + self.sfx_volume * self.slider_width
            sfx_knob_rect = pygame.Rect(
                sfx_knob_x,
                self.sfx_slider_y,
                self.slider_knob_radius * 2,
                self.slider_knob_radius * 2
            )
            
            if sfx_knob_rect.colliderect(cursor_rect):
                self.dragging_sfx = True
                return False, None
            
            # Check if clicking close button
            if self.close_button_rect.colliderect(cursor_rect):
                return True, None  # Signal to close settings
            
            # Check if clicking reset button
            if self.reset_button_rect.colliderect(cursor_rect):
                if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset buffs and gold? This action cannot be undone."):
                    buffs.clear()
                    return True, 0  # Close and reset gold to 0
                else:
                    return False, None  # Do not close
        
        elif singular_event.type == pygame.MOUSEBUTTONUP:
            self.dragging_music = False
            self.dragging_sfx = False
            return False, None
        
        elif singular_event.type == pygame.MOUSEMOTION:
            
            # Update music volume if dragging
            if self.dragging_music:
                relative_x = cursor_rect[0] - self.music_slider_x
                self.music_volume = max(0.0, min(1.0, relative_x / self.slider_width))
                pygame.mixer.music.set_volume(self.music_volume)
            
            # Update SFX volume if dragging
            if self.dragging_sfx:
                relative_x = cursor_rect[0] - self.sfx_slider_x
                self.sfx_volume = max(0.0, min(1.0, relative_x / self.slider_width))
                # Update sound effect volumes
                if hasattr(music_obj, 'braxton_sound'):
                    music_obj.braxton_sound.set_volume(self.sfx_volume)
                if hasattr(music_obj, 'brick_hit_sound'):
                    music_obj.brick_hit_sound.set_volume(self.sfx_volume)
        
        return False, None
    
    def draw_slider(self, screen, x, y, value):
        """Draw a slider bar with knob"""
        # Slider track (background)
        track_rect = pygame.Rect(x, y, self.slider_width, self.slider_height)
        pygame.draw.rect(screen, white, track_rect, border_radius=20)
        pygame.draw.rect(screen, darkblue, track_rect, 3, border_radius=20)
        
        # Filled portion
        filled_width = value * self.slider_width
        if filled_width > 0:
            filled_rect = pygame.Rect(x, y, filled_width, self.slider_height)
            pygame.draw.rect(screen, lightblue, filled_rect, border_radius=20)
        
        # Slider knob
        knob_x = x + value * self.slider_width
        knob_y = y + self.slider_height // 2
        pygame.draw.circle(screen, white, (int(knob_x), int(knob_y)), self.slider_knob_radius)
        pygame.draw.circle(screen, darkblue, (int(knob_x), int(knob_y)), self.slider_knob_radius, 4)
        pygame.draw.circle(screen, lightblue, (int(knob_x), int(knob_y)), self.slider_knob_radius - 8)
    
    def draw(self, screen):
        """Draw the settings UI"""
        # Draw semi-transparent overlay
        screen.blit(self.settings_background,(0,0))
        
        # Draw music slider
        self.draw_slider(screen, self.music_slider_x, self.music_slider_y, self.music_volume)
        
        # Draw SFX slider
        self.draw_slider(screen, self.sfx_slider_x, self.sfx_slider_y, self.sfx_volume)
        
        # Draw close button (X)
        pygame.draw.circle(screen, (200, 50, 50), self.close_button_rect.center, 40)
        pygame.draw.circle(screen, white, self.close_button_rect.center, 40, 4)
        
        # Draw X
        x_font = pygame.font.SysFont('Corbel', 60, bold=True)
        x_text = x_font.render("X", True, white)
        x_rect = x_text.get_rect(center=self.close_button_rect.center)
        screen.blit(x_text, x_rect)
        
        # Draw reset button
        pygame.draw.rect(screen, (200, 50, 50), self.reset_button_rect, border_radius=10)
        pygame.draw.rect(screen, white, self.reset_button_rect, 3, border_radius=10)
        reset_text = self.reset_font.render("Reset Progress", True, white)
        reset_text_rect = reset_text.get_rect(center=self.reset_button_rect.center)
        screen.blit(reset_text, reset_text_rect)