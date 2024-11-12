# (C) 2024 GoodData Corporation
include ../project_common.mk

.PHONY: docs
docs:
	tox $(TOX_FLAGS) -e docs


.PHONY: dev-certs
dev-certs:
	mkdir -p test_data
	# create CA with self-signed certificate > generate keys + cert requests for server and client > sign
	cd test_data && \
		rm -f *.pem && \
		openssl req -x509 -newkey rsa:4096 -days 3650 -nodes -keyout ca-key.pem -out ca-cert.pem -subj "/C=NA/ST=Unknown/L=Unknown/O=Unknown/OU=Unknown/CN=localhost/emailAddress=example@example.com" && \
		openssl req -newkey rsa:4096 -nodes -keyout server-key.pem -out server-req.pem -subj "/C=NA/ST=Unknown/L=Unknown/O=Unknown/OU=Computer/CN=localhost/emailAddress=example@example.com" && \
		openssl req -newkey rsa:4096 -nodes -keyout client-key.pem -out client-req.pem -subj "/C=NA/ST=Unknown/L=Unknown/O=Unknown/OU=Computer/CN=testClient1/emailAddress=example@example.com" && \
		openssl x509 -req -in server-req.pem -days 3650 -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem && \
		openssl x509 -req -in client-req.pem -days 3650 -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out client-cert.pem
