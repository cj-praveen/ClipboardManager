import rumps, pyperclip

MAX_HISTORY = 100

class ClipboardManager(rumps.App):
    def __init__(self) -> None:
        super().__init__("📋")
        self.history: list[str] = []
        self.last_text: str = ""
        self.update_menu()
        self.timer = rumps.Timer(self.check_clipboard, 0.3)
        self.timer.start()

    def check_clipboard(self, _) -> None:
        try:
            current: str = pyperclip.paste()
        except Exception:
            return

        if (
            current
            and current.strip()
            and current != self.last_text
        ):
            self.last_text = current
            self.add_to_history(current)

    def add_to_history(self, text: str) -> None:
        if text in self.history:
            self.history.remove(text)

        self.history.insert(0, text)
        self.history = self.history[:MAX_HISTORY]
        self.update_menu()

    def update_menu(self) -> None:
        self.menu.clear()

        if not self.history:
            self.menu.add(rumps.MenuItem("No history"))
        else:
            for item in self.history:
                text: str = f"{item.replace('\n', ' ')[:50]}..." if len(item) > 50 else item
                menu_item = rumps.MenuItem(text, callback=self.copy_item)
                menu_item.full_text = item
                menu_item.set_callback(self.copy_item)
                self.menu.add(menu_item)

        self.menu.add(None)
        self.menu.add(rumps.MenuItem("Clear History", callback=self.clear_history))
        self.menu.add(None)
        self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))

    def copy_item(self, item) -> None:
        try:
            pyperclip.copy(item.full_text)
        except Exception:
            return

    def clear_history(self, _) -> None:
        self.history = []
        self.update_menu()

if __name__ == "__main__":
    ClipboardManager().run()
