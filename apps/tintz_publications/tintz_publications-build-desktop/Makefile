#############################################################################
# Makefile for building: libtintz.so.1.0.0
# Generated by qmake (2.01a) (Qt 4.7.0) on: Wed Jan 12 13:46:24 2011
# Project:  ../tintz_publications/tintz_publications.pro
# Template: lib
# Command: /usr/bin/qmake-qt4 -spec /usr/share/qt4/mkspecs/linux-g++ -o Makefile ../tintz_publications/tintz_publications.pro
#############################################################################

####### Compiler, tools and options

CC            = gcc
CXX           = g++
DEFINES       = -DTINTZ_LIBRARY -DQT_NO_DEBUG -DQT_GUI_LIB -DQT_CORE_LIB -DQT_SHARED
CFLAGS        = -pipe -O2 -Wall -W -D_REENTRANT -fPIC $(DEFINES)
CXXFLAGS      = -pipe -O2 -Wall -W -D_REENTRANT -fPIC $(DEFINES)
INCPATH       = -I/usr/share/qt4/mkspecs/linux-g++ -I../tintz_publications -I/usr/include/qt4/QtCore -I/usr/include/qt4/QtGui -I/usr/include/qt4 -I/usr/include/qt4/QtTest -I. -I../tintz_publications -I.
LINK          = g++
LFLAGS        = -Wl,-O1 -shared -Wl,-soname,libtintz.so.1
LIBS          = $(SUBLIBS)  -L/usr/lib -lQtTest -lQtGui -lQtCore -lpthread 
AR            = ar cqs
RANLIB        = 
QMAKE         = /usr/bin/qmake-qt4
TAR           = tar -cf
COMPRESS      = gzip -9f
COPY          = cp -f
SED           = sed
COPY_FILE     = $(COPY)
COPY_DIR      = $(COPY) -r
STRIP         = strip
INSTALL_FILE  = install -m 644 -p
INSTALL_DIR   = $(COPY_DIR)
INSTALL_PROGRAM = install -m 755 -p
DEL_FILE      = rm -f
SYMLINK       = ln -f -s
DEL_DIR       = rmdir
MOVE          = mv -f
CHK_DIR_EXISTS= test -d
MKDIR         = mkdir -p

####### Output directory

OBJECTS_DIR   = ./

####### Files

SOURCES       = ../tintz_publications/main.cpp \
		../tintz_publications/fileformat.cpp \
		../tintz_publications/testguesstype.cpp \
		../tintz_publications/comicimages.cpp \
		../tintz_publications/testcomicimages.cpp moc_testguesstype.cpp \
		moc_comicimages.cpp \
		moc_testcomicimages.cpp
OBJECTS       = main.o \
		fileformat.o \
		testguesstype.o \
		comicimages.o \
		testcomicimages.o \
		moc_testguesstype.o \
		moc_comicimages.o \
		moc_testcomicimages.o
DIST          = /usr/share/qt4/mkspecs/common/g++.conf \
		/usr/share/qt4/mkspecs/common/unix.conf \
		/usr/share/qt4/mkspecs/common/linux.conf \
		/usr/share/qt4/mkspecs/qconfig.pri \
		/usr/share/qt4/mkspecs/modules/qt_webkit_version.pri \
		/usr/share/qt4/mkspecs/features/qt_functions.prf \
		/usr/share/qt4/mkspecs/features/qt_config.prf \
		/usr/share/qt4/mkspecs/features/exclusive_builds.prf \
		/usr/share/qt4/mkspecs/features/default_pre.prf \
		/usr/share/qt4/mkspecs/features/release.prf \
		/usr/share/qt4/mkspecs/features/default_post.prf \
		/usr/share/qt4/mkspecs/features/qtestlib.prf \
		/usr/share/qt4/mkspecs/features/warn_on.prf \
		/usr/share/qt4/mkspecs/features/qt.prf \
		/usr/share/qt4/mkspecs/features/unix/thread.prf \
		/usr/share/qt4/mkspecs/features/moc.prf \
		/usr/share/qt4/mkspecs/features/resources.prf \
		/usr/share/qt4/mkspecs/features/uic.prf \
		/usr/share/qt4/mkspecs/features/yacc.prf \
		/usr/share/qt4/mkspecs/features/lex.prf \
		/usr/share/qt4/mkspecs/features/include_source_dir.prf \
		../tintz_publications/tintz_publications.pro
QMAKE_TARGET  = tintz
DESTDIR       = 
TARGET        = libtintz.so.1.0.0
TARGETA       = libtintz.a
TARGETD       = libtintz.so.1.0.0
TARGET0       = libtintz.so
TARGET1       = libtintz.so.1
TARGET2       = libtintz.so.1.0

first: all
####### Implicit rules

.SUFFIXES: .o .c .cpp .cc .cxx .C

.cpp.o:
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o "$@" "$<"

.cc.o:
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o "$@" "$<"

.cxx.o:
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o "$@" "$<"

.C.o:
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o "$@" "$<"

.c.o:
	$(CC) -c $(CFLAGS) $(INCPATH) -o "$@" "$<"

####### Build rules

all: Makefile  $(TARGET)

$(TARGET):  $(OBJECTS) $(SUBLIBS) $(OBJCOMP)  
	-$(DEL_FILE) $(TARGET) $(TARGET0) $(TARGET1) $(TARGET2)
	$(LINK) $(LFLAGS) -o $(TARGET) $(OBJECTS) $(LIBS) $(OBJCOMP)
	-ln -s $(TARGET) $(TARGET0)
	-ln -s $(TARGET) $(TARGET1)
	-ln -s $(TARGET) $(TARGET2)



staticlib: $(TARGETA)

$(TARGETA):  $(OBJECTS) $(OBJCOMP) 
	-$(DEL_FILE) $(TARGETA) 
	$(AR) $(TARGETA) $(OBJECTS)

Makefile: ../tintz_publications/tintz_publications.pro  /usr/share/qt4/mkspecs/linux-g++/qmake.conf /usr/share/qt4/mkspecs/common/g++.conf \
		/usr/share/qt4/mkspecs/common/unix.conf \
		/usr/share/qt4/mkspecs/common/linux.conf \
		/usr/share/qt4/mkspecs/qconfig.pri \
		/usr/share/qt4/mkspecs/modules/qt_webkit_version.pri \
		/usr/share/qt4/mkspecs/features/qt_functions.prf \
		/usr/share/qt4/mkspecs/features/qt_config.prf \
		/usr/share/qt4/mkspecs/features/exclusive_builds.prf \
		/usr/share/qt4/mkspecs/features/default_pre.prf \
		/usr/share/qt4/mkspecs/features/release.prf \
		/usr/share/qt4/mkspecs/features/default_post.prf \
		/usr/share/qt4/mkspecs/features/qtestlib.prf \
		/usr/share/qt4/mkspecs/features/warn_on.prf \
		/usr/share/qt4/mkspecs/features/qt.prf \
		/usr/share/qt4/mkspecs/features/unix/thread.prf \
		/usr/share/qt4/mkspecs/features/moc.prf \
		/usr/share/qt4/mkspecs/features/resources.prf \
		/usr/share/qt4/mkspecs/features/uic.prf \
		/usr/share/qt4/mkspecs/features/yacc.prf \
		/usr/share/qt4/mkspecs/features/lex.prf \
		/usr/share/qt4/mkspecs/features/include_source_dir.prf \
		/usr/lib/libQtTest.prl \
		/usr/lib/libQtGui.prl \
		/usr/lib/libQtCore.prl
	$(QMAKE) -spec /usr/share/qt4/mkspecs/linux-g++ -o Makefile ../tintz_publications/tintz_publications.pro
/usr/share/qt4/mkspecs/common/g++.conf:
/usr/share/qt4/mkspecs/common/unix.conf:
/usr/share/qt4/mkspecs/common/linux.conf:
/usr/share/qt4/mkspecs/qconfig.pri:
/usr/share/qt4/mkspecs/modules/qt_webkit_version.pri:
/usr/share/qt4/mkspecs/features/qt_functions.prf:
/usr/share/qt4/mkspecs/features/qt_config.prf:
/usr/share/qt4/mkspecs/features/exclusive_builds.prf:
/usr/share/qt4/mkspecs/features/default_pre.prf:
/usr/share/qt4/mkspecs/features/release.prf:
/usr/share/qt4/mkspecs/features/default_post.prf:
/usr/share/qt4/mkspecs/features/qtestlib.prf:
/usr/share/qt4/mkspecs/features/warn_on.prf:
/usr/share/qt4/mkspecs/features/qt.prf:
/usr/share/qt4/mkspecs/features/unix/thread.prf:
/usr/share/qt4/mkspecs/features/moc.prf:
/usr/share/qt4/mkspecs/features/resources.prf:
/usr/share/qt4/mkspecs/features/uic.prf:
/usr/share/qt4/mkspecs/features/yacc.prf:
/usr/share/qt4/mkspecs/features/lex.prf:
/usr/share/qt4/mkspecs/features/include_source_dir.prf:
/usr/lib/libQtTest.prl:
/usr/lib/libQtGui.prl:
/usr/lib/libQtCore.prl:
qmake:  FORCE
	@$(QMAKE) -spec /usr/share/qt4/mkspecs/linux-g++ -o Makefile ../tintz_publications/tintz_publications.pro

dist: 
	@$(CHK_DIR_EXISTS) ../tintz_publications/.tmp/tintz1.0.0 || $(MKDIR) ../tintz_publications/.tmp/tintz1.0.0 
	$(COPY_FILE) --parents $(SOURCES) $(DIST) ../tintz_publications/.tmp/tintz1.0.0/ && $(COPY_FILE) --parents ../tintz_publications/fileformat.h ../tintz_publications/testguesstype.h ../tintz_publications/comicimages.h ../tintz_publications/testcomicimages.h ../tintz_publications/.tmp/tintz1.0.0/ && $(COPY_FILE) --parents ../tintz_publications/main.cpp ../tintz_publications/fileformat.cpp ../tintz_publications/testguesstype.cpp ../tintz_publications/comicimages.cpp ../tintz_publications/testcomicimages.cpp ../tintz_publications/.tmp/tintz1.0.0/ && (cd `dirname ../tintz_publications/.tmp/tintz1.0.0` && $(TAR) tintz1.0.0.tar tintz1.0.0 && $(COMPRESS) tintz1.0.0.tar) && $(MOVE) `dirname ../tintz_publications/.tmp/tintz1.0.0`/tintz1.0.0.tar.gz . && $(DEL_FILE) -r ../tintz_publications/.tmp/tintz1.0.0


clean:compiler_clean 
	-$(DEL_FILE) $(OBJECTS)
	-$(DEL_FILE) *~ core *.core


####### Sub-libraries

distclean: clean
	-$(DEL_FILE) $(TARGET) 
	-$(DEL_FILE) $(TARGET0) $(TARGET1) $(TARGET2) $(TARGETA)
	-$(DEL_FILE) Makefile


check: first

mocclean: compiler_moc_header_clean compiler_moc_source_clean

mocables: compiler_moc_header_make_all compiler_moc_source_make_all

compiler_moc_header_make_all: moc_testguesstype.cpp moc_comicimages.cpp moc_testcomicimages.cpp
compiler_moc_header_clean:
	-$(DEL_FILE) moc_testguesstype.cpp moc_comicimages.cpp moc_testcomicimages.cpp
moc_testguesstype.cpp: ../tintz_publications/fileformat.h \
		../tintz_publications/testguesstype.h
	/usr/bin/moc-qt4 $(DEFINES) $(INCPATH) ../tintz_publications/testguesstype.h -o moc_testguesstype.cpp

moc_comicimages.cpp: ../tintz_publications/fileformat.h \
		../tintz_publications/comicimages.h
	/usr/bin/moc-qt4 $(DEFINES) $(INCPATH) ../tintz_publications/comicimages.h -o moc_comicimages.cpp

moc_testcomicimages.cpp: ../tintz_publications/testcomicimages.h
	/usr/bin/moc-qt4 $(DEFINES) $(INCPATH) ../tintz_publications/testcomicimages.h -o moc_testcomicimages.cpp

compiler_rcc_make_all:
compiler_rcc_clean:
compiler_image_collection_make_all: qmake_image_collection.cpp
compiler_image_collection_clean:
	-$(DEL_FILE) qmake_image_collection.cpp
compiler_moc_source_make_all:
compiler_moc_source_clean:
compiler_uic_make_all:
compiler_uic_clean:
compiler_yacc_decl_make_all:
compiler_yacc_decl_clean:
compiler_yacc_impl_make_all:
compiler_yacc_impl_clean:
compiler_lex_make_all:
compiler_lex_clean:
compiler_clean: compiler_moc_header_clean 

####### Compile

main.o: ../tintz_publications/main.cpp ../tintz_publications/testguesstype.h \
		../tintz_publications/fileformat.h \
		../tintz_publications/testcomicimages.h \
		../tintz_publications/comicimages.h
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o main.o ../tintz_publications/main.cpp

fileformat.o: ../tintz_publications/fileformat.cpp ../tintz_publications/fileformat.h
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o fileformat.o ../tintz_publications/fileformat.cpp

testguesstype.o: ../tintz_publications/testguesstype.cpp ../tintz_publications/testguesstype.h \
		../tintz_publications/fileformat.h
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o testguesstype.o ../tintz_publications/testguesstype.cpp

comicimages.o: ../tintz_publications/comicimages.cpp ../tintz_publications/comicimages.h \
		../tintz_publications/fileformat.h
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o comicimages.o ../tintz_publications/comicimages.cpp

testcomicimages.o: ../tintz_publications/testcomicimages.cpp ../tintz_publications/testcomicimages.h \
		../tintz_publications/comicimages.h \
		../tintz_publications/fileformat.h
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o testcomicimages.o ../tintz_publications/testcomicimages.cpp

moc_testguesstype.o: moc_testguesstype.cpp 
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o moc_testguesstype.o moc_testguesstype.cpp

moc_comicimages.o: moc_comicimages.cpp 
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o moc_comicimages.o moc_comicimages.cpp

moc_testcomicimages.o: moc_testcomicimages.cpp 
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o moc_testcomicimages.o moc_testcomicimages.cpp

####### Install

install:   FORCE

uninstall:   FORCE

FORCE:

