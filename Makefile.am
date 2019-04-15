SUFFIXES = .c .mod .def .o .obj .lo .a .m .mxm

SHELL=/bin/bash

prefix= @prefix@
datarootdir= @datarootdir@
srcdir= @srcdir@
mandir= @mandir@
exec_prefix=@exec_prefix@
bindir= @bindir@
INSTALL_PROGRAM = install

help:  force
	@echo "knows about:  all, clean, install"

build: all

all: doorh.png doorv.png doorh-bw.png doorv-bw.png hingeh.png \
     wallh.png wallv.png wallh-bw.png wallv-bw.png hellknight.png tick.png \
     doom3.png rock1sid.png sb_rocket.png sb_nails.png num_colon.png \
     wizwood1_4.png inv2_sshotgun.png inva1_nailgun.png inva1_rlaunch.png \
     inva1_srlaunch.png afloor3_1_gloss.png city1_7.png adoor01_2.png \
     city1_4_gloss.png city2_1.png
	pnmscale -xsize=100 -ysize=100 $< > t.pnm
	pnmtopng t.pnm > $@
	$(RM) t.pnm

city1_4_gloss.png: $(srcdir)/touchmap-extra2/city1_4_gloss.jpg
	convert -resize 100x100 $< $@

city2_1.png: $(srcdir)/touchmap-extra2/city2_1.jpg
	convert -resize 100x100 $< $@

afloor3_1_gloss.png: $(srcdir)/touchmap-extra2/afloor3_1_gloss.jpg
	convert -resize 100x100 $< $@


adoor01_2.png: $(srcdir)/touchmap-extra2/adoor01_2.jpg
	convert -resize 100x100 $< $@
city1_7.png: $(srcdir)/touchmap-extra2/city1_7.jpg
	convert -resize 100x100 $< $@

inv2_sshotgun.png: $(srcdir)/touchmap-extra2/inv2_sshotgun.png
	convert -resize 100x100 $< $@

inva1_nailgun.png: $(srcdir)/touchmap-extra2/inva1_nailgun.png
	convert -resize 100x100 $< $@

inva1_rlaunch.png: $(srcdir)/touchmap-extra2/inva1_rlaunch.png
	convert -resize 100x100 $< $@


inva1_srlaunch.png: $(srcdir)/touchmap-extra2/inva1_srlaunch.png
	convert -resize 100x100 $< $@

wizwood1_4.png: $(srcdir)/touchmap-extra2/wizwood1_4.jpg
	convert -resize 100x100 $< $@

num_colon.png: $(srcdir)/touchmap-extra2/num_colon.png
	convert -resize 100x100 $< $@

rock1sid.png: $(srcdir)/touchmap-extra2/rock1sid.tga
	convert -resize 100x100 $< $@

sb_rocket.png: $(srcdir)/touchmap-extra2/sb_rocket.png
	convert -resize 100x100 $< $@


sb_nails.png: $(srcdir)/touchmap-extra2/sb_nails.png
	convert -resize 100x100 $< $@

hellknight.png: $(srcdir)/images/hellknight.png
	convert -resize 100x100 $< $@

tick.png: $(srcdir)/images/tick.png
	convert -resize 100x100 $< $@


doom3.png: $(srcdir)/images/doom3.png
	convert -resize 100x100 $< $@

.pnm.png:
	pnmscale -xsize=100 -ysize=100 $< > t.pnm
	pnmtopng t.pnm > $@
	$(RM) t.pnm

newimage.png: $(srcdir)/images/newimage.png
	convert $< t1.pnm
	pnmscale -xsize=100 -ysize=100 t1.pnm > t.pnm
	pnmtopng t.pnm > $@
	$(RM) t.pnm t1.pnm

wallh-bw.pnm: $(srcdir)/wallv-bw.ms
	groff -I$(srcdir) < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

wallv-bw.pnm: $(srcdir)/wallv-bw.ms
	groff -I$(srcdir) < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

wallh.pnm: $(srcdir)/wallh.ms
	groff -I$(srcdir) < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

wallv.pnm: $(srcdir)/wallv.ms
	groff -I$(srcdir) < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

doorh.pnm: $(srcdir)/doorh.ms
	groff -I$(srcdir) < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

doorv.pnm: $(srcdir)/doorv.ms
	groff -I$(srcdir) < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

doorh-bw.pnm: $(srcdir)/doorh-bw.ms
	groff -I$(srcdir) < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

doorv-bw.pnm: $(srcdir)/doorv-bw.ms
	groff -I$(srcdir) < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

hingeh.pnm: $(srcdir)/hingeh.ms
	groff -I$(srcdir) < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

hingev.pnm: $(srcdir)/hingeh.ms
	groff -I$(srcdir) < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm | pnmrotate 90 > $@
	$(RM) t.ps t.pnm

release: force
	pwd
	echo pge-`sed -e '/version_string/!d' \
          -e 's/[^0-9.]*\([0-9.]*\).*/\1/' -e q $(srcdir)/version.c` > .fname
	-rm -rf `cat .fname`
	mkdir `cat .fname`
	dst=`cat .fname`; for f in $(DISTFILES); do \
           cp -rp $(srcdir)/$$f $$dst/$$f ; \
        done
	tar --gzip -chf `cat .fname`.tar.gz `cat .fname`
	-rm -rf `cat .fname` .fname

force:
