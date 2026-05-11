from infrastructure.army import Army, ArmiesDict
from infrastructure.warscroll import Warscrolls
import ui.screen as s
from ui.screen import ScreenName as sn
from config import ARMY_PATH, WARSCROLL_PATH

class AppState:
    def __init__(self, army_path: str, warscroll_path: str):
        self.current_army: Army | None = None
        self.armies_dict: ArmiesDict | None = None
        self.warscrolls: Warscrolls | None = None
        self.army_dirty: bool = False
        self.warscrolls_dirty: bool = False
        self.army_path: str = army_path
        self.warscroll_path: str = warscroll_path

        @property
        def has_unsaved_changes(self) -> bool:
            return self.army_dirty or self.warscrolls_dirty

        def save(self):
            if self.current_army:  # and self.army_dirty
                self.current_army.save_army(self.army_path)
            if self.warscrolls:  # and self.warscrolls_dirty
                self.warscrolls.save_warscrolls(self.warscroll_path)


def registry(army_path: str) -> dict[s.ScreenName, s.Screen]:
    screen_registry: dict[s.ScreenName, s.Screen] = {
        sn.MAIN_MENU: s.MainMenuScreen(),
        sn.MANAGE_ARMIES: s.ManageArmiesScreen(),
        sn.LOAD_ARMY: s.LoadArmiesMenu(army_path),
    }
    return screen_registry

class App:
    def __init__(self, first_screen: s.ScreenName, state: AppState):
        self.stack: list[s.ScreenName] = [first_screen]
        self.state: AppState = state

    def run(self):
        screen_registry = registry(self.state.army_path)
        while self.stack:
            screen_name = self.stack.pop()
            if screen_name == sn.EXIT:
                break
            current_screen = screen_registry[screen_name]
            next_screen = current_screen.show()
            self.stack.append(next_screen)


if __name__ == "__main__":
    state = AppState(ARMY_PATH, WARSCROLL_PATH)
    app = App(sn.MAIN_MENU, state)
    app.run()
