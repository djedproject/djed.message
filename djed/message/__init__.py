from pyramid.compat import escape, string_types
from djed.templates import render, template_filter


def add_message(request, msg, type='info'):
    """ Add status message

    Predefined message types

    * info

    * success

    * warning

    * error

    """
    if ':' not in type:
        type = 'message:%s'%type

    request.session.flash(render(request, type, msg), 'status')


def render_messages(request):
    """ Render previously added messages """
    return ''.join(request.session.pop_flash('status'))


def error_message(context, request):
    """ Error message filter """
    if not isinstance(context, (set, list, tuple)):
        context = (context,)

    errors = []
    for err in context:
        if isinstance(err, Exception):
            err = '%s: %s'%(
                err.__class__.__name__, escape(str(err), True))
        errors.append(err)

    return {'errors': errors}


def includeme(config):
    config.include('pyramid_chameleon')
    config.include('djed.templates')

    config.add_layer('message', path='djed.message:templates/')

    config.add_request_method(add_message, 'add_message')
    config.add_request_method(render_messages, 'render_messages')


    config.add_template_filter('message:error', error_message)
