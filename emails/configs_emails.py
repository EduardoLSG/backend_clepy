from django.template.loader import render_to_string


def email_welcome(ctx:dict, template:str):
    subject = """SEJA BEM VINDO A CLEPY"""
    html_body = render_to_string(template, ctx)
    return subject, html_body

def email_not(ctx:dict, template:str):
    subject = """NOTIFICAÇÃO - CLEPY"""
    html_body = render_to_string(template, ctx)
    return subject, html_body

def email_passwd(ctx:dict, template:str):
    subject = """RESET DE SENHA"""
    html_body = render_to_string(template, ctx)
    return subject, html_body