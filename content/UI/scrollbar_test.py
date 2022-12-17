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

# Fill the screen with a solid color for the background
screen.fill((255, 255, 255))

# Create a list of UI components
components = [
    pygame.Rect(100, 100, 100, 100),
    pygame.Rect(200, 200, 100, 100),
    pygame.Rect(300, 300, 100, 100),
    pygame.Rect(400, 400, 100, 100),
    pygame.Rect(500, 500, 100, 100),
]

# Main game loop
running = True
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

    # Calculate the scrolling amount based on the position of the thumb rect
    scroll_amount = thumb_rect.y * (len(components) - 5) / (480 - thumb_rect.height)

    # Update the positions of the UI components based on the scroll amount
    for component in components:
        component.y -= scroll_amount

    # Draw the scrollbar
    scrollbar_surface.fill((255, 255, 255))
    pygame.draw.rect(scrollbar_surface, (0, 0, 0), thumb_rect)

    # Blit the scrollbar to the screen
    screen.blit(scrollbar_surface, scrollbar_rect)

    # Draw the UI components
    for component in components:
        pygame.draw.rect(screen, (0, 0, 0), component)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
