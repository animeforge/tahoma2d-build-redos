

su - -c
dnf install gcc gcc-c++ automake git cmake boost boost-devel SuperLU SuperLU-devel lz4-devel lzma lzo-devel libjpeg-turbo-devel libGLEW glew-devel freeglut-devel freeglut freetype-devel libpng-devel qt5-qtbase-devel qt5-qtsvg qt5-qtsvg-devel qt5-qtscript qt5-qtscript-devel qt5-qttools qt5-qttools-devel qt5-qtmultimedia-devel blas blas-devel json-c-devel libtool intltool make qt5-qtmultimedia libmypaint-devel qt5-qtserialport-devel-5.15.1-1.el7.x86_64 qt5-qttools-static-5.15.1-6.el7.x86_64 turbojpeg-devel-2.1.5-1.el7.x86_64 libdeflate-devel-1.19-1.el7.x86_64 '/PATH/TO/OPENCV/opencv-4.6.0-7.el7.x86_64.rpm' '/PATH/TO/OPENCV/opencv-contrib-4.6.0-7.el7.x86_64.rpm' '/PATH/TO/OPENCV/opencv-core-4.6.0-7.el7.x86_64.rpm' '/PATH/TO/OPENCV/opencv-devel-4.6.0-7.el7.x86_64.rpm'



cd ~
mkdir -p $HOME/.config/Tahoma2D
cd ~
cp -r tahoma2d/stuff $HOME/.config/Tahoma2D/

cat << EOF > $HOME/.config/Tahoma2D/SystemVar.ini
[General]
TAHOMA2DROOT="$HOME/.config/Tahoma2D/stuff"
TAHOMA2DPROFILES="$HOME/.config/Tahoma2D/stuff/profiles"
TAHOMA2DCACHEROOT="$HOME/.config/Tahoma2D/stuff/cache"
TAHOMA2DCONFIG="$HOME/.config/Tahoma2D/stuff/config"
TAHOMA2DFXPRESETS="$HOME/.config/Tahoma2D/stuff/fxs"
TAHOMA2DLIBRARY="$HOME/.config/Tahoma2D/stuff/library"
TAHOMA2DPROFILES="$HOME/.config/Tahoma2D/stuff/profiles"
TAHOMA2DPROJECTS="$HOME/.config/Tahoma2D/stuff/projects"
TAHOMA2DROOT="$HOME/.config/Tahoma2D/stuff"
TAHOMA2DSTUDIOPALETTE="$HOME/.config/Tahoma2D/stuff/studiopalette"
EOF

cd tahoma2d/thirdparty/tiff-4.2.0
./configure --with-pic --disable-jbig --disable-webp 
make -j6
cd ../../
cd toonz
mkdir build
cd build
cmake ../sources
make -j6
