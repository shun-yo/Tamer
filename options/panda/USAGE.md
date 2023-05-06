# How to compile

I added a little modification to the code of PANDA. Please apply the patch modified.patch as follows. After applying the patch, build PANDA. (The platform I used is ubuntu14.04.)

```
% git clone https://github.com/panda-re/panda.git
% cd panda
% git checkout e109e52bc946ca1c3675309ba6ec294c50815a51
% patch -p1 < ../modified.patch
% cd ..
% mkdir build-panda
% cd build-panda/
% ../panda/build.sh
```