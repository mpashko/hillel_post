from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver

from articles.models import Article


class SeleniumTest(StaticLiveServerTestCase):

    NUMBER_OF_ARTICLES = 10

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    def setUp(self) -> None:
        self.user = User.objects.create(first_name='John', last_name='Doe')
        self._create_articles(self.NUMBER_OF_ARTICLES)

    def _create_articles(self, num):
        for article_num in range(num):
            Article.objects.create(
                title=f'Article #{str(article_num)}',
                text='some text',
                author=self.user
            )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_unsuccessful_login(self):
        self.selenium.get(self.live_server_url)

        login_url = self.selenium.find_element_by_id('login')
        login_url.click()

        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('test')

        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('test')

        submit_btn = self.selenium.find_element_by_id('submit_login')
        submit_btn.submit()

        error = self.selenium.find_element_by_id('error')
        expected_error = "Your username and password didn't match. Please try again."
        self.assertEqual(error.text, expected_error)

    def test_sign_up(self):
        self.selenium.get(self.live_server_url)

        login_url = self.selenium.find_element_by_id('login')
        login_url.click()

        sign_up_btn = self.selenium.find_element_by_id('sign_up')
        sign_up_btn.click()

        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys('test@hillepost.com')

        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('test')

        password = 'as79fssdfm97s'
        password_input = self.selenium.find_element_by_name('password1')
        password_input.send_keys(password)

        password_input = self.selenium.find_element_by_name('password2')
        password_input.send_keys(password)

        submit_btn = self.selenium.find_element_by_tag_name('button')
        submit_btn.submit()

        notification = self.selenium.find_element_by_id('notification')
        expected_notification = 'Please confirm your email address to complete the ' \
                                'registration.'
        self.assertEqual(notification.text, expected_notification)

    def test_check_pagination(self):
        self.selenium.get(self.live_server_url)

        pagination = self.selenium.find_element_by_class_name('pagination')

        self.assertTrue(bool(pagination))

    def test_pagination_hide_for_single_page(self):
        Article.objects.all().delete()
        self._create_articles(3)

        self.selenium.get(self.live_server_url)

        expected_message = 'Unable to locate element'
        with self.assertRaisesMessage(NoSuchElementException, expected_message):
            self.selenium.find_element_by_class_name('pagination')
