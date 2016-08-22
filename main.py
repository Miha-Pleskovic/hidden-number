#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "html")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hidden-number.html")

    def post(self):
        hidden_number = 42
        guess = self.request.get("guess")
        if guess.isdigit():
            if guess == str(hidden_number):
                result = "Čestitke, uspelo ti je! Le kako si vedel?"
            elif int(guess) < hidden_number:
                result = "Žal ne. V mislih smo imeli malo večjo številko."
            elif int(guess) > hidden_number:
                result = "Žal ne. V mislih smo imeli malo manjšo številko."
        else:
            result = "Tvoja številka ni številka. Poskusi znova."
        self.write(result)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler)
], debug=True)
