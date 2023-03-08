from crispy_forms.layout import LayoutObject
from crispy_forms.utils import flatatt, TEMPLATE_PACK
from django.template.loader import render_to_string


class ModalContentLayout(LayoutObject):  # TODO move to lib?
    template = "%s/layout/modal_content.html"
    modal_title = ''

    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)
        self.modal_id = kwargs.pop("modal_id", None)
        self.modal_title = kwargs.pop("modal_title", None)
        self.modal_close = kwargs.pop("modal_close", None)
        self.modal_submit = kwargs.pop("modal_submit", None)
        self.modal_message = kwargs.pop("modal_message", None)
        self.modal_body = kwargs.pop("modal_body", None)
        # self.css_class = kwargs.pop("css_class", "")
        # self.css_id = kwargs.pop("css_id", None)
        self.template = kwargs.pop("template", self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

        # modal_title = ""
        # if self.legend:
        #     modal_title = "%s" % Template(str(self.modal_title)).render(context)

        template = self.get_template_name(template_pack)

        return render_to_string(
            template, {
                "fieldset": self,
                "modal_id": self.modal_id,
                "modal_title": self.modal_title,
                "modal_close": self.modal_close,
                "modal_submit": self.modal_submit,
                "modal_message": self.modal_message,
                "modal_body": self.modal_body,
                "fields": fields,
                "form_style": form_style
            }
        )


class ModalLayout(LayoutObject):  # TODO move to lib?
    template = "%s/layout/modal.html"
    modal_title = ''

    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)
        self.css_class = kwargs.pop("css_class", "")
        self.css_id = kwargs.pop("css_id", "")
        self.template = kwargs.pop("template", self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

        template = self.get_template_name(template_pack)

        return render_to_string(
            template, {
                "fieldset": self,
                "css_class": self.css_class,
                "css_id": self.css_id,
                "fields": fields,
                "form_style": form_style
            }
        )
