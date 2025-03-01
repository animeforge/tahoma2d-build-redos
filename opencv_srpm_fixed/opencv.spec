%undefine __cmake_in_source_build
%bcond_without  tests
%bcond_without  extras
# linters are enabled by default if BUILD_DOCS OR BUILD_EXAMPLES
%bcond_without  linters
%bcond_with     ffmpeg
%bcond_without  gstreamer
%bcond_with     eigen2
%bcond_without  eigen3
%bcond_without  opencl
%bcond_without  tbb
%bcond_with     cuda
%bcond_with     xine
# Atlas need (missing: Atlas_CLAPACK_INCLUDE_DIR Atlas_CBLAS_LIBRARY Atlas_BLAS_LIBRARY Atlas_LAPACK_LIBRARY)
# LAPACK may use atlas or openblas since now it detect openblas, atlas is not used anyway, more info please
# check OpenCVFindLAPACK.cmake
%bcond_with     atlas
%bcond_without  openblas
%bcond_without  gdcm
%if 0%{?rhel} >= 8
%bcond_with     vtk
%else
%bcond_without  vtk
%endif

%ifarch x86_64
%bcond_without  libmfx
%bcond_without  va
%else
%bcond_with     libmfx
%endif
%ifarch %{java_arches}
%bcond_without  java
%else
%bcond_with  java
%endif

%bcond_without  vulkan

%define _lto_cflags %{nil}

# If _cuda_version is unset
%if 0%{!?_cuda_version:1} && 0%{?with_cuda:1}
%global _cuda_version 11.2
%global _cuda_rpm_version 11-2
%global _cuda_prefix /usr/local/cuda-%{_cuda_version}
%bcond_without dnn_cuda
%endif

Name:           opencv
Version:        4.6.0
%global javaver %(foo=%{version}; echo ${foo//./})
%global majorver %(foo=%{version}; a=(${foo//./ }); echo ${a[0]} )
%global minorver %(foo=%{version}; a=(${foo//./ }); echo ${a[1]} )
%global padding  %(digits=00; num=%{minorver}; echo ${digits:${#num}:${#digits}} )
%global abiver   %(echo %{majorver}%{padding}%{minorver} )
Release:        7%{?dist}
Summary:        Collection of algorithms for computer vision
# This is normal three clause BSD.
License:        BSD
URL:            https://opencv.org
# TO PREPARE TARBALLS FOR FEDORA
# Edit opencv-clean.sh and set VERSION, save file and run opencv-clean.sh
#
# Need to remove copyrighted lena.jpg images (rhbz#1295173)
# and SIFT/SURF (module xfeatures2d) from tarball, due to legal concerns.
#
Source0:        %{name}-clean-%{version}.tar.gz
Source1:        %{name}_contrib-clean-%{version}.tar.gz
%{?with_extras:
Source2:        %{name}_extra-clean-%{version}.tar.gz
}
Source3:        face_landmark_model.dat.xz
# from https://github.com/opencv/ade/archive/v0.1.1f.zip
Source4:        b624b995ec9c439cbc2e9e6ee940d3a2-v0.1.1f.zip
Source5:        xorg.conf

Patch0:         opencv-4.1.0-install_3rdparty_licenses.patch
Patch3:         opencv.python.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 2.6.3
BuildRequires:  chrpath
%{?with_cuda:
BuildRequires:  cuda-minimal-build-%{?_cuda_rpm_version}
BuildRequires:  pkgconfig(cublas-%{?_cuda_version})
BuildRequires:  pkgconfig(cufft-%{?_cuda_version})
BuildRequires:  pkgconfig(nppc-%{?_cuda_version})
%{?with_dnn_cuda:BuildRequires: libcudnn8-devel}
}
%{?with_eigen2:BuildRequires:  eigen2-devel}
%{?with_eigen3:BuildRequires:  eigen3-devel}
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
%if 0%{?fedora}
%ifnarch s390 s390x
BuildRequires:  libraw1394-devel
BuildRequires:  libdc1394-devel
%endif
%endif
BuildRequires:  jasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libGL-devel
BuildRequires:  libv4l-devel
BuildRequires:  OpenEXR-devel
%{?with_tbb:
BuildRequires:  tbb-devel
}
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
%{?with_linters:
BuildRequires:  pylint
BuildRequires:  python3-flake8
}
BuildRequires:  swig >= 1.3.24
%{?with_ffmpeg:BuildRequires:  ffmpeg-devel >= 0.4.9}
%if 0%{?fedora} || 0%{?rhel} > 7
%{?with_gstreamer:BuildRequires:  gstreamer1-devel gstreamer1-plugins-base-devel}
%else
%{?with_gstreamer:BuildRequires:  gstreamer-devel gstreamer-plugins-base-devel}
%endif
%{?with_xine:BuildRequires:  xine-lib-devel}
%{?with_opencl:BuildRequires:  opencl-headers}
BuildRequires:  libgphoto2-devel
BuildRequires:  libwebp-devel
BuildRequires:  tesseract-devel
BuildRequires:  protobuf-devel
BuildRequires:  gdal-devel
BuildRequires:  glog-devel
#BuildRequires:  doxygen
BuildRequires:  python3-beautifulsoup4
#for doc/doxygen/bib2xhtml.pl
#BuildRequires:  perl-open
BuildRequires:  gflags-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  libGL-devel
BuildRequires:  libGLU-devel
BuildRequires:  hdf5-devel
BuildRequires:  openjpeg2-devel
BuildRequires:  freetype-devel
BuildRequires:  harfbuzz-devel
# Module opencv_ovis disabled because of incompatible OGRE3D version < 1.10
# BuildRequires:  ogre-devel
%{?with_vtk:BuildRequires: vtk-devel}
%{?with_vtk:
  %{?with_java:
BuildRequires:  vtk-java
   }
}
%{?with_atlas:BuildRequires: atlas-devel}
#ceres-solver-devel push eigen3-devel and tbb-devel
%{?with_tbb:
  %{?with_eigen3:
# CERES support is disabled. Ceres Solver for reconstruction API is required.
# seems that ceres-solver is only needed for SFM algorithms but SFM algorithms are disabled because needs xfeatures2d
# BuildRequires:  ceres-solver-devel
  }
}
%{?with_openblas:
BuildRequires:  openblas-devel
BuildRequires:  blas-devel
BuildRequires:  lapack-devel
}
%{?with_gdcm:BuildRequires: gdcm-devel}
%{?with_libmfx:BuildRequires:  libmfx-devel}
%{?with_va:BuildRequires:   libva-devel}
%{?with_java:
BuildRequires:  ant
BuildRequires:  java-devel
}
%{?with_vulkan:BuildRequires:  vulkan-headers}
%if %{with tests}
BuildRequires:  xorg-x11-drv-dummy
BuildRequires:  mesa-dri-drivers
%endif

Requires:       opencv-core%{_isa} = %{version}-%{release}

%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.


%package        core
Summary:        OpenCV core libraries
Provides:       bundled(quirc) = 1.0
Obsoletes:      python2-%{name} < %{version}-%{release}

%description    core
This package contains the OpenCV C/C++ core libraries.


%package        devel
Summary:        Development files for using the OpenCV library
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       %{name}-contrib%{_isa} = %{version}-%{release}

%description    devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that
will use the OpenCV library. You should consider installing opencv-doc
package.


%package        doc
Summary:        Documentation files
Requires:       opencv-devel = %{version}-%{release}
# Doc dependes on architecture, specifically whether the va_intel sample is installed depends on HAVE_VA
# BuildArch:      noarch
Provides:       %{name}-devel-docs = %{version}-%{release}
Obsoletes:      %{name}-devel-docs < %{version}-%{release}

%description    doc
This package contains the OpenCV documentation, samples and examples programs.


%package        -n python3-opencv
Summary:        Python3 bindings for apps which use OpenCV
Requires:       opencv%{_isa} = %{version}-%{release}
Requires:       python3-numpy
%{?%py_provides:%py_provides python3-%{name}}

%description    -n python3-opencv
This package contains Python3 bindings for the OpenCV library.


%package    java
Summary:    Java bindings for apps which use OpenCV
Requires:   java-headless
Requires:   javapackages-filesystem
Requires:   %{name}-core%{_isa} = %{version}-%{release}

%description java
This package contains Java bindings for the OpenCV library.


%package        contrib
Summary:        OpenCV contributed functionality

%description    contrib
This package is intended for development of so-called "extra" modules, contributed
functionality. New modules quite often do not have stable API, and they are not
well-tested. Thus, they shouldn't be released as a part of official OpenCV
distribution, since the library maintains binary compatibility, and tries
to provide decent performance and stability.

%prep
%setup -q -a1 %{?with_extras:-a2}
%if 1
# we don't use pre-built contribs except quirc
pushd 3rdparty
shopt -s extglob
#rm -r !(openexr|openvx|quirc)
rm -r !(openvx|quirc)
shopt -u extglob
popd &>/dev/null
%endif

%patch0 -p1 -b .install_3rdparty_licenses
%patch3 -p1 -b .python_install_binary

pushd %{name}_contrib-%{version}
#patch1 -p1 -b .install_cvv
popd

# Install face_landmark_model
mkdir -p .cache/data
install -pm 0644 %{SOURCE3} .cache/data
pushd .cache/data
  xz -d face_landmark_model.dat.xz
  mv face_landmark_model.dat 7505c44ca4eb54b4ab1e4777cb96ac05-face_landmark_model.dat
popd

# Install ADE, needed for opencv_gapi
mkdir -p .cache/ade
install -pm 0644 %{SOURCE4} .cache/ade/

%build
# enabled by default if libraries are presents at build time:
# GTK, GSTREAMER, 1394, V4L, eigen3
# non available on Fedora: FFMPEG, XINE
# disabling IPP because it is closed source library from intel

%cmake \
 -DCV_TRACE=OFF \
 -DWITH_IPP=OFF \
 -DWITH_ITT=OFF \
 -DWITH_QT=ON \
 -DWITH_OPENGL=ON \
%if ! %{with tests}
 -DBUILD_TESTS=OFF \
%endif
 -DOpenGL_GL_PREFERENCE=GLVND \
 -DWITH_GDAL=ON \
 -DWITH_OPENEXR=ON \
 -DCMAKE_SKIP_RPATH=ON \
 -DWITH_CAROTENE=OFF \
%ifarch x86_64 %{ix86}
 -DCPU_BASELINE=SSE2 \
%endif
 -DCMAKE_BUILD_TYPE=ReleaseWithDebInfo \
 %{?with_java: -DBUILD_opencv_java=ON \
 -DOPENCV_JAR_INSTALL_PATH=%{_jnidir} } \
 %{!?with_java: -DBUILD_opencv_java=OFF } \
 %{?with_tbb: -DWITH_TBB=ON } \
 %{!?with_gstreamer: -DWITH_GSTREAMER=OFF } \
 %{!?with_ffmpeg: -DWITH_FFMPEG=OFF } \
 %{?with_cuda: \
 -DWITH_CUDA=ON \
 -DCUDA_TOOLKIT_ROOT_DIR=%{?_cuda_prefix} \
 -DCUDA_VERBOSE_BUILD=ON \
 -DCUDA_PROPAGATE_HOST_FLAGS=OFF \
 -DCUDA_NVCC_FLAGS="-Xcompiler -fPIC" \
 %{?with_dnn_cuda:-DOPENCV_DNN_CUDA=ON} \
 } \
 %{!?with_xine: -DWITH_XINE=OFF } \
 -DBUILD_DOCS=ON \
 -DBUILD_EXAMPLES=ON \
 -DBUILD_opencv_python2=OFF \
 -DINSTALL_C_EXAMPLES=ON \
 -DINSTALL_PYTHON_EXAMPLES=ON \
 -DPYTHON3_EXECUTABLE=%{__python3} \
 -DPYTHON3_PACKAGES_PATH=%{python3_sitearch} \
 -DOPENCV_GENERATE_SETUPVARS=OFF \
 %{!?with_linters: \
 -DENABLE_PYLINT=OFF \
 -DENABLE_FLAKE8=OFF \
 } \
 -DBUILD_PROTOBUF=OFF \
 -DPROTOBUF_UPDATE_FILES=ON \
%{?with_opencl: -DOPENCL_INCLUDE_DIR=%{_includedir}/CL } \
%{!?with_opencl: -DWITH_OPENCL=OFF } \
 -DOPENCV_EXTRA_MODULES_PATH=opencv_contrib-%{version}/modules \
 -DWITH_LIBV4L=ON \
 -DWITH_OPENMP=ON \
 -DOPENCV_CONFIG_INSTALL_PATH=%{_lib}/cmake/OpenCV \
 -DOPENCV_GENERATE_PKGCONFIG=ON \
%{?with_extras: -DOPENCV_TEST_DATA_PATH=opencv_extra-%{version}/testdata} \
 %{?with_gdcm: -DWITH_GDCM=ON } \
 %{?with_libmfx: -DWITH_MFX=ON } \
 %{?with_va: -DWITH_VA=ON } \
 %{!?with_vtk: -DWITH_VTK=OFF} \
 %{?with_vulkan: -DWITH_VULKAN=ON -DVULKAN_INCLUDE_DIRS=%{_includedir}/vulkan }

%cmake_build


%install
%cmake_install

rm -rf %{buildroot}%{_datadir}/OpenCV/licenses/
%if %{with java}
ln -s -r %{buildroot}%{_jnidir}/libopencv_java%{javaver}.so %{buildroot}%{_jnidir}/libopencv_java.so
ln -s -r %{buildroot}%{_jnidir}/opencv-%{javaver}.jar %{buildroot}%{_jnidir}/opencv.jar
%endif

# For compatibility with existing opencv.pc application
%{!?without_compat_openvc_pc:
  ln -s opencv4.pc %{buildroot}%{_libdir}/pkgconfig/opencv.pc
}


%check
# Check fails since we don't support most video
# read/write capability and we don't provide a display
# ARGS=-V increases output verbosity
#ifnarch ppc64
%if %{with tests}
    cp %SOURCE5 .
    if [ -x /usr/libexec/Xorg ]; then
       Xorg=/usr/libexec/Xorg
    else
       Xorg=/usr/libexec/Xorg.bin
    fi
    $Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xorg.log -config ./xorg.conf -configdir . :99 &
    export DISPLAY=:99
    LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/build/lib:$LD_LIBARY_PATH %ctest || :
%endif
#endif


%ldconfig_scriptlets core

%ldconfig_scriptlets contrib

%ldconfig_scriptlets java

%files
%doc README.md
%{_bindir}/opencv_*
%dir %{_datadir}/opencv4
%{_datadir}/opencv4/haarcascades
%{_datadir}/opencv4/lbpcascades
%{_datadir}/opencv4/valgrind*
%{_datadir}/opencv4/quality

%files core
%license LICENSE
%{_datadir}/licenses/opencv4/
%{_libdir}/libopencv_calib3d.so.{%{abiver},%{version}}
%{_libdir}/libopencv_core.so.{%{abiver},%{version}}
%{_libdir}/libopencv_dnn.so.{%{abiver},%{version}}
%{_libdir}/libopencv_features2d.so.{%{abiver},%{version}}
%{_libdir}/libopencv_flann.so.{%{abiver},%{version}}
%{_libdir}/libopencv_gapi.so.{%{abiver},%{version}}
%{_libdir}/libopencv_highgui.so.{%{abiver},%{version}}
%{_libdir}/libopencv_imgcodecs.so.{%{abiver},%{version}}
%{_libdir}/libopencv_imgproc.so.{%{abiver},%{version}}
%{_libdir}/libopencv_ml.so.{%{abiver},%{version}}
%{_libdir}/libopencv_objdetect.so.{%{abiver},%{version}}
%{_libdir}/libopencv_photo.so.{%{abiver},%{version}}
%{_libdir}/libopencv_stitching.so.{%{abiver},%{version}}
%{_libdir}/libopencv_video.so.{%{abiver},%{version}}
%{_libdir}/libopencv_videoio.so.{%{abiver},%{version}}

%files devel
%dir %{_includedir}/opencv4
%{_includedir}/opencv4/opencv2
%{_libdir}/lib*.so
%{!?without_compat_openvc_pc:
%{_libdir}/pkgconfig/opencv.pc
}
%{_libdir}/pkgconfig/opencv4.pc
%{_libdir}/cmake/OpenCV/*.cmake

%files doc
%{_datadir}/opencv4/samples

%files -n python3-opencv
%{python3_sitearch}/cv2

%if %{with java}
%files java
%{_jnidir}/libopencv_java%{javaver}.so
%{_jnidir}/opencv-%{javaver}.jar
%{_jnidir}/libopencv_java.so
%{_jnidir}/opencv.jar
%endif

%files contrib
%{_libdir}/libopencv_alphamat.so.{%{abiver},%{version}}
%{_libdir}/libopencv_aruco.so.{%{abiver},%{version}}
%{_libdir}/libopencv_bgsegm.so.{%{abiver},%{version}}
%{_libdir}/libopencv_barcode.so.{%{abiver},%{version}}
%{_libdir}/libopencv_bioinspired.so.{%{abiver},%{version}}
%{_libdir}/libopencv_ccalib.so.{%{abiver},%{version}}
%{?with_cuda:
%{_libdir}/libopencv_cuda*.so.{%{abiver},%{version}}
%{_libdir}/libopencv_cudev.so.{%{abiver},%{version}}
}
%{_libdir}/libopencv_cvv.so.{%{abiver},%{version}}
%{_libdir}/libopencv_datasets.so.{%{abiver},%{version}}
%{_libdir}/libopencv_dnn_objdetect.so.{%{abiver},%{version}}
%{_libdir}/libopencv_dnn_superres.so.{%{abiver},%{version}}
%{_libdir}/libopencv_dpm.so.{%{abiver},%{version}}
%{_libdir}/libopencv_face.so.{%{abiver},%{version}}
%{_libdir}/libopencv_freetype.so.{%{abiver},%{version}}
%{_libdir}/libopencv_fuzzy.so.{%{abiver},%{version}}
%{_libdir}/libopencv_hdf.so.{%{abiver},%{version}}
%{_libdir}/libopencv_hfs.so.{%{abiver},%{version}}
%{_libdir}/libopencv_img_hash.so.{%{abiver},%{version}}
%{_libdir}/libopencv_intensity_transform.so.{%{abiver},%{version}}
%{_libdir}/libopencv_line_descriptor.so.{%{abiver},%{version}}
%{_libdir}/libopencv_mcc.so.{%{abiver},%{version}}
%{_libdir}/libopencv_optflow.so.{%{abiver},%{version}}
%{_libdir}/libopencv_phase_unwrapping.so.{%{abiver},%{version}}
%{_libdir}/libopencv_plot.so.{%{abiver},%{version}}
%{_libdir}/libopencv_quality.so.{%{abiver},%{version}}
%{_libdir}/libopencv_rapid.so.{%{abiver},%{version}}
%{_libdir}/libopencv_reg.so.{%{abiver},%{version}}
%{_libdir}/libopencv_rgbd.so.{%{abiver},%{version}}
%{_libdir}/libopencv_saliency.so.{%{abiver},%{version}}
%{_libdir}/libopencv_shape.so.{%{abiver},%{version}}
%{_libdir}/libopencv_stereo.so.{%{abiver},%{version}}
%{_libdir}/libopencv_structured_light.so.{%{abiver},%{version}}
%{_libdir}/libopencv_superres.so.{%{abiver},%{version}}
%{_libdir}/libopencv_surface_matching.so.{%{abiver},%{version}}
%{_libdir}/libopencv_text.so.{%{abiver},%{version}}
%{_libdir}/libopencv_tracking.so.{%{abiver},%{version}}
%{_libdir}/libopencv_videostab.so.{%{abiver},%{version}}
%if %{with vtk}
%{_libdir}/libopencv_viz.so.{%{abiver},%{version}}
%endif
%{_libdir}/libopencv_wechat_qrcode.so.{%{abiver},%{version}}
%{_libdir}/libopencv_ximgproc.so.{%{abiver},%{version}}
%{_libdir}/libopencv_xobjdetect.so.{%{abiver},%{version}}
%{_libdir}/libopencv_xphoto.so.{%{abiver},%{version}}

%changelog
* Wed Sep 28 2022 Tom Rix <trix@redhat.com> - 4.6.0-7
- Remove Unicap

* Fri Jul 29 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.6.0-6
- BR vte-java only on %%java_arches

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Sandro Mani <manisandro@gmail.com> - 4.6.0-4
- Rebuild (tesseract)

* Wed Jul 06 2022 Sérgio Basto <sergio@serjux.com> - 4.6.0-3
- (#2104082) only build Java sub package on arches that java is supported

* Mon Jun 20 2022 Sérgio Basto <sergio@serjux.com> - 4.6.0-2
- Rebuilt for Python 3.11 (is just arrived to rawhide)

* Fri Jun 17 2022 Sérgio Basto <sergio@serjux.com> - 4.6.0-1
- Update opencv to 4.6.0 (#2094603)
- Remove hack to keep old so version
- Adapt spec to new so version ${OPENCV_VERSION_MAJOR}${OPENCV_VERSION_MINOR_2DIGITS}
  and drop OPENCV_VERSION_PATCH

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 4.5.5-9
- Rebuilt for Python 3.11

* Sat May 21 2022 Sandro Mani <manisandro@gmail.com> - 4.5.5-8
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Sun Mar 20 2022 Sérgio Basto <sergio@serjux.com> - 4.5.5-7
- Switch to new Python loader, doesn't fix rhbz #2054951 but can be a step

* Thu Mar 10 2022 Sandro Mani <manisandro@gmail.com> - 4.5.5-6
- Rebuild for tesseract 5.1.0

* Tue Feb 15 2022 Sérgio Basto <sergio@serjux.com> - 4.5.5-5
- The upstream fix https://github.com/opencv/opencv/pull/21614
  and remove the previous workaround

* Sun Feb 13 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.5.5-4
- Disable some altivec vectorization optimization on ppc64le (bug 2051193)

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 4.5.5-3
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 27 2021 Sérgio Basto <sergio@serjux.com> - 4.5.5-1
- Update opencv to 4.5.5 (#2035628)

* Sun Dec 19 2021 Sandro Mani <manisandro@gmail.com> - 4.5.4-8
- Rebuild (tesseract)

* Tue Dec 14 2021 Sandro Mani <manisandro@gmail.com> - 4.5.4-7
- Rebuild (tesseract)

* Mon Nov 22 2021 Orion Poplawski <orion@nwra.com> - 4.5.4-6
- Rebuild for hdf5 1.12.1

* Thu Nov 11 2021 Sandro Mani <manisandro@gmail.com> - 4.5.4-5
- Rebuild (gdal)

* Sat Nov 06 2021 Adrian Reber <adrian@lisas.de> - 4.5.4-4
- Rebuilt for protobuf 3.19.0

* Fri Nov 05 2021 Adrian Reber <adrian@lisas.de> - 4.5.4-3
- Rebuilt for protobuf 3.19.0

* Mon Oct 25 2021 Adrian Reber <adrian@lisas.de> - 4.5.4-2
- Rebuilt for protobuf 3.18.1

* Sun Oct 10 2021 Sérgio Basto <sergio@serjux.com> - 4.5.4-1
- Update to 4.5.4

* Fri Aug 20 2021 Richard Shaw <hobbes1069@gmail.com> - 4.5.3-6
- Rebuild for OpenEXR/Imath 3.1.

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 4.5.3-5
- Rebuild for hdf5 1.10.7

* Sat Jul 31 2021 Richard Shaw <hobbes1069@gmail.com> - 4.5.3-4
- Rebuild for OpenEXR/Imath 3.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Richard Shaw <hobbes1069@gmail.com> - 4.5.3-2
- Rebuild for openexr 3.

* Thu Jul 15 2021 Sérgio Basto <sergio@serjux.com> - 4.5.3-1
- Update to 4.5.3

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.5.2-6
- Rebuilt for Python 3.10

* Fri May 21 2021 Sandro Mani <manisandro@gmail.com> - 4.5.2-5
- Rebuild (gdal)

* Thu May 20 2021 Richard Shaw <hobbes1069@gmail.com> - 4.5.2-4
- Rebuild for gdal 3.3.0.

* Fri May 07 2021 Sandro Mani <manisandro@gmail.com> - 4.5.2-3
- Rebuild (gdal)

* Thu Apr 29 2021 Sérgio Basto <sergio@serjux.com> - 4.5.2-2
- Upstream fixed GCC11 issues, so we can re-enable the tests

* Sat Apr 03 2021 Nicolas Chauvet <kwizart@gmail.com> - 4.5.2-1
- Update to 4.5.2

* Wed Mar 31 2021 Nicolas Chauvet <kwizart@gmail.com> - 4.5.1-8
- Disable tests for now

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 4.5.1-7
- Rebuilt for removed libstdc++ symbol (#1937698)

* Wed Feb 10 2021 Jiri Kucera <jkucera@redhat.com> - 4.5.1-6
- Fix file lists
  Based on comparison of `opencv-4.5.1/modules/` and
  `opencv-4.5.1/opencv_contrib-4.5.1/modules/`, move some *.so's between core
  and contrib rpms

* Sun Jan 31 2021 Orion Poplawski <orion@nwra.com> - 4.5.1-5
- Rebuild for VTK 9

* Wed Jan 27 2021 Tomas Popela <tpopela@redhat.com> - 4.5.1-4
- Drop unused BR on SFML and disable VTK support on RHEL 8+

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 14:20:57 CET 2021 Adrian Reber <adrian@lisas.de> - 4.5.1-2
- Rebuilt for protobuf 3.14

* Sat Jan 02 2021 Sérgio Basto <sergio@serjux.com> - 4.5.1-1
- Update to 4.5.1

* Fri Jan 01 2021 Richard Shaw <hobbes1069@gmail.com> - 4.5.0-4
- Rebuild for OpenEXR 2.5.3.

* Sat Dec  5 2020 Jeff Law <law@redhat.com> - 4.5.0-3
- Fix missing #include for gcc-11

* Fri Nov  6 22:47:45 CET 2020 Sandro Mani <manisandro@gmail.com> - 4.5.0-2
- Rebuild (proj, gdal)

* Thu Oct 15 2020 Sérgio Basto <sergio@serjux.com> - 4.5.0-1
- Update 4.5.0

* Wed Oct 07 2020 Sérgio Basto <sergio@serjux.com> - 4.4.0-1
- Update 4.4.0
- opencv_vulkan.patch already applied in upstream

* Thu Sep 24 2020 Adrian Reber <adrian@lisas.de> - 4.3.0-9
- Rebuilt for protobuf 3.13

* Fri Jul 24 2020 Nicolas Chauvet <kwizart@gmail.com> - 4.3.0-8
- Rebuilt
- Fix cmake build
- Disable LTO on ppc64le
- Add undefine __cmake_in_source_build to allow build on Fedora < 33

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 4.3.0-7
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Fri Jun 26 2020 Orion Poplawski <orion@nwra.com> - 4.3.0-6
- Rebuild for hdf5 1.10.6

* Tue Jun 23 2020 Adrian Reber <adrian@lisas.de> - 4.3.0-5
- Rebuilt for protobuf 3.12

* Sun Jun 21 2020 Sérgio Basto <sergio@serjux.com> - 4.3.0-4
- Readd flake8 build requirement
- Fix build because pangox has been retired for F33 so we need remove the BR
  gtkglext
- Also remove all gtk stuff (we have to choose between gtk or qt when build opencv)
  https://answers.opencv.org/question/215066/gtk-or-qt-when-build-opencv/
- Doxygen requires gtk2, disabling for now

* Sun Jun 14 2020 Adrian Reber <adrian@lisas.de>
- Rebuilt for protobuf 3.12

* Tue Jun 02 2020 Orion Poplawski <orion@nwra.com> - 4.3.0-3
- Run tests

* Tue Jun 02 2020 Orion Poplawski <orion@nwra.com> - 4.3.0-2
- Add upstream patches for VTK 9.0 support (bz#1840977)

* Thu May 28 2020 Nicolas Chauvet <kwizart@gmail.com> - 4.3.0-1
- Update to 4.3.0

* Thu May 28 2020 Charalampos Stratakis <cstratak@redhat.com> - 4.2.0-9
- Remove flake8 build requirement

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.2.0-8
- Rebuilt for Python 3.9

* Thu May 21 2020 Sandro Mani <manisandro@gmail.com> - 4.2.0-7
- Rebuild (gdal)

* Fri May 08 2020 Nicolas Chauvet <kwizart@gmail.com> - 4.2.0-6
- Drop compat symlink for includes - rhbz#1830266

* Thu Mar 26 2020 Nicolas Chauvet <kwizart@gmail.com> - 4.2.0-5
- Add without_compat_opencv_pc with conditional - rhbz#1816439

* Tue Mar 03 2020 Sandro Mani <manisandro@gmail.com> - 4.2.0-4
- Rebuild (gdal)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 29 2020 Nicolas Chauvet <kwizart@gmail.com> - 4.2.0-2
- Backport patch for ppc64le

* Tue Dec 31 2019 Nicolas Chauvet <kwizart@gmail.com> - 4.2.0-1
- Update to 4.2.0

* Sat Dec 28 2019 Sandro Mani <manisandro@gmail.com> - 4.1.2-3
- Rebuild (tesseract)

* Thu Dec 19 2019 Orion Poplawski <orion@nwra.com> - 4.1.2-2
- Rebuild for protobuf 3.11

* Thu Oct 17 2019 Nicolas Chauvet <kwizart@gmail.com> - 4.1.2-1.1
- Fix include path
- Drop CPU baseline to SSE2 for x86
- Add missing directory ownership
- Add symlinks for compatibility with older versions
- Restore deprecated headers for compat

* Sat Oct 12 2019 Nicolas Chauvet <kwizart@gmail.com> - 4.1.2-1
- Update to 4.1.2

* Fri Sep 13 2019 Nicolas Chauvet <kwizart@gmail.com> - 4.1.1-1
- Update to 4.1.1

* Fri Sep 13 2019 Sérgio Basto <sergio@serjux.com> - 4.1.0-1
- Update opencv to 4.1.0

* Fri Sep 13 2019 Christopher N. Hesse <raymanfx@gmail.com> - 4.1.0-0
- Enable vulkan compute backend

* Fri Sep 13 2019 Sérgio Basto <sergio@serjux.com> - 3.4.6-9
- Reenable pylint and vtk, they are working now.
* Wed Sep 11 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.6-8
- F-32: remove vtk gcdm dependency for now because they have broken dependency
  (bug 1751406)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.4.6-7
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Jerry James <loganjerry@gmail.com> - 3.4.6-5
- Rebuild for coin-or package updates

* Tue Jun 25 2019 Sérgio Basto <sergio@serjux.com> - 3.4.6-4
- cmake: use relative PATH on OPENCV_CONFIG_INSTALL_PATH, fixes rhbz #1721876
- cmake: don't set ENABLE_PKG_CONFIG

* Wed Jun 12 2019 Sérgio Basto <sergio@serjux.com> - 3.4.6-3
- Remove Obsoletes/Provides libopencv_java.so and use OPENCV_JAR_INSTALL_PATH

* Sun Jun 09 2019 Sérgio Basto <sergio@serjux.com> - 3.4.6-2
- Fix cmakes location
- add BR: python3-beautifulsoup4

* Thu May 23 2019 Sérgio Basto <sergio@serjux.com> - 3.4.6-1
- Update to 3.4.6

* Mon May 20 2019 Sérgio Basto <sergio@serjux.com> - 3.4.4-10
- Try improve Java Bindings

* Sun May 12 2019 Sérgio Basto <sergio@serjux.com> - 3.4.4-9
- Enable Java Bindings (contribution of Ian Wallace)
- Obsoletes python2-opencv to fix upgrade path

* Wed Apr 10 2019 Richard Shaw <hobbes1069@gmail.com> - 3.4.4-8
- Rebuild for OpenEXR 2.3.0.

* Mon Mar 18 2019 Orion Poplawski <orion@nwra.com>
- Rebuild for vtk 8.2

* Sun Mar 03 2019 Sérgio Basto <sergio@serjux.com> - 3.4.4-6
- Reenable build with gdcm
- Opencl is fixed for ppc64le on F30

* Thu Feb 21 2019 Josef Ridky <jridky@redhat.com> - 3.4.4-5
- build without gdcm to fix FTBFS in F30+ (#1676289)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.4.4-3
- Subpackage python2-opencv has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Dec 03 2018 Sérgio Basto <sergio@serjux.com> - 3.4.4-2
- Add the correct and upstreamed fix for support_YV12_too, pull request 13351
  which is merged

* Sat Dec 01 2018 Sérgio Basto <sergio@serjux.com> - 3.4.4-1
- Update to 3.4.4

* Wed Nov 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.4.3-7
- Rebuild for protobuf 3.6

* Tue Nov 13 2018 Sandro Mani <manisandro@gmail.com> - 3.4.3-6
- Rebuild (tesseract)

* Tue Oct 30 2018 Sérgio Basto <sergio@serjux.com> - 3.4.3-5
- Enable vtk should work with vtk-8.1.1
- Add BR python Flake8

* Tue Oct 23 2018 Felix Kaechele <heffer@fedoraproject.org> - 3.4.3-4
- enable building of dnn

* Sat Oct 13 2018 Jerry James <loganjerry@gmail.com> - 3.4.3-3
- Rebuild for tbb 2019_U1

* Sun Sep 30 2018 Sérgio Basto <sergio@serjux.com> - 3.4.3-2
- Use GLVND libraries for OpenGL and GLX, setting OpenGL_GL_PREFERENCE=GLVND

* Wed Sep 26 2018 Sérgio Basto <sergio@serjux.com> - 3.4.3-1
- Update to 3.4.3
- Fix build on arm and s390x

* Wed Sep 26 2018 Sérgio Basto <sergio@serjux.com> - 3.4.2-1
- Update to 3.4.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Sérgio Basto <sergio@serjux.com> - 3.4.1-5
- Small fix to build with Pyhton-3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.4.1-4
- Rebuilt for Python 3.7

* Mon Mar 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.4.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Mar 08 2018 Sérgio Basto <sergio@serjux.com> - 3.4.1-2
- Enable VA
- Do not use -f on rm because it silences errors
- Opencv sub-package don't need ldconfig because don't have any so

* Thu Mar 01 2018 Josef Ridky <jridky@redhat.com> - 3.4.1-1
- Spec clean up (remove Group tag, add ldconfig scriptlets, escape macros in comments)
- Remove unused patch
- Add gcc and gcc-c++ requirements
- Rebase to version 3.4.1

* Sun Feb 18 2018 Sérgio Basto <sergio@serjux.com> - 3.3.1-7
- Rebuild for gdcm-2.8

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.3.1-6
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Sérgio Basto <sergio@serjux.com> - 3.3.1-4
- Enable Pylint
- Enable Clp (COIN-OR Linear Program Solver)
- Enable VA (Video Acceleration API for Linux)
- Enable OpenMP
- Provides and obsoletes for opencv-devel-docs
- BuildRequires perl-local do generate documentation without errors

* Thu Jan 25 2018 Sérgio Basto <sergio@serjux.com> - 3.3.1-3
- Rename sub-package opencv-python3 to python3-opencv and other minor fixes in
  python packaging
- Generate documentation
- Rename sub-package devel-docs to doc
- Cleanup some comments from opencv 2.4 packaging

* Wed Jan 24 2018 Troy Dawson <tdawson@redhat.com> - 3.3.1-2
- Update conditionals

* Tue Nov 14 2017 Sérgio Basto <sergio@serjux.com> - 3.3.1-1
- Update to 3.3.1
- Fix WARNING: Option ENABLE_SSE='OFF' is deprecated and should not be used anymore
-          Behaviour of this option is not backward compatible
-          Refer to 'CPU_BASELINE'/'CPU_DISPATCH' CMake options documentation
- Fix WARNING: Option ENABLE_SSE2='OFF' is deprecated and should not be used anymore
-          Behaviour of this option is not backward compatible
-          Refer to 'CPU_BASELINE'/'CPU_DISPATCH' CMake options documentation
- Update opencv to 3.3.0
- Patch3 is already in source code
- Fix WARNING: Option ENABLE_SSE3='OFF' is deprecated and should not be used anymore
- Enable openblas
- Add conditonal to build with_gdcm
- Disable "Intel ITT support" because source is in 3rdparty/ directory

* Sat Oct 28 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-13
- Require python3-numpy instead numpy for opencv-python3 (#1504555)

* Sat Sep 02 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-12
- Fix 2 rpmlint errors

* Sat Sep 02 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-11
- Enable libv4l1 to fix open a video (#1487816)

* Mon Aug 28 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-10
- Better conditionals to enable openni only available in ix86, x86_64 and arm

* Sun Aug 20 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-9
- Enable openni.
- Enable eigen3 except in ppc64le because fails to build in OpenCL headers.
- Documented why is not enabled atlas, openblas and vtk.

* Sun Aug 20 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-8
- Reenable gstreamer
- Remove architecture checks for tbb and enable it, inspired on (#1262788)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.0-7
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.0-6
- Python 2 binary package renamed to python2-opencv
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Orion Poplawski <orion@cora.nwra.com> - 3.2.0-3
- Rebuild for protobuf 3.3.1

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon Feb 27 2017 Josef Ridky <jridky@redhat.com> - 3.2.0-1
- Rebase to the latest version (3.2.0) - #1408880
- Remove unused BuildRequires and patches
- Remove copyrighted lena.jpg images and SIFT/SURF from tarball, due to legal concerns.
- Disable dnn module from opencv_contrib, due missing BuildRequired package in Fedora (protobuf-cpp)
- Disable tracking module from opencv_contrib, due disabling dnn module (is required by this module)
- Disable CAROTENE in compilation (caused error on arm and ppc64le)
- Fix syntax error in opencv_contrib test file (opencv-3.2.0-test-file-fix.patch)

* Tue Feb 21 2017 Sandro Mani <manisandro@gmail.com> - 3.1.0-15
- Rebuild (tesseract)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 3.1.0-13
- Rebuild (libwebp)

* Thu Jan 26 2017 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-12
- Rebuild for protobuf 3.2.0

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-11
- Rebuild for Python 3.6

* Sat Dec 03 2016 Rex Dieter <rdieter@fedoraproject.org> - 3.1.0-10
- rebuild (jasper)

* Sat Nov 19 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-9
- Rebuild for protobuf 3.1.0

* Tue Jul 26 2016 Nicolas Chauvet <kwizart@gmail.com> - 3.1.0-8
- Clean uneeded symbols until fixed upstream

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri May 27 2016 Till Maas <opensource@till.name> - 3.1.0-6
- Define %%srcname for python subpackages
- Fix whitespace

* Mon May 09 2016 Sérgio Basto <sergio@serjux.com> - 3.1.0-5
- Don't clean unneeded symbols (as recommended by fedora-review), fix undefined
  symbol: cvLoadImage in Unknown on line 0 on php-facedetect package.

* Sat May 07 2016 Sérgio Basto <sergio@serjux.com> - 3.1.0-4
- Put all idefs and ifarchs outside the scope of rpm conditional builds, rather
  than vice versa, as had organized some time ago, it seems to me more correct.
- Remove SIFT/SURF from source tarball in opencv_contrib, due to legal concerns
- Redo and readd OpenCV-2.4.4-pillow.patch .
- Add OpenCV-3.1-pillow.patch to apply only opencv_contrib .
- Add the %%python_provide macro (Packaging:Python guidelines). 

* Fri Apr 22 2016 Sérgio Basto <sergio@serjux.com> - 3.1.0-3
- Use always ON and OFF instead 0 and 1 in cmake command.
- Remove BUILD_TEST and TBB_LIB_DIR variables not used by cmake.
- Add BRs: tesseract-devel, protobuf-devel, glog-devel, doxygen,
  gflags-devel, SFML-devel, libucil-devel, qt5-qtbase-devel, mesa-libGL-devel,
  mesa-libGLU-devel and hdf5-devel.
- Remove BR: vtk-devel because VTK support is disabled. Incompatible 
  combination: OpenCV + Qt5 and VTK ver.6.2.0 + Qt4
- Enable build with Qt5.
- Enable build with OpenGL.
- Enable build with UniCap.
- Also requires opencv-contrib when install opencv-devel (#1329790).

* Wed Apr 20 2016 Sérgio Basto <sergio@serjux.com> - 3.1.0-2
- Add BR:libwebp-devel .
- Merge from 2.4.12.3 package: 
  Add aarch64 and ppc64le to list of architectures where TBB is supported (#1262788).
  Use bcond tags to easily enable or disable modules.
  Fix unused-direct-shlib-dependency in cmake with global optflags.
  Added README.md with references to online documentation.
  Investigation on the documentation, added a few notes.
- Update to 3.1.0 (Fri Mar 25 2016 Pavel Kajaba <pkajaba@redhat.com> - 3.1.0-1)
- Added opencv_contrib (Thu Jul 09 2015 Sérgio Basto <sergio@serjux.com> -
  3.0.0-2)
- Update to 3.0.0 (Fri Jun 05 2015 Jozef Mlich <jmlich@redhat.com> - 3.0.0-1)

* Tue Mar 01 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.12.3-3
- Fix FTBFS with GCC 6 (#1307821)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 02 2015 Sérgio Basto <sergio@serjux.com> - 2.4.12.3-1
- Update opencv to 2.4.12.3 (#1271460).
- Add aarch64 and ppc64le to list of architectures where TBB is supported (#1262788).

* Tue Jul 14 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-5
- Use bcond tags to easily enable or disable modules.
- Package review, more cleaning in the spec file.
- Fixed unused-direct-shlib-dependency in cmake with global optflags.
- Added README.md index.rst with references to online documentation.
- Investigation on the documentation, added a few notes.

* Mon Jul 06 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-4
- Enable-gpu-module, rhbz #1236417, thanks to Rich Mattes.
- Deleted the global gst1 because it is no longer needed.

* Thu Jun 25 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-3
- Fix license tag

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-1
- Update to 2.4.11 .
- Dropped patches 0, 10, 11, 12, 13 and 14 .

* Sat Apr 11 2015 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-6
- rebuild (gcc5)

* Mon Feb 23 2015 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-5
- rebuild (gcc5)

* Tue Nov 25 2014 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-4
- rebuild (openexr)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 25 2014 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-2
- backport support for GStreamer 1 (#1123078)

* Thu Jul 03 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.4.9-1
- Update to 2.4.9

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Rex Dieter <rdieter@fedoraproject.org> 2.4.7-6
- revert pkgcmake2 patch (#1070428)

* Fri Jan 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.4.7-5
- Fix opencv_ocl isn't part of -core

* Thu Jan 16 2014 Christopher Meng <rpm@cicku.me> - 2.4.7-4
- Enable OpenCL support.
- SPEC small cleanup.

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.7-3
- rebuild (openexr)

* Mon Nov 18 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.7-2
- OpenCV cmake configuration broken (#1031312)

* Wed Nov 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.7-1
- Update to 2.4.7

* Sun Sep 08 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.6.1-2
- rebuild (openexr)

* Wed Jul 24 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.6.1-1
- Update to 2.4.6.1

* Thu May 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.5-1
- Update to 2.4.5-clean
- Spec file clean-up
- Split core libraries into a sub-package

* Sat May 11 2013 François Cami <fcami@fedoraproject.org> - 2.4.4-3
- change project URL.

* Tue Apr 02 2013 Tom Callaway <spot@fedoraproject.org> - 2.4.4-2
- make clean source without SIFT/SURF

* Sat Mar 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.4-1
- Update to 2.4.4a
- Fix tbb-devel architecture conditionals

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.4-0.2.beta
- rebuild (OpenEXR)

* Mon Feb 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.4-0.1.beta
- Update to 2.4.4 beta
- Drop python-imaging also from requires
- Drop merged patch for additionals codecs
- Disable the java binding for now (untested)

* Fri Jan 25 2013 Honza Horak <hhorak@redhat.com> - 2.4.3-7
- Do not build with 1394 libs in rhel

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 2.4.3-6
- rebuild due to "jpeg8-ABI" feature drop

* Sun Jan 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-5
- Add more FourCC for gstreamer - rhbz#812628
- Allow to use python-pillow - rhbz#895767

* Mon Nov 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-3
- Switch Build Type to ReleaseWithDebInfo to avoid -03

* Sun Nov 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-2
- Disable SSE3 and allow --with sse3 build conditional.
- Disable gpu module as we don't build cuda
- Update to 2.4.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Honza Horak <hhorak@redhat.com> - 2.4.2-1
- Update to 2.4.2

* Fri Jun 29 2012 Honza Horak <hhorak@redhat.com> - 2.4.1-2
- Fixed cmake script for generating opencv.pc file
- Fixed OpenCVConfig script file

* Mon Jun 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.1-1
- Update to 2.4.1
- Rework dependencies - rhbz#828087
  Re-enable using --with tbb,openni,eigen2,eigen3

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-8
- Rebuilt for c++ ABI breakage

* Mon Jan 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-7
- Update gcc46 patch for ARM FTBFS

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Adam Jackson <ajax@redhat.com> 2.3.1-5
- Rebuild for new libpng

* Thu Oct 20 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-4
- Rebuilt for tbb silent ABI change

* Mon Oct 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-3
- Update to 2.3.1a

* Mon Sep 26 2011 Dan Horák <dan[at]danny.cz> - 2.3.1-2
- openni is exclusive for x86/x86_64

* Fri Aug 19 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-1
- Update to 2.3.1
- Add BR openni-devel python-sphinx
- Remove deprecated cmake options
- Add --with cuda conditional (wip)
- Disable make test (unavailable)

* Thu May 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-6
- Backport fixes from branch 2.2 to date

* Tue May 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-5
- Re-enable v4l on f15
- Remove unused cmake options

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-2
- Fix with gcc46
- Disable V4L as V4L1 is disabled for Fedora 15

* Thu Jan 06 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-1
- Update to 2.2.0
- Disable -msse and -msse2 on x86_32

* Wed Aug 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.1.0-5
- -devel: include OpenCVConfig.cmake (#627359)

* Thu Jul 22 2010 Dan Horák <dan[at]danny.cz> - 2.1.0-4
- TBB is available only on x86/x86_64 and ia64

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun 25 2010 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-2
- Move samples from main to -devel
- Fix spurious permission
- Add BR tbb-devel
- Fix CFLAGS

* Fri Apr 23 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- Update libdir patch

* Tue Apr 13 2010 Karel Klic <kklic@redhat.com> - 2.0.0-10
- Fix nonstandard executable permissions

* Tue Mar 09 2010 Karel Klic <kklic@redhat.com> - 2.0.0-9
- apply the previously added patch

* Mon Mar 08 2010 Karel Klic <kklic@redhat.com> - 2.0.0-8
- re-enable testing on CMake build system
- fix memory corruption in the gaussian random number generator

* Sat Feb 27 2010 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-7
- replaced BR unicap-devel by libucil-devel (unicap split)

* Thu Feb 25 2010 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-6
- use cmake build system
- applications renamed to opencv_xxx instead of opencv-xxx
- add devel-docs subpackage #546605
- add OpenCVConfig.cmake
- enable openmp build
- enable old SWIG based python wrappers
- opencv package is a good boy and use global instead of define

* Tue Feb 16 2010 Karel Klic <kklic@redhat.com> - 2.0.0-5
- Set CXXFLAXS without -match=i386 for i386 architecture #565074

* Sat Jan 09 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 2.0.0-4
- Updated opencv-samples-Makefile (Thanks Scott Tsai) #553697

* Wed Jan 06 2010 Karel Klic <kklic@redhat.com> - 2.0.0-3
- Fixed spec file issues detected by rpmlint

* Sun Dec 06 2009 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-2
- Fix autotools scripts (missing LBP features) - #544167

* Fri Nov 27 2009 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-1
- Updated to 2.0.0
- Removed upstream-ed patches
- Ugly hack (added cvconfig.h)
- Disable %%check on ppc64

* Thu Sep 10 2009 Karsten Hopp <karsten@redhat.com> - 1.1.0-0.7.pre1
- fix build on s390x where we don't have libraw1394 and devel

* Thu Jul 30 2009 Haïkel Guémar <karlthered@gmail.com> - 1.1.0.0.6.pre1
- Fix typo I introduced that prevented build on i386/i586

* Thu Jul 30 2009 Haïkel Guémar <karlthered@gmail.com> - 1.1.0.0.5.pre1
- Added 1394 libs and unicap support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.4.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.3.pre1
- Build with gstreamer support - #491223
- Backport gcc43 fix from trunk

* Thu Jul 16 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.2.pre1
- Fix FTBFS #511705

* Fri Apr 24 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.1.pre1
- Update to 1.1pre1
- Disable CXXFLAGS hardcoded optimization
- Add BR: python-imaging, numpy
- Disable make check failure for now

* Wed Apr 22 2009 kwizart < kwizart at gmail.com > - 1.0.0-14
- Fix for gcc44
- Enable BR jasper-devel
- Disable ldconfig run on python modules (uneeded)
- Prevent timestamp change on install

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 1.0.0-12
- fix URL field

* Fri Dec 19 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.0.0-11
- Adopt latest python spec rules.
- Rebuild for Python 2.6 once again.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.0-10
- Rebuild for Python 2.6

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.0-9
- fix license tag

* Sun May 11 2008 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-8
- Adjust library order in opencv.pc.in (BZ 445937).

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0-7
- Autorebuild for GCC 4.3

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-6
- Rebuild for gcc43.

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.0.0-5
- Rebuild for selinux ppc32 issue.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-4
- Mass rebuild.

* Thu Mar 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-3
- Fix %%{_datadir}/opencv/samples ownership.
- Adjust timestamp of cvconfig.h.in to avoid re-running autoheader.

* Thu Mar 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-2
- Move all of the python module to pyexecdir (BZ 233128).
- Activate the testsuite.

* Mon Dec 11 2006 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-1
- Upstream update.

* Mon Dec 11 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-4
- Remove python-abi.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.9.9-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-2
- Stop configure.in from hacking CXXFLAGS.
- Activate testsuite.
- Let *-devel require pkgconfig.

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-1
- Upstream update.
- Don't BR: autotools.
- Install samples' Makefile as GNUmakefile.

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.7-18
- Un'%%ghost *.pyo.
- Separate %%{pythondir} from %%{pyexecdir}.

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.7-17
- Rebuild for FC6.
- BR: libtool.

* Fri Mar 17 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-16
- Rebuild.

* Wed Mar  8 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-15
- Force a re-run of Autotools by calling autoreconf.

* Wed Mar  8 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-14
- Added build dependency on Autotools.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-13
- Changed intrinsics patch so that it matches upstream.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-12
- More intrinsics patch fixing.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-11
- Don't do "make check" because it doesn't run any tests anyway.
- Back to main intrinsics patch.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-10
- Using simple intrinsincs patch.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-9
- Still more fixing of intrinsics patch for Python bindings on x86_64.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-8
- Again fixed intrinsics patch so that Python modules build on x86_64.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-7
- Fixed intrinsics patch so that it works.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-6
- Fixed Python bindings location on x86_64.

* Mon Mar  6 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-5
- SSE2 support on x86_64.

* Mon Mar  6 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-4
- Rebuild

* Sun Oct 16 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-3
- Removed useless sample compilation makefiles/project files and replaced them
  with one that works on Fedora Core.
- Removed shellbang from Python modules.

* Mon Oct 10 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-2
- Made FFMPEG dependency optional (needs to be disabled for inclusion in FE).

* Mon Oct 10 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-1
- Initial package.
