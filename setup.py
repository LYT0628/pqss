from distutils.core import setup

setup(
    name='PQSS',
    packages=['pqss', 'pqss.env', 'pqss.lex', 'pqss.parse', 'pqss.parse.ast', 'pqss.util'],
    author='lyt0628',
    author_email='lyt.0628@qq.com',
    url='http://lyt0628.icu/docs/pqss',
    download_url='http://pypi.org//pqss',
    description='PQSS is a dynamic language for qss, like scss for css.'
)