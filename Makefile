UNAME := $(shell uname)
REQUIREMENTS := Plone -c https://dist.plone.org/release/6.0-dev/constraints.txt

all: build generate_graph

build:
	# The Darwin-like OS implementation
	if [ "$(UNAME)" = "Darwin" ]; then \
		brew install graphviz; \
		pip install --global-option=build_ext --global-option="-I/include/" --global-option="-L/lib/" pipdeptree pipforester; \
		mkdir venvs; \
		mkdir trees; \
		python -m venv ./venvs/plone_venv; \
		python -m venv ./venvs/graph_venv; \
		./venvs/plone_venv/bin/ install --no-cache $(REQUIREMENTS); \
		./venvs/graph_venv/bin/pip install --no-cache -r graph_requirements.txt; \
	fi

	# The Debian-like OS implementation
	if [ "$(UNAME)" = "Linux" ]; then \
		apt-get install -y graphviz-dev; \
		mkdir venvs; \
		mkdir trees; \
		python -m venv ./venvs/plone_venv; \
		python -m venv ./venvs/graph_venv; \
		./venvs/plone_venv/bin/pip install $(REQUIREMENTS); \
		./venvs/graph_venv/bin/pip install -r graph_requirements.txt; \
	fi

generate_graph:
	if [ "$(UNAME)" = "Darwin" ]; then \
		./venvs/graph_venv/bin/python -m pipdeptree --python ./venvs/plone_venv/bin/python -j -e 'zope*','zc.*','z3c.*','setuptools','six','zodb*','five.*','accesscontrol','piexif','pillow','cookiecutter','pycparser','cffi','zdaemon','zeo','extensionclass','acquisition','persistence','persistent','zexceptions','roman','datetime','record','missing','python-dateutil','arrow','jinja2-time','jinja2','markupsafe','beautifulsoup4','unidecode','transaction','lxml','future','btrees','docutils','simplejson','cssselect','pyrsistent','attrs','jsonschema','requests','pyjwt','authencoding','binaryornot','chardet','restrictedpython','documenttemplate','products.pythonscripts','collective.monkeypatcher','pytz','certifi','chameleon','charset-normalizer','click','idna','multimapping','multipart','paste','pastedeploy','pip','pipdeptree','python-gettext','python-slugify','text-unidecode','decorator','soupsieve','pyyaml','urllib3','wheel','zconfig','webtest','waitress','webob','wsgiproxy2','sgmllib3k','feedparser','markdown','mxmake','mxdev','inquirer','blessed','wcwidth','python-editor','readchar','importlib-metadata','importlib-resources','pkgutil-resolve-name','zipp' > ./trees/deptree.json; \
		./venvs/graph_venv/bin/python -m pipforester -i deptree.json -o ./trees/deptree.dot; \
		./venvs/graph_venv/bin/python -m pipforester --cycles -i deptree.json -o ./trees/depcycles.dot; \
	fi

	if [ "$(UNAME)" = "Linux" ]; then \
		./venvs/graph_venv/bin/python -m pipdeptree --python ./venvs/plone_venv/bin/python -j -e zope*,zc.*,z3c.*,setuptools,six,zodb*,five.*,accesscontrol,piexif,pillow,cookiecutter,pycparser,cffi,zdaemon,zeo,extensionclass,acquisition,persistence,persistent,zexceptions,roman,datetime,record,missing,python-dateutil,arrow,jinja2-time,jinja2,markupsafe,beautifulsoup4,unidecode,transaction,lxml,future,btrees,docutils,simplejson,cssselect,pyrsistent,attrs,jsonschema,requests,pyjwt,authencoding,binaryornot,chardet,restrictedpython,documenttemplate,products.pythonscripts,collective.monkeypatcher,pytz,certifi,chameleon,charset-normalizer,click,idna,multimapping,multipart,paste,pastedeploy,pip,pipdeptree,python-gettext,python-slugify,text-unidecode,decorator,soupsieve,pyyaml,urllib3,wheel,zconfig,webtest,waitress,webob,wsgiproxy2,sgmllib3k,feedparser,markdown,mxmake,mxdev,inquirer,blessed,wcwidth,python-editor,readchar,importlib-metadata,importlib-resources,pkgutil-resolve-name,zipp > deptree.json; \
		./venvs/graph_venv/bin/python -m pipforester -i deptree.json -o ./trees/deptree.dot; \
		./venvs/graph_venv/bin/python -m pipforester --cycles -i deptree.json -o ./trees/depcycles.dot; \
	fi

	dot -Tpng ./trees/deptree.dot -o outdeptree.png
	dot -Tsvg ./trees/deptree.dot -o outdeptree.svg
	dot -Tjpeg ./trees/deptree.dot -o outdeptree.jpeg

	dot -Tpng ./trees/depcycles.dot -o outdepcycles.png
	dot -Tsvg ./trees/depcycles.dot -o outdepcycles.svg
	dot -Tjpeg ./trees/depcycles.dot -o outdepcycles.jpeg