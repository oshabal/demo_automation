from playwright.sync_api import expect
from packages.utils import tools
from functools import wraps
from zipfile import ZipFile
from faker import Faker
import random

class Base:
    def __init__(self, page):
        self.page = page
        self.fake_data = Faker()

    def get_visible_element(self, locator):
        count = locator.count()
        for i in range(count):
            nth = locator.nth(i)
            if nth.is_visible():
                visible_locator = nth
        return visible_locator

    def get_visible_elements(self, locator):
        count = locator.count()
        visible_locators = []
        for i in range(count):
            nth = locator.nth(i)
            if nth.is_visible():
                visible_locators.append(nth)
        return visible_locators

    def pick_from_list(self, locators_list, index=None):
        try:
            element = locators_list[index]
        except (TypeError, IndexError):
            index = random.randint(0, len(locators_list)-1)
            element = locators_list[index]
        return element

    def click_random_area(self, locator):
        box = locator.bounding_box()
        locator.click(
            position={
                "x": random.uniform(0, box["width"]),
                "y": random.uniform(0, box["height"]),
            })

    def clear_n_type(self, locator, value):
        locator.press("Meta+a")
        locator.press("Backspace")
        self.page.keyboard.insert_text(str(value))
        expect(locator).to_have_value(value)

    def toggle(self, locator, set_state):
        current_state = locator.get_attribute("aria-checked")
        if set_state is True:
            if current_state == "true":
                pass
            else:
                locator.click()
                expect(locator).to_have_attribute("aria-checked", "true")
        elif set_state is False:
            if current_state == "false":
                pass
            else:
                locator.click()
                expect(locator).to_have_attribute("aria-checked", "false")

class Path(Base):
    def home(self):
        self.page.goto('/', wait_until="networkidle")
        expect(self.page).to_have_title("Home | Colorful")
        expect(self.page).to_have_url("https://www.colorful.app/")

    def showcase(self):
        self.page.goto('/showcases/showcase', wait_until="networkidle")
        expect(self.page).to_have_title("colorful.app")
        expect(self.page).to_have_url("https://www.colorful.app/showcases/showcase")

    def packshot_generator(self):
        self.page.goto('https://packshot.colorful.app/', wait_until="networkidle")
        expect(self.page).to_have_title("Colorful - Create realistic packshots using a 3D model")
        expect(self.page).to_have_url("https://packshot.colorful.app/")

    def careers(self):
        self.page.goto('/careers', wait_until="networkidle")
        expect(self.page).to_have_title("Careers")
        expect(self.page).to_have_url("https://www.colorful.app/careers")

class Background(Base):
    @property
    def colorpicker(self):
        return self.page.locator(".chrome-picker ")

    @property
    def bg_button(self):
        locator = self.page.locator('.w-10') # rework
        return self.get_visible_element(locator)

    def open_colorpicker(self):
        if not self.colorpicker.is_visible():
            self.bg_button.click()
            self.colorpicker.wait_for(state="visible")

    def close_colorpicker(self):
        overlay = self.page.locator('[id="headlessui-portal-root"] >> [role="dialog"]')
        if self.colorpicker.is_visible():
            overlay.click(position={'x': 0, 'y': 0})
            self.colorpicker.wait_for(state="hidden")

    def switch(self, locator):
        switch = self.colorpicker.locator("svg")
        count = locator.count()
        while count == 0:
            switch.click()
            count = locator.count()

    def hsv(self):
        saturation = self.page.locator(".saturation-black")
        hue = self.page.locator(".hue-horizontal")
        self.open_colorpicker()
        self.click_random_area(saturation)
        self.click_random_area(hue)
        self.close_colorpicker()

    def hex(self, value=None):
        hex_input = self.page.locator('label:has-text("hex")')
        if value is None: value = self.fake_data.hex_color()
        self.open_colorpicker()
        self.switch(hex_input)
        self.clear_n_type(hex_input, value)
        self.close_colorpicker()

    def rgb(self, values=None):
        r_input = self.page.locator('label:has-text("r")')
        g_input = self.page.locator('label:has-text("g")')
        b_input = self.page.locator('label:has-text("b")')
        if values is None: values = self.fake_data.rgb_color()
        r, g, b = values.split(',')
        self.open_colorpicker()
        self.switch(r_input)
        self.clear_n_type(r_input, r)
        self.clear_n_type(g_input, g)
        self.clear_n_type(b_input, b)
        self.close_colorpicker()

    def hsl(self, values=None):
        h_input = self.page.locator('label:has-text("h")')
        s_input = self.page.locator('label:has-text("s")')
        l_input = self.page.locator('label:has-text("l")')
        if values is None: values = self.fake_data.rgb_color()
        h, s, l = values.split(',')
        self.open_colorpicker()
        self.switch(l_input)
        self.clear_n_type(h_input, h)
        self.clear_n_type(s_input, s)
        self.clear_n_type(l_input, l)
        self.close_colorpicker()

class Packshot_Generator(Base):
    @property
    def images(self):
        elements = self.page.locator('img[alt="front"], img[alt="back"], img[alt="diagonal"], img[alt="custom"], img[alt="render"]')
        return self.get_visible_elements(elements)

    @property
    def canvas(self):
        locator = self.page.locator('canvas')
        return self.get_visible_element(locator)

    @property
    def shadows_toogle(self):
        locator = self.page.locator('button[role="switch"]:has-text("Shadows")')
        return self.get_visible_element(locator)

    @property
    def transparent_toogle(self):
        locator = self.page.locator('button[role="switch"]:has-text("Transparent")')
        return self.get_visible_element(locator)

    @property
    def four_k_toogle(self):
        locator = self.page.locator('button[role="switch"]:has-text("4K resolution")')
        return self.get_visible_element(locator)

    @property
    def generate_button(self):
        element = self.page.locator('text=Generate')
        return self.get_visible_element(element)

    @property
    def background(self):
        return Background(self.page)

    # Decorator to validate image count after add/delete action
    def counter_comparator(count):
        def decorator(method):
            @wraps(method)
            def _decorator(self):
                # Compare images count with generate button value before action
                image_count_before = len(self.images)
                button_value_before = tools.get_int_from_string(self.generate_button.inner_text())
                assert image_count_before == button_value_before
                # Perform action (add/delete image)
                method(self)
                # Compare images count with generate button value after action
                image_count_after = len(self.images)
                button_value_after = tools.get_int_from_string(self.generate_button.inner_text())
                assert image_count_after == button_value_after
                if count == "+":
                    assert image_count_after == image_count_before+1
                    assert button_value_after == button_value_before+1
                if count == "-":
                    assert image_count_after == image_count_before-1
                    assert button_value_after == button_value_before-1
            return _decorator
        return decorator

    def wait_for_model_upload(self, timeout=60000):
        selector = "text='Ready ✓' >> nth=0"
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)

    def wait_for_image_render(self, timeout=300000):
        selector = 'button:has-text("Download all")'
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)

    def get_state(self):
        state = {
            "images_count": len(self.images),
            "shadows": self.shadows_toogle.get_attribute("aria-checked"),
            "transparent": self.transparent_toogle.get_attribute("aria-checked"),
            "four_k_resolution": self.four_k_toogle.get_attribute("aria-checked"),
            "background_color": tools.get_int_from_string(self.background.bg_button.get_attribute("style")),
        }
        return state

    def upload_3D_model(self, file_name=None):
        upload_button = self.page.locator("text=Upload 3D model")
        file_path = tools.get_filepath(directory="3D_models", file_name=file_name)
        with self.page.expect_file_chooser() as fc_info:
            upload_button.click()
        file_chooser = fc_info.value
        with self.page.expect_navigation(wait_until="networkidle", timeout=60000):
            file_chooser.set_files(file_path)
        self.wait_for_model_upload()

    def upload_sample_3D_model(self, option=None):
        options = ['[id="example_model0"]', '[id="example_model1"]', '[id="example_model2"]']
        try:
            option = options[option]
        except (TypeError, IndexError):
            option = random.choice(options)
        with self.page.expect_navigation(wait_until="networkidle", timeout=60000):
            self.page.locator(option).click()
        self.wait_for_model_upload()

    def shadows(self, set_state):
        self.toggle(self.shadows_toogle, set_state)

    def transparent(self, set_state):
        self.toggle(self.transparent_toogle, set_state)

    def four_k_resolution(self, set_state):
        self.toggle(self.four_k_toogle, set_state)

    def zoom_in(self, times=1):
        locator = self.page.locator('button:has-text("+")')
        button = self.get_visible_element(locator)
        button.click(click_count=times)

    def zoom_out(self, times=1):
        locator = self.page.locator('button:has-text("-")')
        button = self.get_visible_element(locator)
        button.click(click_count=times)

    def drag(self):
        canvas_area = self.canvas.bounding_box()
        self.page.drag_and_drop(
            'canvas',
            'canvas',
            source_position={
                "x": random.uniform(0, canvas_area["width"]),
                "y": random.uniform(0, canvas_area["height"]),
            },
            target_position={
                "x": random.uniform(0, canvas_area["width"]),
                "y": random.uniform(0, canvas_area["height"]),
            },
        )

    @counter_comparator(count='+')
    def add_image(self):
        selector = 'text="+" >> nth=0'  # <rework>
        button = self.page.locator(selector)
        button.click()

    @counter_comparator(count='-')
    def delete_image(self, index=None):
        image = self.pick_from_list(self.images, index=index)
        box = image.bounding_box()
        image.hover()
        image.click(position={"x": box["width"], "y": 0}, force=True)

    def select_image(self, index=None):
        image = self.pick_from_list(self.images, index=index)
        image.click()

    def generate_images(self, email=None):
        if email is None: email = self.fake_data.email()
        state_before = self.get_state()
        with self.page.expect_navigation(wait_until="networkidle", timeout=60000):
            self.generate_button.click()
            self.page.keyboard.insert_text(email)
            self.page.keyboard.press('Enter')
        self.wait_for_image_render()
        state_after = self.get_state()
        assert state_before == state_after

    def download_all(self):
        button = self.page.locator('button:has-text("Download all")')
        with self.page.expect_download() as download_info:
            button.click()
        download = download_info.value
        with ZipFile(download.path()) as archive:
            archive.printdir()
