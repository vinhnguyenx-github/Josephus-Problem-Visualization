import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from josephus import JosephusVis

import pygame
pygame.init()
pygame.font.init()


class DummyScreen:
    """Minimal mock screen to bypass Pygame rendering for logic testing."""
    def __init__(self):
        self.actions = []
    def fill(self, color): pass
    def blit(self, *args, **kwargs): pass


# -----------------------------
# JosephusVis Logic Tests
# -----------------------------
def test_reset_initialization():
    vis = JosephusVis(DummyScreen())
    vis.n = 12
    vis.reset()
    assert len(vis.people) == 12
    assert vis.auto is False
    assert isinstance(vis.eliminated, set)


def test_do_step_elimination_progress():
    vis = JosephusVis(DummyScreen())
    vis.n = 6
    vis.reset()
    initial_count = len(vis.people)
    for _ in range(3):
        vis.do_step()
    assert len(vis.people) <= initial_count


def test_set_n_changes_size():
    vis = JosephusVis(DummyScreen())
    vis.set_n(15)
    assert vis.n == 15
    assert len(vis.people) == 15


def test_elimination_until_last():
    vis = JosephusVis(DummyScreen())
    vis.n = 5
    vis.reset()
    for _ in range(100):  # simulate many rounds
        vis.do_step()
        if len(vis.people) == 1:
            break
    assert len(vis.people) == 1
    assert len(vis.eliminated) == vis.n - 1


def test_current_k_switch():
    vis = JosephusVis(DummyScreen())
    vis.n = 5
    vis.reset()
    assert vis.current_k() == 3  # primary rule
    vis.people = [1, 2]
    assert vis.current_k() == 2  # fallback rule


def test_auto_toggle_and_step():
    vis = JosephusVis(DummyScreen())
    vis.auto = False
    vis.auto = not vis.auto
    assert vis.auto is True
    vis.do_step()
    assert isinstance(vis.people, list)


def test_positions_layout():
    vis = JosephusVis(DummyScreen())
    vis.n = 8
    pos = vis.positions()
    assert isinstance(pos, dict)
    assert len(pos) == 8
    for node, (x, y) in pos.items():
        assert isinstance(x, int)
        assert isinstance(y, int)


def test_reset_reinitializes_state():
    vis = JosephusVis(DummyScreen())
    vis.n = 10
    vis.reset()
    vis.do_step()
    vis.reset()
    assert len(vis.people) == 10
    assert len(vis.eliminated) == 0
    assert vis.current_index == 0