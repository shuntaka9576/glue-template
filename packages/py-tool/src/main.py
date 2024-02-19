from jinja2 import Template


def render_hello_template(context):
    template_str = "Hello {{ name }}"
    template = Template(template_str)

    return template.render(context)


def main():
    params = {"name": "World"}
    render_hello_template(params)


if __name__ == "__main__":
    main()
