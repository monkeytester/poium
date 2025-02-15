import os
import time
import warnings
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoAlertPresentException
from appium.webdriver.common.touch_action import TouchAction as MobileTouchAction

from poium.selenium import BasePage
from poium.common.keyboard import KeyEvent


class Page(BasePage):
    """
    Implement the APIs with javascript,
    and selenium/appium extension APIs。
    """

    def execute_script(self, js=None, *args):
        """
        Execute JavaScript scripts.
        """
        if js is None:
            raise ValueError("Please input js script")
        
        return self.driver.execute_script(js, *args)

    def window_scroll(self, width=None, height=None):
        """
        JavaScript API, Only support css positioning
        Setting width and height of window scroll bar.
        """
        if width is None:
            width = "0"
        if height is None:
            height = "0"
        js = f"window.scrollTo({width},{height});"
        self.execute_script(js)

    @property
    def get_title(self):
        """
        JavaScript API
        Get page title.
        """
        js = 'return document.title;'
        return self.execute_script(js)

    @property
    def get_url(self):
        """
        JavaScript API
        Get page URL.
        """
        js = "return document.URL;"
        return self.execute_script(js)

    def set_window_size(self, width=None, height=None):
        """
        selenium API
        Sets the width and height of the current window.

        :Args:
         - width: the width in pixels to set the window to
         - height: the height in pixels to set the window to

        :Usage:
            driver.set_window_size(800,600)
        """
        if width is None and height is None:
            self.driver.maximize_window()
        else:
            self.driver.set_window_size(self, width, height)

    def switch_to_frame(self, frame_reference):
        """
        selenium API
        Switches focus to the specified frame, by id, name, or webelement.
        """
        warnings.warn("use page.elem.switch_to_frame() instead",
                      DeprecationWarning, stacklevel=2)
        self.driver.switch_to.frame(frame_reference)

    def switch_to_parent_frame(self):
        """
        selenium API
        Switches focus to the parent context.
        Corresponding relationship with switch_to_frame () method.
        """
        self.driver.switch_to.parent_frame()

    @property
    def new_window_handle(self):
        """
        selenium API
        Getting a handle to a new window.
        """
        warnings.warn("This method is on the verge of obsolescence",
                      DeprecationWarning, stacklevel=2)
        all_handle = self.driver.window_handles
        return all_handle[-1]

    @property
    def current_window_handle(self):
        """
        selenium API
        Returns the handle of the current window.
        """
        warnings.warn("This method is on the verge of obsolescence",
                      DeprecationWarning, stacklevel=2)
        return self.driver.current_window_handle

    @property
    def window_handles(self):
        """
        selenium API
        Returns the handles of all windows within the current session.
        """
        warnings.warn("This method is on the verge of obsolescence",
                      DeprecationWarning, stacklevel=2)
        return self.driver.window_handles

    def switch_to_window(self, index: int) -> None:
        """
        selenium API
        Switches focus to the specified window.

        :Args:
         - window: window index. 1 represents a newly opened window (0 is the first one)

        :Usage:
            self.switch_to_window(1)
        """
        all_handles = self.driver.window_handles
        self.driver.switch_to.window(all_handles[index])

    def screenshots(self, path=None, filename=None):
        """
        selenium API
        Saves a screenshots of the current window to a PNG image file
        :param path: The path to save the file
        :param filename: The file name
        """
        if path is None:
            path = os.getcwd()
        if filename is None:
            filename = str(time.time()).split(".")[0] + ".png"
        file_path = os.path.join(path, filename)
        self.driver.save_screenshot(file_path)

    def get_cookies(self):
        """
        Returns a set of dictionaries, corresponding to cookies visible in the current session.
        """
        return self.driver.get_cookies()

    def get_cookie(self, name):
        """
        Returns information of cookie with ``name`` as an object.
        """
        return self.driver.get_cookie(name)

    def add_cookie(self, cookie_dict):
        """
        Adds a cookie to your current session.
        Usage:
            add_cookie({'name' : 'foo', 'value' : 'bar'})
        """
        if isinstance(cookie_dict, dict):
            self.driver.add_cookie(cookie_dict)
        else:
            raise TypeError("Wrong cookie type.")

    def add_cookies(self, cookie_list):
        """
        Adds a cookie to your current session.
        Usage:
            cookie_list = [
                {'name' : 'foo', 'value' : 'bar'},
                {'name' : 'foo', 'value' : 'bar'}
            ]
            add_cookie(cookie_list)
        """
        if isinstance(cookie_list, list):
            for cookie in cookie_list:
                self.add_cookie(cookie)
        else:
            raise TypeError("Wrong cookie type.")

    def delete_cookie(self, name):
        """
        Deletes a single cookie with the given name.
        """
        self.driver.delete_cookie(name)

    def delete_all_cookies(self):
        """
        Delete all cookies in the scope of the session.
        Usage:
            self.delete_all_cookies()
        """
        self.driver.delete_all_cookies()

    def switch_to_app(self):
        """
        appium API
        Switch to native app.
        """
        current_context = self.driver.current_context
        if current_context != "NATIVE_APP":
            self.driver.switch_to.context('NATIVE_APP')

    def switch_to_web(self, context=None):
        """
        appium API
        Switch to web view.
        """
        current_context = self.driver.current_context
        if context is not None:
            self.driver.switch_to.context(context)
        elif "WEBVIEW" in current_context:
            return
        else:
            all_context = self.driver.contexts
            for context in all_context:
                if "WEBVIEW" in context:
                    self.driver.switch_to.context(context)
                    break
            else:
                raise NameError("No WebView found.")

    def switch_to_flutter(self):
        """
        appium API
         Switch to flutter app.
        """
        current_context = self.driver.current_context
        if current_context != "FLUTTER":
            self.driver.switch_to.context('FLUTTER')

    def key_text(self, text):
        """
        appium API
        Support input text, Chinese is not supported
        Usage:
            self.set_text("hello")
        """
        ke = KeyEvent(self.driver)
        ke.input(text)

    def key_text_capital(self, text):
        """
        appium API
        Support input capital text, Chinese is not supported
        Usage:
            self.key_text_capital("HELLO")
        """
        ke = KeyEvent(self.driver)
        ke.input_capital(text)

    def accept_alert(self):
        """
        selenium API
        Accept warning box.
        """
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        selenium API
        Dismisses the alert available.
        """
        self.driver.switch_to.alert.dismiss()

    def alert_is_display(self):
        """
        selenium API
        Determines if alert is displayed
        """
        try:
            self.driver.switch_to.alert
        except NoAlertPresentException:
            return False
        else:
            return True

    @property
    def get_alert_text(self):
        """
        selenium API
        Get warning box prompt information.
        """
        return self.driver.switch_to.alert.text

    def move_to_element(self, elem):
        """
        selenium API
        Moving the mouse to the middle of an element
        """
        warnings.warn("use page.elem.move_to_element() instead",
                      DeprecationWarning, stacklevel=2)
        ActionChains(self.driver).move_to_element(elem).perform()

    def click_and_hold(self, elem):
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        warnings.warn("use page.elem.click_and_hold() instead",
                      DeprecationWarning, stacklevel=2)
        ActionChains(self.driver).click_and_hold(elem).perform()

    def double_click(self, elem):
        """
        selenium API
        Double-clicks an element.
        """
        warnings.warn("use page.elem.double_click() instead",
                      DeprecationWarning, stacklevel=2)
        ActionChains(self.driver).double_click(elem).perform()

    def move_by_offset(self, x, y, click=False):
        """
        selenium API
        Moving the mouse to an offset from current mouse position.

        :Args:
         - x: X offset to move to, as a positive or negative integer.
         - y: Y offset to move to, as a positive or negative integer.
        """
        if click is True:
            ActionChains(self.driver).move_by_offset(x, y).click().perform()
        else:
            ActionChains(self.driver).move_by_offset(x, y).perform()

    def release(self):
        """
        selenium API
        Releasing a held mouse button on an element.
        """
        ActionChains(self.driver).release().perform()

    def context_click(self, elem):
        """
        selenium API
        Performs a context-click (right click) on an element.
        """
        warnings.warn("use page.elem.context_click() instead",
                      DeprecationWarning, stacklevel=2)
        ActionChains(self.driver).context_click(elem).perform()

    def drag_and_drop_by_offset(self, elem, x, y):
        """
        selenium API
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.
        :param elem: The element to mouse down.
        :param x: X offset to move to.
        :param y: Y offset to move to.
        """
        warnings.warn("use page.elem.drag_and_drop_by_offset(x, y) instead",
                      DeprecationWarning, stacklevel=2)
        ActionChains(self.driver).drag_and_drop_by_offset(elem, xoffset=x, yoffset=y).perform()

    def refresh_element(self, elem, timeout=10):
        """
        selenium API
        Refreshes the current page, retrieve elements.
        """
        warnings.warn("use page.elem.refresh_element() instead",
                      DeprecationWarning, stacklevel=2)
        try:
            timeout_int = int(timeout)
        except TypeError:
            raise ValueError("Type 'timeout' error, must be type int() ")

        for i in range(timeout_int):
            if elem is not None:
                try:
                    elem
                except StaleElementReferenceException:
                    self.driver.refresh()
                else:
                    break
            else:
                sleep(1)
        else:
            raise TimeoutError("stale element reference: element is not attached to the page document.")

    def top(self, elem, x, y, count):
        """
        appium API
        Perform a tap action on the element
        """
        action = MobileTouchAction(self.driver)
        action.tap(elem, x, y, count).perform()

    def press(self, elem, x, y, pressure):
        """
        appium API
        Begin a chain with a press down action at a particular element or point
        """
        action = MobileTouchAction(self.driver)
        action.press(elem, x, y, pressure).perform()

    def long_press(self, elem, x, y, duration):
        """
        appium API
        Begin a chain with a press down that lasts `duration` milliseconds
        """
        action = MobileTouchAction(self.driver)
        action.long_press(elem, x, y, duration).perform()

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        """
        appium API
        Swipe from one point to another point, for an optional duration.
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def back(self):
        """go back"""
        self.driver.back()

    def home(self):
        """press home"""
        self.driver.home()

    @staticmethod
    def sleep(sec: int) -> None:
        """
        Usage:
            page.sleep(seconds)
        """
        time.sleep(sec)

    def wait(self, secs: int = 10) -> None:
        """
        Implicitly wait.All elements on the page.
        Usage:
            page.wait(10)
        """
        self.driver.implicitly_wait(secs)

    def wait_script_timeout(self, time_to_wait):
        """
        Set the amount of time that the script should wait during an
           execute_async_script call before throwing an error.
        Usage:
            page.wait_script_timeout(10)
        """
        self.driver.set_script_timeout(time_to_wait)

    def wait_page_load_timeout(self, time_to_wait):
        """
        Set the amount of time to wait for a page load to complete
           before throwing an error.
        Usage:
            page.wait_page_load_timeout(10)
        """
        self.driver.set_page_load_timeout(time_to_wait)
