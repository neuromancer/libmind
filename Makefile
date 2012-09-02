SUBDIRS = src/io/text/mhyphen
     
.PHONY: subdirs $(SUBDIRS)
     
all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

clean: 
	$(MAKE) -C $(SUBDIRS) $@
