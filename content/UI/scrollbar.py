import pygame

# Initialize Pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode((640, 480))

# Create a surface for the scrollbar
scrollbar_surface = pygame.Surface((20, 480))

# Create a rect for the scrollbar
scrollbar_rect = pygame.Rect(620, 0, 20, 480)

# Create a rect for the scrollbar thumb
thumb_rect = pygame.Rect(620, 0, 20, 40)

# Main game loop
running = True
dragging = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked on the scrollbar thumb
            if thumb_rect.collidepoint(event.pos):
                # The user has clicked on the thumb, start dragging it
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # The user has released the mouse button, stop dragging
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            # Update the thumb rect if we are dragging it
            if dragging:
                thumb_rect.y = event.pos[1]

    # Keep the thumb rect within the bounds of the scrollbar
    thumb_rect.y = max(0, min(thumb_rect.y, 480 - thumb_rect.height))

    # Draw the scrollbar
    screen.fill((170, 170, 170))
    scrollbar_surface.fill((255, 255, 255))

    # Blit the scrollbar to the screen
    screen.blit(scrollbar_surface, scrollbar_rect)
    pygame.draw.rect(screen, (0, 0, 0), thumb_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()