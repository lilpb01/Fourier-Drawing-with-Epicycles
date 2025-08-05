import pygame
import math
import cmath

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Draw Shape and Animate Fourier Epicycles")
clock = pygame.time.Clock()

drawing = True
path = []
scale = 1
t = 0
fourier = []
trail = []

while drawing:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            break

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        path.append(complex(mx - width//2, my - height//2))

    for i in range(1, len(path)):
        pygame.draw.line(screen, (255, 255, 255),
                         (path[i-1].real + width//2, path[i-1].imag + height//2),
                         (path[i].real + width//2, path[i].imag + height//2), 2)

    pygame.display.flip()
    clock.tick(120)

def dft(signal):
    N = len(signal)
    X = []
    for k in range(N):
        total = 0
        for n in range(N):
            angle = 2 * math.pi * k * n / N
            total += signal[n] * cmath.exp(-1j * angle)
        total /= N
        freq = k
        amp = abs(total)
        phase = cmath.phase(total)
        X.append((freq, amp, phase, total))
    return sorted(X, key=lambda x: x[1], reverse=True)

fourier = dft(path)
N = len(fourier)

running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    x = width // 2
    y = height // 2

    for freq, amp, phase, coef in fourier[:200]:  # Use top 200 terms
        prev_x, prev_y = x, y
        angle = 2 * math.pi * freq * t / N + phase
        x += amp * math.cos(angle)
        y += amp * math.sin(angle)

        pygame.draw.circle(screen, (80, 80, 80), (int(prev_x), int(prev_y)), int(amp), 1)
        pygame.draw.line(screen, (255, 255, 255), (int(prev_x), int(prev_y)), (int(x), int(y)), 1)

    trail.insert(0, (x, y))
    if len(trail) > N:
        trail.pop()
    for i in range(1, len(trail)):
        pygame.draw.line(screen, (0, 255, 0), trail[i-1], trail[i], 2)

    t += 1
    if t >= N:
        t = 0
        trail = []

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
