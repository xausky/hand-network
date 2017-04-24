DESTDIR=target
version=1.1
.PHONY: install clean

install:
	mkdir -p $(DESTDIR)/usr/bin
	mkdir -p $(DESTDIR)/usr/share/hand-network
	mkdir -p $(DESTDIR)/usr/share/applications
	cp bin/* $(DESTDIR)/usr/bin
	cp src/* $(DESTDIR)/usr/share/hand-network
	cp share/* $(DESTDIR)/usr/share/hand-network
	cp applications/* $(DESTDIR)/usr/share/applications
clean:
	- rm src/*.pyc
	- rm -rf src/__pycache__
