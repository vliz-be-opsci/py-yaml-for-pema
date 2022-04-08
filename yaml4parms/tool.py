import yaml
import json
import os
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape


log = logging.getLogger(__name__)


class ParameterDescription():
    """ Wrapper class representing the information structure read from the parameters file.
    """

    def __init__(self, ymls: str):
        """ Creates the ParameterDescription model from the passed yml

        :param ymls: the yaml-string holding the params description
        """
        self._ymls = ymls
        self._model = ParameterDescription.yamlparse(ymls)

    def __repr__(self):
        return f'ParameterDescription("""{self._ymls}""")'

    def __str__(self):
        return self._ymls

    def __iter__(self):
        return iter(self._model['parameters'])

    def __getitem__(self, key: str):
        return self._model['parameters'][key]

    @property
    def about(self):
        return self._model['about']

    def format(self, format: str ='yml'):
        if (format == 'json'):
            return self.as_json()
        #else
        if (format == 'html'):
            return self.as_html()
        #else
        log.warning("TODO implement mutliple formats html, csv(?)")
        return str(self)

    def as_json(self):
        return json.dumps(self._model, indent=2)

    def as_html(self):
        # find j2 folder relative to __file__
        j2fldr = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'j2')
        assert os.path.isdir(j2fldr), "no template folder found"
        tname = 'parms2form.html.j2'
        assert os.path.isfile(os.path.join(j2fldr, tname)), 'template to use not found'
        # make j2 context
        j2env = Environment(
            loader=FileSystemLoader(j2fldr),
            autoescape=select_autoescape(
                default_for_string=True,
                default=True
            ),
        )
        # j2env.globals = dict_of_useful_functions
        # j2env.filters.update(dict_of_useful_filters)

        # compile template
        tpl = j2env.get_template(tname)
        # render result
        html = tpl.render(dict(parms=self))
        return html

    # todo have a validate(strict=True) method to check on some schema requirements .
    # e.g. only contains elms we know about
    #      only 1 validation can have regex, range, ...

    @staticmethod
    def yamlparse(content: str):
        try:
            return yaml.safe_load(content)
        except (RuntimeError, Exception) as e:
            log.error(f"Error while parsing the content\n--\n{content}")
            log.error("-- end content")
            log.exception(e)
            raise e

    @staticmethod
    def read(src: str, prefix: str = '#= '):
        # todo allow src to point to a url directly
        fname = src
        pfxlen = len(prefix)
        content = ""
        with open(fname, 'r') as fin:
            for line in fin.readlines():
                if line[:pfxlen] == prefix:
                    content += line[pfxlen:]
        return ParameterDescription(content)


read = ParameterDescription.read
