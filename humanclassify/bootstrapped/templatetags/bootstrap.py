from django import template
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

register = template.Library()

SCRIPT_TAG = '<script src="%sbootstrapped/js/%s" type="text/javascript"></script>'
PREFIX_SCRIPTS = ['affix', 'alert', 'button', 'carousel', 'collapse', 'dropdown', 'modal', 
        'popover', 'scrollspy', 'tab', 'tooltip', 'transition', 'typeahead']
        
NO_PREFIX_SCRIPTS = ['jquery', 'bootstrap.min']

def getScriptTag(featureName):
    
    if featureName in NO_PREFIX_SCRIPTS:
        out = '%s.js' % featureName
        return SCRIPT_TAG % (settings.STATIC_URL, out)        
        
    if featureName in PREFIX_SCRIPTS:
        out = 'bootstrap-%s.js' % featureName
        return SCRIPT_TAG % (settings.STATIC_URL, out)        
        
    raise ValueError("bootstrapped: Feature %s not available" % featureName)
    

        
    
    


class BootstrapJSNode(template.Node):

    def __init__(self, args):
        self.args = set(args)

    def render_all_scripts(self):
    
        results = [ getScriptTag('jquery'), getScriptTag('bootstrap.min'),]
        """
        for x in PREFIX_SCRIPTS:
            results.append( getScriptTag(x))
        """
        
        return '\n'.join(results)

    def render(self, context):
        if 'all' in self.args:
            return self.render_all_scripts()
        
        tags = [getScriptTag(tag) for tag in self.args]
        return '\n'.join(tags)
            
            

@register.simple_tag
def bootstrap_custom_less(less):
    output=[
            '<link rel="stylesheet/less" type="text/css" href="%s%s" media="all">' % (settings.STATIC_URL, less),
            '<script src="%ssbootstrapped/js/less-1.3.0.min.js" type="text/javascript"></script>' % settings.STATIC_URL,
        ]
    return '\n'.join(output)

@register.simple_tag
def bootstrap_css():
        return '<link rel="stylesheet" type="text/css" href="%sbootstrapped/css/bootstrap.css">' % settings.STATIC_URL

@register.simple_tag
def bootstrap_responsive_css():
        return '<link rel="stylesheet" type="text/css" href="%sbootstrapped/css/bootstrap_responsive.css">' % settings.STATIC_URL


@register.simple_tag
def bootstrap_less():
    output=[
            '<link rel="stylesheet/less" type="text/css" href="%ssbootstrapped/lib/bootstrap.less">' % settings.STATIC_URL,
            '<script src="%s%ssbootstrapped/js/less-1.3.0.min.js" type="text/javascript"></script>' % settings.STATIC_URL,
        ]
    return '\n'.join(output)

@register.tag(name='bootstrap_js')
def do_bootstrap_js(parser, token):
    #print '\n'.join(token.split_contents())
    return BootstrapJSNode(token.split_contents()[1:])
    
    
    
#this has been merged from django-bootstrap-form
@register.filter
def bootstrapform(element):
    element_type = element.__class__.__name__.lower()

    if element_type == 'boundfield':
        template = get_template("bootstrapform/field.html")
        context = Context({'field': element})
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            template = get_template("bootstrapform/formset.html")
            context = Context({'formset': element})
        else:
            template = get_template("bootstrapform/form.html")
            context = Context({'form': element})
        
    return template.render(context)


#this has been merged from django-bootstrap-form
@register.filter
def bootstrapform_tooltip(element):
    print element
    element_type = element.__class__.__name__.lower()

    if element_type == 'boundfield':
        template = get_template("bootstrapform/field.html")
        context = Context({'field': element})
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            template = get_template("bootstrapform/formset.html")
            context = Context({'formset': element})
        else:
            template = get_template("bootstrapform/form.html")
            context = Context({'form': element})
        
    return template.render(context)



@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"


@register.filter
def is_radio(field):
    return field.field.widget.__class__.__name__.lower() == "radioselect"


@register.simple_tag
def active_if_starts(path, pattern):
    if path.startswith(pattern):
        return 'active'
    return ''
    
@register.filter
def before_pipe(content):
    pieces = content.split("|")
    return pieces[0]
    
@register.filter
def after_pipe(content):
    pieces = content.split("|")
    if len(pieces) == 2:
        return pieces[1]
    return ""
    
    
    