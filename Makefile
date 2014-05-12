cleanup:
	find . -name '*.pyc' -delete
	find . -name 'sessions' | xargs rm -rf 

lint:
	flake8 . --ignore=E501

run:
	. ~/.monitor/bin/activate
	cd www/ && gunicorn application:wsgiapp -b 0.0.0.0:8009 -D -w4

rundev:
	cd www/ && python application.py 8888

test:
	nosetests tests/ www/ --with-cov --with-doctest -v -s
