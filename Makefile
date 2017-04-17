deb=deb/target
version=1.1
deb:src
	mkdir -p $(deb)/usr/bin
	mkdir -p $(deb)/usr/share/hand-network
	mkdir -p $(deb)/usr/share/applications
	cp bin/* $(deb)/usr/bin
	cp src/* $(deb)/usr/share/hand-network
	cp share/* $(deb)/usr/share/hand-network
	cp applications/* $(deb)/usr/share/applications
	cp -r deb/DEBIAN $(deb)
	dpkg-deb -b $(deb) hand-network_$(version)_amd64.deb

clean:
	- rm -rf $(prefix)
	- rm hand-network_$(version)_amd64.deb
	- rm src/*.pyc
