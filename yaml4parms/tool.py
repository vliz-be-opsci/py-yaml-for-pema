import yaml
import logging


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


    # todo have an 'about' property
    # todo have a tojson() on the model
    # todo have a template driven tohtml()
    # todo have a validate(strict=True) method to check on some schema requirements .


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
