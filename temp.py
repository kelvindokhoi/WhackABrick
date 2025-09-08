# ... existing code ...

# create text and info for our quit button
quitButtonImage = pygame.transform.scale(pygame.image.load(resource_path(quit_button_image_path)).convert_alpha(),(73,32))
quitButtonRect = quitButtonImage.get_rect()
quitButtonx = 150  # Shifted left
quitButtony = 600
quitButtonwidth = quitButtonRect.width
quitButtonheight = quitButtonRect.height
quitButtonRect.topleft = (quitButtonx,quitButtony)
screen.blit(quitButtonImage, quitButtonRect)

# create text and info for our shop button
shopButtonText = buttonfont.render(" Shop ", True, black, pink)
shopButtonRect = shopButtonText.get_rect()
shopButtonx = 300  # New position
shopButtony = 600
shopButtonwidth = shopButtonRect.width
shopButtonheight = shopButtonRect.height
shopButtonRect.topleft = (shopButtonx,shopButtony)
pygame.draw.rect(screen,white,shopButtonRect)
screen.blit(shopButtonText, shopButtonRect)

# create text and info for our start button
startButtonText = buttonfont.render(" Start ", True, black, pink)
startButtonRect = startButtonText.get_rect()
startButtonx = 450  # Shifted right
startButtony = 600
startButtonwidth = startButtonRect.width
startButtonheight = startButtonRect.height
startButtonRect.topleft = (startButtonx,startButtony)
pygame.draw.rect(screen,white,startButtonRect)
screen.blit(startButtonText, startButtonRect)

# ... existing code ...

while True:
    # ... existing event handling ...

    if event.type == pygame.MOUSEBUTTONDOWN:
        # was the quit rectangle clicked?
        if mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
            mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
            pygame.quit()
            sys.exit()
        
        if gameState==GameState.MAIN_MENU and mousex >= startButtonx and mousex <= startButtonx + startButtonwidth and \
            mousey >= startButtony and mousey <= startButtony + startButtonheight:
            gameState = GameState.GAME_START
            playerPoints = 0
            pygame.mouse.set_visible(False)
            cursor_image = transform.scale(pygame.image.load("cursor.png"),(30,30))
            cursor_rect = cursor_image.get_rect()
        
        # Add shop button click
        if gameState==GameState.MAIN_MENU and mousex >= shopButtonx and mousex <= shopButtonx + shopButtonwidth and \
            mousey >= shopButtony and mousey <= shopButtony + shopButtonheight:
            gameState = GameState.SHOP
        
        # ... existing code ...

    # ... existing code ...

    if gameState == GameState.SHOP:
        # Placeholder for shop: display text and back button
        shopText = headerfont.render("Shop Coming Soon!", True, black, pink)
        shopRect = shopText.get_rect()
        shopRect.center = (350, 300)
        screen.blit(shopText, shopRect)
        
        backButtonText = buttonfont.render(" Back ", True, black, pink)
        backButtonRect = backButtonText.get_rect()
        backButtonRect.center = (350, 500)
        pygame.draw.rect(screen, white, backButtonRect)
        screen.blit(backButtonText, backButtonRect)
        
        # Handle back button click (add in event loop if needed, but for simplicity, assume it's handled separately)
        # Note: For full functionality, add mouse click detection for back button to set gameState back to MAIN_MENU
    
    else:
        # ... existing main menu drawing ...
        # Update button positions in drawing
        if mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
                mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
            quitButtonText = buttonfont.render(" Quit ", True, red, pink)
        else:
            quitButtonText = buttonfont.render(" Quit ", True, black, pink)
        
        if mousex >= shopButtonx and mousex <= shopButtonx + shopButtonwidth and \
                mousey >= shopButtony and mousey <= shopButtony + shopButtonheight:
            shopButtonText = buttonfont.render(" Shop ", True, red, pink)
        else:
            shopButtonText = buttonfont.render(" Shop ", True, black, pink)
        
        if mousex >= startButtonx and mousex <= startButtonx + startButtonwidth and \
                mousey >= startButtony and mousey <= startButtony + startButtonheight:
            startButtonText = buttonfont.render(" Start ", True, red, pink)
        else:
            startButtonText = buttonfont.render(" Start ", True, black, pink)
        
        screen.blit(quitButtonText, quitButtonRect)
        screen.blit(shopButtonText, shopButtonRect)
        screen.blit(startButtonText, startButtonRect)

    # ... existing code ...
