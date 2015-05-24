from pyramid.compat import text_

from .base import BaseTestCase
from djed.message import add_message
from djed.message import render_messages


class TestStatusMessages(BaseTestCase):

    def test_messages_addmessage(self):
        add_message(self.request, 'message')
        res = render_messages(self.request).strip()

        self.assertIn('alert-info', res)
        self.assertIn('message', res)

    def test_messages_warning_msg(self):
        add_message(self.request, 'warning-message', 'warning')
        res = render_messages(self.request).strip()

        self.assertIn('alert-warning', res)
        self.assertIn('warning-message', res)

    def test_messages_error_msg(self):
        add_message(self.request, 'error-message', 'error')
        res = render_messages(self.request).strip()

        self.assertIn('alert-danger', res)
        self.assertIn('error-message', res)

        add_message(self.request, ValueError('Error'), 'error')
        res = render_messages(self.request).strip()

        self.assertIn('alert-danger', res)
        self.assertIn('ValueError: Error', res)

    def test_multi_error(self):
        add_message(self.request, ['error1', ValueError('error2')], 'error')

        res = render_messages(self.request)
        self.assertIn('error1', res)
        self.assertIn('ValueError: error2', res)

    def test_messages_custom_msg(self):
        self.config.add_layer(
            'message', 'test', path='tests:message/')

        add_message(self.request, 'message', 'custom')
        self.assertEqual(
            render_messages(self.request).strip(),
            '<div class="customMsg">message</div>')

    def test_messages_custom_msg_different_type(self):
        self.config.add_layer(
            'test', path='tests:message/')

        add_message(self.request, 'message', 'test:custom')
        self.assertEqual(
            render_messages(self.request).strip(),
            '<div class="customMsg">message</div>')

    def test_messages_render_message_with_error(self):
        self.config.add_layer(
            'message', 'test', path='tests:messages/')

        def customMessage(context, request):
            raise ValueError()

        self.config.add_template_filter('message:custom', customMessage)

        self.assertRaises(
            ValueError, add_message, self.request, 'message', 'custom')

    def test_messages_render(self):
        add_message(self.request, 'message')
        res = render_messages(self.request).strip()

        self.assertIn('message', res)

        msg = render_messages(self.request)
        self.assertEqual(msg, '')

    def test_messages_unknown_type(self):
        from djed.templates import RendererNotFound

        self.assertRaises(
            RendererNotFound,
            add_message, self.request, 'message', 'unknown')

    def test_messages_request_attr(self):
        """
        Request has `add_message` and `render_messages` methods
        """
        req = self.make_request()
        req.add_message('message')

        res = req.render_messages().strip()

        self.assertIn('message', res)
