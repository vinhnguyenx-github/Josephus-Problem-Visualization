import math, pygame
from config import *
from button import Button

class JosephusVis:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(FONT_NAME, 28, bold=True)
        self.small = pygame.font.SysFont(FONT_NAME, 20)
        self.big = pygame.font.SysFont(FONT_NAME, 40, bold=True)
        self.center = (WIDTH // 2, HEIGHT // 2 + 40)

        self.auto = False
        self.step_delay_ms = 350
        self.last_step_time = 0
        self.n = 15

        self.reset()
        self._create_buttons()

    # ----------------------------- 
    # LOGIC 
    # -----------------------------
    def reset(self):
        self.people = list(range(1, self.n + 1))
        self.eliminated = set()
        self.current_index = 0
        self.count_accum = 0
        self.winner = None
        self.auto = False

    def current_k(self):
        return K_PRIMARY if len(self.people) >= 3 else K_FALLBACK

    def set_n(self, new_n):
        new_n = max(1, min(60, new_n))
        if new_n != self.n:
            self.n = new_n
            self.reset()

    def do_step(self):
        if self.winner is not None or len(self.people) <= 1:
            if len(self.people) == 1:
                self.winner = self.people[0]
            return

        k = self.current_k()
        self.count_accum = (self.count_accum + 1)
        if self.count_accum == k:
            elim_idx = self.current_index
            elim_person = self.people.pop(elim_idx)
            self.eliminated.add(elim_person)
            self.count_accum = 0
            if self.people:
                self.current_index = elim_idx % len(self.people)
        else:
            self.current_index = (self.current_index + 1) % len(self.people)

        if len(self.people) == 1:
            self.winner = self.people[0]

    def maybe_auto_step(self):
        if not self.auto or self.winner is not None:
            return
        now = pygame.time.get_ticks()
        if now - self.last_step_time >= self.step_delay_ms:
            self.last_step_time = now
            self.do_step()

    # ----------------
    # BUTTONS 
    # ----------------
    def _create_buttons(self):
        x0 = WIDTH - BUTTON_W - BUTTON_PAD
        y = 22
        self.buttons = [
            Button(x0, y, BUTTON_W, BUTTON_H, "AUTO: SPACE", "auto"),
            Button(x0, y + (BUTTON_H + BUTTON_PAD), BUTTON_W, BUTTON_H, "STEP: N", "step"),
            Button(x0, y + 2 * (BUTTON_H + BUTTON_PAD), BUTTON_W, BUTTON_H, "RESET: R", "reset"),
            Button(x0, y + 3 * (BUTTON_H + BUTTON_PAD), BUTTON_W // 2 - 6, BUTTON_H, "N -", "n-"),
            Button(x0 + BUTTON_W // 2 + 6, y + 3 * (BUTTON_H + BUTTON_PAD), BUTTON_W // 2 - 6, BUTTON_H, "N +", "n+"),
        ]

    def on_click(self, event):
        callback_map = {
            "auto": lambda: setattr(self, "auto", not self.auto),
            "step": self.do_step,
            "reset": self.reset,
            "n-": lambda: self.set_n(self.n - 1),
            "n+": lambda: self.set_n(self.n + 1),
        }
        for btn in self.buttons:
            if btn.handle_event(event, callback_map):
                return True
        return False

    # ----------------------------- 
    # VISUALS 
    # -----------------------------
    def positions(self):
        pts = {}
        total = max(self.n, 1)
        for i in range(1, total + 1):
            theta = 2 * math.pi * (i - 1) / total - math.pi / 2
            x = self.center[0] + int(RING_RADIUS * math.cos(theta))
            y = self.center[1] + int(RING_RADIUS * math.sin(theta))
            pts[i] = (x, y)
        return pts

    def draw(self):
        self.screen.fill(BACKGROUND)
        title = self.big.render("JOSEPHUS VISUALIZER", True, NEON)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 40)))

        rule = self.small.render(
            f"Rule: eliminate every {K_PRIMARY}, fallback to {K_FALLBACK} when fewer than 3",
            True, NEON
        )
        self.screen.blit(rule, rule.get_rect(center=(WIDTH // 2, 80)))

        pygame.draw.circle(self.screen, NEON_DIM, self.center, RING_RADIUS, 1)

        pos = self.positions()
        for pid, (x, y) in pos.items():
            if pid in self.eliminated:
                color = ELIMINATED
            elif pid in self.people:
                color = NEON_DIM
            else:
                color = NEON_DIM
            pygame.draw.circle(self.screen, color, (x, y), PERSON_RADIUS)

        if self.winner:
            pygame.draw.circle(self.screen, WINNER, pos[self.winner], PERSON_RADIUS + 4, 3)
        elif self.people:
            current_person = self.people[self.current_index]
            pygame.draw.circle(self.screen, CURRENT, pos[current_person], PERSON_RADIUS + 4, 2)

        for pid, (x, y) in pos.items():
            label = self.small.render(str(pid), True, TEXT)
            self.screen.blit(label, label.get_rect(center=(x, y)))

        info = f"N={self.n}  alive={len(self.people)}  eliminated={len(self.eliminated)}  k={self.current_k()}"
        info_s = self.small.render(info, True, TEXT)
        self.screen.blit(info_s, (20, HEIGHT - 40))

        for btn in self.buttons:
            btn.draw(self.screen)