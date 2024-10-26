from playwright.sync_api import sync_playwright
import time

def init_playwright():
    """Initialize Playwright with required settings"""
    return sync_playwright().start()

def close_playwright(playwright):
    """Properly close Playwright instance"""
    playwright.stop()