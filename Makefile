control.Description:=Convert SRS cards to the `anki` format

.PHONY: install
install: dist/$(archivename).deb
	# install -d $(PREFIX)/ankiconv
	# install -m 0644 -t $(PREFIX)/ankiconv

.PHONY: uninstall
uninstall:
	$(RM) -r $(PREFIX)/ankiconv

USERNAME?=$(shell git config user.name)
EMAIL?=$(shell git config user.email)

## Name of the archive.
archivename?=$(shell basename `pwd`)

default: dist/$(archivename).deb

## Name of the Debian package.
control.Package?=$(archivename)

## Version of the Debian package.
control.Version?=1.0.0

## Section of the Debian package.
control.Section?=user/hidden

## Priority of the Debian package.
control.Priority?=optional

## Architecture of the Debian package.
control.Architecture?=all

## Architecture of the RPM package.
alien.rpm.Architecture?=$(if $(filter all,$(control.Architecture)),noarch,$(control.Architecture))

## Installed size of the Debian package.
control.Installed-Size?=`du -cks data/ | tail -n 1 | cut -f 1`

## Maintainer of the Debian package.
control.Maintainer?=$(USERNAME) <$(EMAIL)>

## Description of the Debian package.
control.Description?=$(error control.Description required)

.PHONY: dist
## Creates the distribution archives.
dist: dist/$(archivename).tar.gz dist/$(archivename).tar.bz2 dist/$(archivename).zip dist/$(archivename).deb # dist/$(archivename)-$(control.Version)-1.$(alien.rpm.Architecture).rpm

dist/%.tar.gz: dist/%.tar

dist/%.tar.bz2: dist/%.tar

%.gz: %
	<$< gzip -9 >$@

%.bz2: %
	<$< bzip2 -9 >$@

dist/$(archivename).tar dist/$(archivename).zip:
	mkdir -p dist
	git archive -o $@ --prefix $(archivename)/ HEAD .

.PHONY: clean
clean: cleanDist

cleanDist:
	$(RM) -r dist control data/ data.tar.gz control.tar.gz debian-binary

control: data/
	echo -n "$(foreach key,Package Version Section Priority Architecture Installed-Size Maintainer Description,$(key): $(control.$(key))\n)" | sed 's/^ //' >$@

control.tar.gz: control
	tar czf $@ $^

data.tar.gz: | data/
	tar czf $@ --transform 's,^\./,/,' -C data/ .

data/:
	mkdir -p data
	cp *.py data/
	# $(MAKE) PREFIX=data/usr/ install

debian-binary:
	echo 2.0 >$@

dist/$(archivename).deb: debian-binary control.tar.gz data.tar.gz
	ar -Drc $@ $^

dist/$(archivename)-$(control.Version)-1.$(alien.rpm.Architecture).rpm: dist/$(archivename).deb
	cd dist/ ; alien -r --bump=0 $(archivename).deb
