import rumps, pyperclip, time

MAX_HISTORY = 100

class ClipboardManager(rumps.App):
    def __init__(self):
        super().__init__("📋")
        self.history = []
        self.last_text = ""
        self.update_menu()
        self.timer = rumps.Timer(self.check_clipboard, 0.5)
        self.timer.start()

    def check_clipboard(self, _):
        try:
            current = pyperclip.paste()
        except Exception:
            return

        if (
            current
            and current.strip()
            and current != self.last_text
        ):
            self.last_text = current
            self.add_to_history(current)

    def add_to_history(self, text):
        if text in self.history:
            self.history.remove(text)

        self.history.insert(0, text)
        self.history = self.history[:MAX_HISTORY]
        self.update_menu()

    def update_menu(self):
        self.menu.clear()

        if not self.history:
            self.menu.add(rumps.MenuItem("No history"))
        else:
            for item in self.history[:10]:
                shortened = item.replace("\n", " ")[:50]
                menu_item = rumps.MenuItem(shortened)
                menu_item.full_text = item
                menu_item.set_callback(self.copy_item)
                self.menu.add(menu_item)

        self.menu.add(None)
        self.menu.add(rumps.MenuItem("Clear History", callback=self.clear_history))
        self.menu.add(None)
        self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))

    def copy_item(self, sender):
        pyperclip.copy(sender.full_text)

    def clear_history(self, _):
        self.history = []
        self.update_menu()

if __name__ == "__main__":
    ClipboardManager().run()

