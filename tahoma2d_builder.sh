#!/bin/bash

echo ">>> Create build"
if ! [ -d $(dirname "$0")/build ]
then
	mkdir $(dirname "$0")/build
fi

HOME_PATH=$(dirname "$0")/build
cd $HOME_PATH
if ! [ "$EUID" -ne 0 ];
then 
	if ! [ -d $HOME_PATH/tahoma2d ];
	then	
		echo ">>> Download Tahoma2D repo"
		git clone https://github.com/tahoma2d/tahoma2d.git
		chmod -R ugo+rwx tahoma2d
	else
		echo ">>> Directory is exists"
	fi
	
	echo ">>> Install packages .rpm"
	dnf install -y gcc gcc-c++ automake git cmake boost boost-devel SuperLU SuperLU-devel lz4-devel lzma lzo-devel libjpeg-turbo-devel libGLEW glew-devel freeglut-devel freeglut freetype-devel libpng-devel qt5-qtbase-devel qt5-qtsvg qt5-qtsvg-devel qt5-qtscript qt5-qtscript-devel qt5-qttools qt5-qttools-devel qt5-qtmultimedia-devel blas blas-devel json-c-devel libtool intltool make qt5-qtmultimedia libmypaint-devel qt5-qtserialport-devel-5.15.1-1.el7.x86_64 qt5-qttools-static-5.15.1-6.el7.x86_64 turbojpeg-devel-2.1.5-1.el7.x86_64 libdeflate-devel-1.19-1.el7.x86_64 
	
	echo ">>> Copu OpenCV.rpm"
	if ! [ -d $HOME_PATH/OpenCV ]
	then
		mkdir $HOME_PATH/OpenCV
	fi
	for item in opencv-4.6.0-7.el7.x86_64.rpm opencv-contrib-4.6.0-7.el7.x86_64.rpm opencv-core-4.6.0-7.el7.x86_64.rpm opencv-devel-4.6.0-7.el7.x86_64.rpm;
	do 
		if ! [ -e $HOME_PATH/OpenCV/$item ];
		then
			cd $HOME_PATH/OpenCV
			wget https://github.com/animeforge/tahoma2d-build-redos/releases/download/v1.5-beta-2024-10-27/$item
			cd ../
		fi
	done
	
	echo">>> Install OpenCV.rpm"
	dnf install -y $HOME_PATH/OpenCV/opencv-4.6.0-7.el7.x86_64.rpm $HOME_PATH/OpenCV/opencv-contrib-4.6.0-7.el7.x86_64.rpm $HOME_PATH/OpenCV/opencv-core-4.6.0-7.el7.x86_64.rpm $HOME_PATH/OpenCV/opencv-devel-4.6.0-7.el7.x86_64.rpm
	
	echo ">>> Tahoma2D assembly"
	cd tahoma2d/thirdparty/tiff-*
	./configure --with-pic --disable-jbig --disable-webp 
	make -j6
	cd ../../
	cd toonz
	mkdir build
	cd build
	cmake ../sources
	make -j6
	
	source /opt/qt515/bin/qt515-env.sh
	
	echo ">>> Temporary install of Tahoma2D"
	export BUILDDIR=$HOME_PATH/tahoma2d/toonz/build
	cd $BUILDDIR
	ldconfig
	
	echo ">>> Creating appDir"
	if [ -d $HOME_PATH/appdir ]
	then
	   rm -rf $HOME_PATH/appdir
	fi
	mkdir -p $HOME_PATH/appdir/usr

	echo ">>> Copy and configure Tahoma2D installation in appDir"
	cp -r /opt/tahoma2d/* $HOME_PATH/appdir/usr
	cp $HOME_PATH/appdir/usr/share/applications/*.desktop $HOME_PATH/appdir
	cp $HOME_PATH/appdir/usr/share/icons/hicolor/*/apps/*.png $HOME_PATH/appdir
	mv $HOME_PATH/appdir/usr/lib/tahoma2d/* $HOME_PATH/appdir/usr/lib
	rmdir $HOME_PATH/appdir/usr/lib/tahoma2d

	if [ -d ../../thirdparty/canon/Library ]
	then
	   echo ">>> Copying canon libraries"
	   cp -R ../../thirdparty/canon/Library/x86_64/* appdir/usr/lib
	fi

	echo ">>> Copying libghoto2 supporting directories"
	cp -r /usr/local/lib/libgphoto2 $HOME_PATH/appdir/usr/lib
	cp -r /usr/local/lib/libgphoto2_port $HOME_PATH/appdir/usr/lib

	rm $HOME_PATH/appdir/usr/lib/libgphoto2/print-camera-list
	find $HOME_PATH/appdir/usr/lib/libgphoto2* -name *.la -exec rm -f {} \;
	find $HOME_PATH/appdir/usr/lib/libgphoto2* -name *.so -exec patchelf --set-rpath '$ORIGIN/../..' {} \;

	cd $HOME_PATH/../
	cp -f tahoma2d $HOME_PATH/appdir/usr/bin/
	cd $HOME_PATH
	
	echo ">>> Creating Tahoma2D/Tahoma2D.AppImage"

	if [ ! -f linuxdeployqt*.AppImage ]
	then
	   wget -c "https://github.com/probonopd/linuxdeployqt/releases/download/continuous/linuxdeployqt-continuous-x86_64.AppImage"
	   chmod a+x linuxdeployqt*.AppImage
	fi

	export LD_LIBRARY_PATH=appdir/usr/lib
	./linuxdeployqt*.AppImage appdir/usr/bin/Tahoma2D -bundle-non-qt-libs -verbose=0 -always-overwrite -no-strip \
	   -executable=appdir/usr/bin/lzocompress \
	   -executable=appdir/usr/bin/lzodecompress \
	   -executable=appdir/usr/bin/tcleanup \
	   -executable=appdir/usr/bin/tcomposer \
	   -executable=appdir/usr/bin/tconverter \
	   -executable=appdir/usr/bin/tfarmcontroller \
	   -executable=appdir/usr/bin/tfarmserver 
	
	rm appdir/AppRun
	cp $HOME_PATH/../scripts/AppRun appdir
	chmod 775 $HOME_PATH/appdir/AppRun


	./linuxdeployqt*.AppImage appdir/usr/bin/Tahoma2D -appimage -no-strip 

	chmod -R ugo+rwx $HOME_PATH
	echo ">>> Start app Tahoma2D:"$HOME_PATH/Tahoma2D-x86_64.AppImage
else
	echo ">>> Run script from root"
fi
